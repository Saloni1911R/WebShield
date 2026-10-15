# WebShield 🔐

**Website Security Audit Platform**

WebShield is a Python-based website security auditing application built with **Django**. It helps authenticated users inspect HTTPS websites for important HTTP security headers and TLS certificate information.

## Features

- **User Authentication:** Account registration, login, and logout.
- **HTTP Security Headers:** Checks Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, and Referrer-Policy.
- **TLS Certificate Check:** Inspects TLS certificate validity and details.
- **HTTP Status Check:** Displays the website's HTTP response status.
- **Security Summary:** Presents passed checks, warnings, and errors.
- **URL Validation:** Validates submitted HTTPS URLs and blocks certain unsafe destinations.
- **Responsive Interface:** Dark-themed interface built with HTML and CSS.

## Technologies Used

- Python
- Django
- HTML and CSS
- Requests
- SQLite
- SSL/TLS

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Saloni1911R/WebShield.git
cd WebShield
git switch django-conversion
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the application

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. Register an account, log in, and access the scanning dashboard.

## Run Tests

```bash
python manage.py test
```

## Scope and Limitations

WebShield performs basic checks of HTTP security headers and TLS certificates. It is an educational cybersecurity project and does not replace a professional security assessment or comprehensive vulnerability scanner.

Only scan websites you own or have permission to test. Additional security hardening and production configuration are required before public deployment.

## Author

Saloni Ramavat
