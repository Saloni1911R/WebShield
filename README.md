# WebShield 🛡️

**Website Security Audit Platform**

WebShield is a Python-based web application built with Django that helps users inspect HTTPS websites for important security headers and TLS certificate information.

## Features

- **User Authentication:** Register, log in, and log out securely.
- **HTTPS Validation:** Accepts HTTPS website URLs for scanning.
- **Security Header Analysis:** Checks important HTTP security headers:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Content-Type-Options
  - X-Frame-Options
  - Referrer-Policy
- **TLS Certificate Inspection:** Checks TLS certificate validity and certificate details.
- **URL Validation:** Rejects invalid URLs and certain unsafe destinations.
- **Responsive Interface:** Dark-themed interface with a modern WebShield design.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Security:** HTTPS validation, HTTP security-header checks, TLS certificate inspection
- **Testing:** Django testing framework

## Project Structure

```text
WebShield/
├── config/                 # Django project settings and URLs
├── scanner/                # Website scanning application
│   ├── migrations/
│   ├── templates/
│   │   └── scanner/
│   │       └── index.html
│   ├── forms.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── registration/
│       ├── login.html
│       └── register.html
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Saloni1911R/WebShield.git
cd WebShield
```

### 2. Switch to the Django branch

```bash
git switch django-conversion
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

Register an account, log in, and enter an HTTPS website URL to perform a scan.

## Usage

1. Create a WebShield account.
2. Log in to access the scanning dashboard.
3. Enter an HTTPS website URL.
4. Run the security scan.
5. Review the security-header results and TLS certificate information.

## Security Disclaimer

WebShield is an educational cybersecurity project intended for authorized security testing and learning. Scan only websites you own or have permission to assess.

A successful scan does not guarantee that a website is completely secure. Header checks and TLS inspection cover only a limited set of security indicators.

## Future Improvements

- Automated security tests
- Improved protection against unsafe URL destinations
- Detailed scan reports
- Production deployment with secure Django settings
- Additional security checks

## Author

Developed as a cybersecurity and web security learning project.
