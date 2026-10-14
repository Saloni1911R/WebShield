
import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse


def check_tls_certificate(url):
    parsed = urlparse(url)

    if parsed.scheme != "https" or not parsed.hostname:
        return {
            "status": "Error",
            "message": "Enter a valid HTTPS URL."
        }

    hostname = parsed.hostname
    port = parsed.port or 443

    try:
        context = ssl.create_default_context()

        with socket.create_connection(
            (hostname, port), timeout=5
        ) as connection:
            with context.wrap_socket(
                connection, server_hostname=hostname
            ) as tls_connection:

                certificate = tls_connection.getpeercert()

        expiry_text = certificate.get("notAfter")

        if not expiry_text:
            return {
                "status": "Error",
                "message": "Certificate expiry date is unavailable."
            }

        expiry_date = datetime.strptime(
            expiry_text, "%b %d %H:%M:%S %Y %Z"
        ).replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        days_left = (expiry_date - now).days

        issuer = dict(
            (key, value)
            for group in certificate.get("issuer", [])
            for key, value in group
        )

        return {
            "status": "Valid",
            "hostname": hostname,
            "issuer": issuer.get("organizationName", "Not provided"),
            "expires": expiry_date.strftime("%Y-%m-%d %H:%M UTC"),
            "days_left": days_left,
            "message": (
                "Certificate has expired."
                if days_left < 0 else
                "Certificate expires soon."
                if days_left <= 30 else
                "Certificate is valid and not expiring soon."
            )
        }

    except (OSError, ssl.SSLError, ValueError) as error:
        return {
            "status": "Error",
            "message": f"TLS validation failed: {error}"
        }
