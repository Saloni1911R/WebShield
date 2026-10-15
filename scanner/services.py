import ipaddress
import socket
import ssl
from urllib.parse import urlparse

import requests

from tls_check import check_tls_certificate


SECURITY_HEADERS = {
    "Content-Security-Policy":
        "Helps control which resources a browser can load.",
    "Strict-Transport-Security":
        "Instructs browsers to use HTTPS for future requests.",
    "X-Content-Type-Options":
        "Helps prevent MIME-type sniffing.",
    "X-Frame-Options":
        "Helps protect against clickjacking.",
    "Referrer-Policy":
        "Controls referrer information sent by browsers.",
}


def validate_url(url):
    parsed = urlparse(url)

    if parsed.scheme != "https" or not parsed.hostname:
        return False, "Enter a valid HTTPS URL."

    if parsed.username or parsed.password:
        return False, "URLs containing credentials are not allowed."

    try:
        addresses = socket.getaddrinfo(
            parsed.hostname,
            parsed.port or 443,
            type=socket.SOCK_STREAM,
        )

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if not ip.is_global:
                return False, "Private or non-public addresses are blocked."

    except (OSError, ValueError):
        return False, "Could not resolve the website address."

    return True, ""


def scan_website(url):
    valid, error = validate_url(url)

    if not valid:
        return {"error": error, "findings": []}

    try:
        response = requests.get(
            url,
            timeout=8,
            allow_redirects=False,
            stream=True,
            headers={"User-Agent": "WebShield-Student-Audit/1.0"},
        )

        try:
            findings = []

            for name, explanation in SECURITY_HEADERS.items():
                present = name in response.headers

                findings.append({
                    "name": name,
                    "present": present,
                    "status": "Pass" if present else "Warning",
                    "explanation": explanation,
                    "recommendation": (
                        "Review the header's configuration."
                        if present
                        else f"Consider configuring {name} where appropriate."
                    ),
                })

            result = {
                "error": None,
                "status_code": response.status_code,
                "findings": findings,
                "tls": check_tls_certificate(url),
            }

            passed = sum(item["present"] for item in findings)
            warnings = len(findings) - passed
            errors = int(result["tls"]["status"] != "Valid")

            if result["tls"]["status"] == "Valid":
                passed += 1

            result["summary"] = {
                "passed": passed,
                "warnings": warnings,
                "errors": errors,
            }

            return result

        finally:
            response.close()

    except requests.RequestException:
        return {
            "error": "The request failed or the website could not be reached.",
            "findings": [],
        }
