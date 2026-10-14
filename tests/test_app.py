
import pytest
from unittest.mock import patch

import app as webshield


@pytest.fixture
def client():
    webshield.app.config["TESTING"] = True

    with webshield.app.test_client() as test_client:
        yield test_client


def test_homepage_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"WebShield" in response.data


def test_url_validation_rejects_http():
    valid, message = webshield.validate_url("http://example.com")

    assert valid is False
    assert "HTTPS" in message


def test_url_validation_rejects_credentials():
    valid, message = webshield.validate_url(
        "https://user:password@example.com"
    )

    assert valid is False
    assert "credentials" in message


def test_missing_security_headers_are_warnings():
    mock_response = type(
        "MockResponse",
        (),
        {
            "headers": {},
            "status_code": 200,
            "close": lambda self: None,
        },
    )()

    with patch.object(
        webshield, "validate_url", return_value=(True, "")
    ), patch.object(
        webshield.requests, "get", return_value=mock_response
    ):
        result = webshield.check_headers("https://example.com")

    assert result["error"] is None
    assert len(result["findings"]) == 5
    assert all(item["status"] == "Warning" for item in result["findings"])

def test_url_validation_rejects_private_ip():
    from app import validate_url

    valid, error = validate_url("https://127.0.0.1")

    assert valid is False
    assert "blocked" in error.lower()


def test_url_validation_rejects_localhost():
    from app import validate_url

    valid, error = validate_url("https://localhost")

    assert valid is False
    assert "blocked" in error.lower()


def test_tls_checker_rejects_http():
    from tls_check import check_tls_certificate

    result = check_tls_certificate("http://example.com")

    assert result["status"] == "Error"
    assert result["message"] == "Enter a valid HTTPS URL."


def test_tls_checker_rejects_missing_hostname():
    from tls_check import check_tls_certificate

    result = check_tls_certificate("https://")

    assert result["status"] == "Error"

def test_redirects_are_not_followed():
    mock_response = type(
        "MockResponse",
        (),
        {
            "headers": {},
            "status_code": 302,
            "close": lambda self: None,
        },
    )()

    with patch.object(
        webshield, "validate_url", return_value=(True, "")
    ), patch.object(
        webshield.requests,
        "get",
        return_value=mock_response,
    ) as mock_get:
        result = webshield.check_headers("https://example.com")

    assert result["error"] is None
    assert result["status_code"] == 302
    assert mock_get.call_args.kwargs["allow_redirects"] is False


def test_request_failure_is_handled():
    with patch.object(
        webshield, "validate_url", return_value=(True, "")
    ), patch.object(
        webshield.requests,
        "get",
        side_effect=webshield.requests.ConnectionError,
    ):
        result = webshield.check_headers("https://example.com")

    assert result["error"] == (
        "The request failed or the website could not be reached."
    )
    assert result["findings"] == []
