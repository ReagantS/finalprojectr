# Final Project Inventory System

[![CI](https://github.com/a137816-cmd/finalprojectreag/actions/workflows/ci.yml/badge.svg)](https://github.com/a137816-cmd/finalprojectreag/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-60%25-brightgreen)](README.md)

A simple inventory management system built in Python with support for MySQL/XAMPP. The project includes automated unit tests, integration tests, and a GitHub Actions CI pipeline that collects coverage data.

## Features
- Add, view, update, and delete inventory items
- Search inventory by item name or category
- Adjust stock safely with validation
- Calculate total item value automatically
- Database support for local SQLite and MySQL/XAMPP

## Project Structure
- `app/` – Python application code
- `database/` – MySQL schema and PHP setup script
- `tests/` – Unit and integration tests
- `.github/workflows/ci.yml` – GitHub Actions pipeline

## Requirement Coverage
- Unit tests: 15+ test cases
- Integration tests: 5+ test cases
- Test coverage report with target 60%+
- CI pipeline runs on `push` and `pull_request`

## Setup
### Python environment
1. Install Python 3.11+.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

### MySQL / XAMPP setup
1. Install XAMPP and start Apache + MySQL.
2. Create the database and table using the PHP setup script:
   ```bash
   php database\setup_database.php
   ```
3. Configure environment variables if using MySQL:
   ```powershell
   $env:DB_DRIVER='mysql'
   $env:MYSQL_HOST='127.0.0.1'
   $env:MYSQL_PORT='3306'
   $env:MYSQL_USER='root'
   $env:MYSQL_PASSWORD=''
   $env:MYSQL_DATABASE='inventory_db'
   ```

### Run the app
```bash
python -m app.main
```
Open `http://127.0.0.1:5000/items` to browse inventory endpoints.

## Testing
Run all tests with coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

## GitHub Actions CI
The workflow installs dependencies, runs tests, and reports coverage on every `push` and `pull_request`.

## Database scripts
- `database/schema.sql` – SQL schema for MySQL
- `database/setup_database.php` – PHP setup script for XAMPP MySQL

## GitHub Repository
Repository: `https://github.com/a137816-cmd/finalprojectreag`

## Notes
If you want to use MySQL in development, set the environment variables and run the PHP script before starting the app.
