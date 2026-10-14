# WebShield 🔐

**WebShield** is a Python-based website security auditing tool built with Flask. It performs basic security checks on a website and displays the results through a web interface.

## Features

- **HTTP Security Headers:** Checks for Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, and Referrer-Policy.
- **TLS Certificate Check:** Verifies the website's TLS certificate.
- **HTTP Status Check:** Displays the website's HTTP response status.
- **Security Summary:** Shows passed checks, warnings, and errors in one place.

## Technologies Used

- Python
- Flask
- HTML and CSS
- Requests
- SSL/TLS

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Saloni1911R/WebShield.git
   cd WebShield
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## Scope and Limitations

WebShield performs basic checks of HTTP security headers and TLS certificates. It is an educational project and does not replace a professional security assessment or comprehensive vulnerability scanner.

Only scan websites you own or have permission to test. The application is intended for local development; additional protections are required before public deployment.

## Author

Saloni Ramavat
