from flask import Flask, render_template, request
from tls_check import check_tls_certificate
from urllib.parse import urlparse
import ipaddress
import socket
import requests

app = Flask(__name__)

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

    host = parsed.hostname

    try:
        addresses = socket.getaddrinfo(
            host, parsed.port or 443, type=socket.SOCK_STREAM
        )

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])
            if not ip.is_global:
                return False, "Private or non-public addresses are blocked."

    except (OSError, ValueError):
        return False, "Could not resolve the website address."

    return True, ""


def check_headers(url):
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
            headers = response.headers
            findings = []

            for name, explanation in SECURITY_HEADERS.items():
                present = name in headers

                findings.append({
                    "name": name,
                    "present": present,
                    "status": "Pass" if present else "Warning",
                    "explanation": explanation,
                    "recommendation": (
                        "Review the header's configuration."
                        if present else
                        f"Consider configuring {name} where appropriate."
                    ),
                })

            return {
                "error": None,
                "status_code": response.status_code,
                "findings": findings,
            }
        finally:
            response.close()

    except requests.RequestException:
        return {
            "error": "The request failed or the website could not be reached.",
            "findings": [],
        }



@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    submitted_url = ""

    if request.method == "POST":
        submitted_url = request.form.get("url", "").strip()

        if len(submitted_url) > 2048:
            result = {
                "error": "The URL is too long.",
                "findings": [],
            }
        else:
            result = check_headers(submitted_url)

            if not result.get("error"):
                result["tls"] = check_tls_certificate(submitted_url)

                # Count header checks and TLS validation separately.
                findings = result.get("findings", [])

                passed = sum(
                    1 for item in findings if item["present"]
                )
                warnings = sum(
                    1 for item in findings if not item["present"]
                )
                errors = 0

                tls = result["tls"]

                if tls["status"] == "Valid":
                    passed += 1
                else:
                    errors += 1

                result["summary"] = {
                    "passed": passed,
                    "warnings": warnings,
                    "errors": errors,
                }

    return render_template(
        "index.html",
        result=result,
        submitted_url=submitted_url,
    )



if __name__ == "__main__":
    app.run(debug=True)
