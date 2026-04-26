# Final Project Inventory System

[![CI](https://github.com/a137816-cmd/finalprojectreag/actions/workflows/ci.yml/badge.svg)](https://github.com/a137816-cmd/finalprojectreag/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)](README.md)
[![Tests](https://img.shields.io/badge/tests-21%2F21%20passed-success)]()
[![Python 3.11](https://img.shields.io/badge/python-3.11%2B-blue)]()

Sistem Manajemen Inventori yang lengkap dengan automated testing, CI/CD pipeline, dan web dashboard.  
**Final Project untuk mata kuliah Software Testing - Implementasi Testable Software dengan GitHub Actions CI**

## Features
- 🎨 **Web UI Dashboard** – Tampilan web yang user-friendly untuk mengelola inventory
- ✅ Add, view, update, and delete inventory items
- 🔍 Search inventory by item name or category
- 📊 Adjust stock safely with validation
- 💰 Calculate total item value automatically
- 💾 Database support for local SQLite and MySQL/XAMPP
- 🔌 REST API endpoints untuk integrasi eksternal

## Project Structure
```
Finale Project/
├── app/                          # Python Flask application
│   ├── __init__.py              # Flask app initialization
│   ├── main.py                  # Entry point
│   ├── config.py                # Configuration settings
│   ├── database.py              # Database connection
│   ├── models.py                # SQLAlchemy models
│   ├── routes.py                # Flask routes (API + Web UI)
│   ├── schemas.py               # Request validation schemas
│   ├── service.py               # Business logic
│   ├── templates/               # HTML templates
│   │   └── index.html           # Main web UI dashboard
│   └── static/                  # Static files (CSS, JS)
│       ├── css/
│       │   └── style.css        # Styling
│       └── js/
│           └── app.js           # Frontend JavaScript
├── database/                    # Database scripts
│   ├── schema.sql               # MySQL schema
│   └── setup_database.php       # PHP setup script
├── tests/                       # Test suite
│   ├── conftest.py
│   ├── test_integration_api.py  # Integration tests
│   └── test_unit_inventory.py   # Unit tests
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
├── requirements.txt             # Python dependencies
└── README.md
```

## Requirements Checklist ✅

### 3. Ketentuan Aplikasi
- ✅ Aplikasi: **Sistem Manajemen Inventori**
- ✅ Fitur utama ≥2-3:
  - ✅ Manajemen Item (CRUD)
  - ✅ Pencarian & Filter
  - ✅ Penyesuaian Stok
  - ✅ Dashboard Web UI
- ✅ Validasi input: Ada (name, category, location, quantity, price)
- ✅ Logika bisnis: Ada (kalkulasi nilai stok, validasi stok)
- ✅ Penyimpanan data: SQLite/MySQL dengan SQLAlchemy ORM
- ✅ Framework: Flask (Python)

### 4. Ketentuan Pengujian

#### 4.1 Unit Testing ✅
- ✅ **Minimal: 15 test cases**
- ✅ **Actual: 15 test cases di `tests/test_unit_inventory.py`**
  - Validasi input: 3 tests
  - CRUD operations: 5 tests
  - Stock management: 3 tests
  - Search/Filter: 2 tests
  - Business logic: 2 tests

#### 4.2 Integration Testing ✅
- ✅ **Minimal: 5 integration tests**
- ✅ **Actual: 6 integration tests di `tests/test_integration_api.py`**
  - GET /items (empty list)
  - POST /items (create with validation)
  - GET /items/<id> (retrieve)
  - PUT /items/<id> (update)
  - POST /items/<id>/stock (adjust stock)
  - DELETE /items/<id> (delete)

#### 4.3 Test Coverage ✅
- ✅ **Target: ≥60% code coverage**
- ✅ **Achieved: 85% code coverage**
- ✅ Coverage report: Generated with pytest-cov

### 5. Continuous Integration ✅
- ✅ GitHub Actions workflow: `.github/workflows/ci.yml`
- ✅ Triggers: `push` dan `pull_request` ke branch main/master
- ✅ Pipeline steps:
  - ✅ Install dependencies
  - ✅ Build aplikasi
  - ✅ Menjalankan semua test
  - ✅ Generate coverage report
  - ✅ Upload artifacts

### 6. Struktur Repository ✅
- ✅ README.md: Lengkap dengan dokumentasi
- ✅ Folder source code: `app/`
- ✅ Folder test: `tests/`
- ✅ Konfigurasi GitHub Actions: `.github/workflows/ci.yml`
- ✅ Commit history: Jelas di git repository

### 7. Badge Repository ✅
- ✅ Build status badge: CI workflow badge
- ✅ Test coverage badge: 85% coverage
- ✅ Test result badge: 21/21 passed

### 8. Laporan Proyek ✅
- ✅ File: `LAPORAN_PROYEK.md` (2-3 halaman format)
- ✅ Berisi:
  - ✅ Deskripsi sistem
  - ✅ Arsitektur aplikasi
  - ✅ Strategi pengujian
  - ✅ Penjelasan test coverage
  - ✅ Penjelasan pipeline CI

### 9. Teknologi ✅
- ✅ Framework: Flask 3.1.3 (Python)
- ✅ Testing: pytest 9.0.3 + pytest-cov 7.1.0
- ✅ Database: SQLAlchemy 2.0 + SQLite/MySQL
- ✅ Language: Python 3.11+

---

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

#### Akses Aplikasi
- 🌐 **Web UI Dashboard**: Buka browser dan akses `http://127.0.0.1:5000`
  - Tampilan interaktif untuk mengelola inventory
  - Fitur: tambah, edit, hapus, cari, dan adjust stock item
  
- 📡 **REST API Endpoints**: 
  - `http://127.0.0.1:5000/items` – Daftar semua item
  - `http://127.0.0.1:5000/items/<id>` – Detail item tertentu
  - `http://127.0.0.1:5000/summary` – Ringkasan inventory

## Testing
Run all tests with coverage:
```bash
pytest --cov=app --cov-report=term-missing -v
```

### Test Results Summary
```
======================== 21 tests collected ========================
PASSED:  21 tests ✅
FAILED:  0 tests
SKIPPED: 0 tests
COVERAGE: 85% (242 statements, 37 missed)
EXECUTION TIME: 0.44 seconds
```

### Test Statistics
- **Unit Tests:** 15 tests (test_unit_inventory.py)
- **Integration Tests:** 6 tests (test_integration_api.py)
- **Total Tests:** 21 tests
- **Pass Rate:** 100%
- **Code Coverage:** 85% (Target: 60%+)

### Running Specific Tests
```bash
# Run only unit tests
pytest tests/test_unit_inventory.py -v

# Run only integration tests
pytest tests/test_integration_api.py -v

# Run specific test
pytest tests/test_unit_inventory.py::test_create_item_persists_record -v

# Run with coverage and HTML report
pytest --cov=app --cov-report=html
```

## Web UI Features
Dashboard inventory yang intuitif dengan fitur:
- 📊 **Summary Statistics** – Total item dan nilai stok
- ➕ **Add Item** – Form untuk tambah item baru dengan validasi
- 📋 **Item Table** – Daftar lengkap inventory dengan sorting
- 🔍 **Search & Filter** – Cari item berdasarkan nama atau kategori
- ✏️ **Edit Item** – Modal form untuk mengubah data item
- 📦 **Adjust Stock** – Tambah atau kurangi stok secara aman
- 🗑️ **Delete Item** – Hapus item dengan konfirmasi
- 💰 **Auto-calculation** – Total nilai dihitung otomatis (qty × harga)

## GitHub Actions CI

### Workflow Configuration
- **File:** `.github/workflows/ci.yml`
- **Triggers:** Push & Pull Request ke branch `main` atau `master`
- **Environment:** Windows Latest + Python 3.11

### Pipeline Steps
1. **Checkout** - Ambil source code
2. **Setup Python** - Install Python 3.11
3. **Install Dependencies** - Install dari requirements.txt
4. **Run Tests** - Jalankan pytest dengan coverage
5. **Generate Report** - Buat coverage.xml
6. **Upload Artifacts** - Simpan coverage report

### View Build Status
- **GitHub Actions:** Lihat di tab "Actions" di repository
- **Coverage Report:** Download dari artifacts setelah workflow selesai
- **Badge Status:** Ditampilkan di README

### CI/CD Benefits
✅ **Otomasi:** Tests berjalan otomatis setiap push  
✅ **Early Detection:** Bug terdeteksi sebelum merge  
✅ **Quality Metrics:** Coverage tracking & trending  
✅ **Consistency:** Same testing environment every run  
✅ **Transparency:** Build status visible untuk semua developer

## Testing Strategy
### Unit Tests (`test_unit_inventory.py`)
Menguji logika bisnis individual dengan 15 test cases:
- **Validasi Input (3 tests):** Empty name, negative quantity, negative price
- **CRUD Operations (5 tests):** Create, get, update, delete, list items
- **Stock Management (3 tests):** Increase, decrease, reject negative stock
- **Search & List (2 tests):** Search by name/category, list all items
- **Business Logic (2 tests):** Calculate total value, partial update

### Integration Tests (`test_integration_api.py`)
Menguji alur end-to-end dengan 6 test cases:
- **GET /items** - Empty list handling
- **POST /items** - Create item with validation
- **GET /items/<id>** - Retrieve single item
- **PUT /items/<id>** - Update item fields
- **POST /items/<id>/stock** - Stock adjustment
- **DELETE /items/<id>** - Delete item & verify

### Coverage Metrics
```
Total Code: 242 statements
Covered:    205 statements (85%)
Missed:     37 statements (15%)
Target:     60% minimum ✅ Exceeded by 25%
```

Per-module coverage:
- models.py:     100% ⭐
- __init__.py:   100% ⭐
- service.py:    98%  ⭐
- database.py:   95%  ⭐
- schemas.py:    84%
- routes.py:     80%

## Database scripts
- `database/schema.sql` – SQL schema for MySQL
- `database/setup_database.php` – PHP setup script for XAMPP MySQL

## API Reference

### Endpoints

#### List Items
```
GET /items?q={search_query}
Response: { "items": [...] }
Status: 200 OK
```

#### Get Single Item
```
GET /items/{id}
Response: { "id": 1, "name": "...", ... }
Status: 200 OK / 404 Not Found
```

#### Create Item
```
POST /items
Content-Type: application/json
Body: {
  "name": "Item Name",
  "category": "Category",
  "location": "Location",
  "quantity": 10,
  "unit_price": 5.50,
  "description": "Optional description"
}
Response: 201 Created / 422 Unprocessable Entity
```

#### Update Item
```
PUT /items/{id}
Content-Type: application/json
Body: { "quantity": 15, "unit_price": 6.00 }
Response: 200 OK / 404 Not Found / 422 Validation Error
```

#### Adjust Stock
```
POST /items/{id}/stock
Content-Type: application/json
Body: { "amount": 5 }  # Positive to add, negative to subtract
Response: 200 OK / 404 Not Found / 422 Invalid Amount
```

#### Delete Item
```
DELETE /items/{id}
Response: 200 OK / 404 Not Found
```

#### Get Summary
```
GET /summary
Response: { "total_items": 10, "total_stock_value": 1250.50 }
Status: 200 OK
```

## GitHub Repository
Repository: `https://github.com/a137816-cmd/finalprojectreag`

## Project Documentation
- 📄 **Main Report:** See `LAPORAN_PROYEK.md` for detailed project report (2-3 pages)
- 📋 **Architecture:** See "Project Structure" section above
- 🧪 **Testing Strategy:** See "Testing Strategy" section below

## Notes
- If you want to use MySQL in development, set the environment variables and run the PHP script before starting the app.
- For production deployment, use a proper WSGI server (Gunicorn, uWSGI) instead of Flask development server.
- All tests should pass before pushing to repository (enforced by CI).
- Coverage reports are automatically generated and uploaded as CI artifacts.
