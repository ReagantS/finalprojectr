# Final Project Software Testing - Laporan Proyek
## Sistem Manajemen Inventori

**Nama Mata Kuliah:** Software Testing  
**Nama Mahasiswa:** [Student Name]  
**NIM:** 03081230050  
**Program Studi:** Teknik Informatika  
**Semester:** [Semester]  
**Tanggal Pengumpulan:** April 22, 2026

---

## 1. Deskripsi Sistem

### 1.1 Latar Belakang
Sistem Manajemen Inventori adalah aplikasi web yang dirancang untuk mengelola stok barang secara efisien. Aplikasi ini memungkinkan pengguna untuk melakukan operasi CRUD (Create, Read, Update, Delete), pencarian, dan penyesuaian stok dengan validasi yang ketat.

### 1.2 Tujuan Pengembangan
1. Mengimplementasikan aplikasi yang dapat diuji (testable software)
2. Mengotomatisasi pengujian melalui GitHub Actions CI/CD
3. Mencapai target code coverage minimal 60%
4. Menerapkan best practices dalam software development
5. Mensimulasikan workflow development modern dengan testing

### 1.3 Fitur Utama Sistem
- **Manajemen Item:** Tambah, edit, hapus, dan lihat detail item inventory
- **Pencarian:** Cari item berdasarkan nama atau kategori
- **Penyesuaian Stok:** Tambah atau kurangi stok dengan validasi
- **Kalkulasi Nilai:** Otomatis menghitung total nilai stok (quantity × unit_price)
- **Dashboard Web UI:** Antarmuka user-friendly untuk manajemen inventory
- **REST API:** Endpoint API untuk integrasi eksternal

---

## 2. Arsitektur Aplikasi

### 2.1 Teknologi yang Digunakan
| Komponen | Teknologi |
|----------|-----------|
| **Framework Web** | Flask 3.1.3 |
| **Database** | SQLAlchemy 2.0 + SQLite/MySQL |
| **Testing** | pytest 9.0.3 + pytest-cov 7.1.0 |
| **Language** | Python 3.11 |
| **CI/CD** | GitHub Actions |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |

### 2.2 Struktur Arsitektur Aplikasi
```
┌─────────────────────────────────────┐
│      Web UI (HTML/CSS/JavaScript)   │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │   Flask Routes     │  (routes.py)
        │   (Web + REST API) │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Business Logic     │  (service.py)
        │ (InventoryService) │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Validation Layer   │  (schemas.py)
        │ (Input Validation) │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Data Models        │  (models.py)
        │ (SQLAlchemy ORM)   │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Database Layer     │  (database.py)
        │ (SQLite/MySQL)     │
        └────────────────────┘
```

### 2.3 Komponen Utama

#### 2.3.1 Models Layer (`models.py`)
- `InventoryItem` - Model untuk item inventory dengan atribut:
  - `id` (Primary Key)
  - `name`, `category`, `location`, `description`
  - `quantity`, `unit_price`
  - `total_value` (computed property)
  - `created_at` (timestamp)

#### 2.3.2 Service Layer (`service.py`)
- `InventoryService` class dengan methods:
  - `list_items()` - Ambil semua item dengan optional search
  - `get_item()` - Ambil detail item by ID
  - `create_item()` - Buat item baru dengan validasi
  - `update_item()` - Update item dengan partial update support
  - `delete_item()` - Hapus item
  - `adjust_stock()` - Tambah/kurangi stok
  - `calculate_total_value()` - Hitung nilai total

#### 2.3.3 Routes Layer (`routes.py`)
- Web UI route: `GET /` - Serve dashboard HTML
- API Endpoints:
  - `GET /items` - List items (dengan search parameter `?q=`)
  - `GET /items/<id>` - Get single item
  - `POST /items` - Create item
  - `PUT /items/<id>` - Update item
  - `DELETE /items/<id>` - Delete item
  - `POST /items/<id>/stock` - Adjust stock
  - `GET /summary` - Get summary statistics

#### 2.3.4 Frontend (`templates/index.html` + `static/`)
- Responsive dashboard dengan:
  - Summary cards (total items, total value)
  - Form untuk tambah item
  - Tabel dengan pagination
  - Search/filter functionality
  - Modal edit form
  - Alert notifications

---

## 3. Strategi Pengujian

### 3.1 Unit Testing Strategy

#### Tujuan Unit Test:
Menguji fungsi individual dan logika bisnis secara terisolasi tanpa dependencies eksternal.

#### Test Coverage Area:

| Aspek | Test Case | Jumlah |
|-------|-----------|--------|
| **Validasi Input** | Reject empty name, negative qty/price | 3 |
| **CRUD Operations** | Create, Read, Update, Delete | 5 |
| **Stock Management** | Adjust (increase/decrease/reject) | 3 |
| **Search/Filter** | List items, search by name | 2 |
| **Business Logic** | Calculate total value, partial update | 2 |
| **Total Unit Tests** | | **15 tests** |

#### Contoh Unit Test:
```python
def test_validate_item_payload_rejects_negative_quantity(service):
    """Test bahwa service menolak quantity negatif"""
    with pytest.raises(ValueError):
        service.create_item({
            "name": "Item",
            "category": "Cat",
            "location": "Loc",
            "quantity": -1,  # Invalid
            "unit_price": 100.0
        })
```

### 3.2 Integration Testing Strategy

#### Tujuan Integration Test:
Menguji alur end-to-end API endpoints dengan interaksi database nyata.

#### Test Coverage Area:

| Endpoint | Test Scenario | Jumlah |
|----------|---------------|--------|
| **List Items** | GET /items (empty, filtered, etc) | 1 |
| **Create Item** | POST /items with validation | 1 |
| **Get Item** | GET /items/<id> | 1 |
| **Update Item** | PUT /items/<id> | 1 |
| **Adjust Stock** | POST /items/<id>/stock | 1 |
| **Delete Item** | DELETE /items/<id> | 1 |
| **Total Integration Tests** | | **6 tests** |

#### Contoh Integration Test:
```python
def test_create_item_endpoint(client):
    """Test POST /items endpoint"""
    payload = {
        "name": "USB Drive",
        "category": "Electronics",
        "location": "Shelf 1",
        "quantity": 8,
        "unit_price": 7.5,
    }
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    assert response.get_json()["total_value"] == 60.0
```

### 3.3 Test Coverage Analysis

#### Current Coverage:
```
TOTAL               242 Statements   37 Miss   85% Coverage
```

#### Per-Module Coverage:
| Module | Coverage | Status |
|--------|----------|--------|
| `app/__init__.py` | 100% | ✅ Excellent |
| `app/models.py` | 100% | ✅ Excellent |
| `app/service.py` | 98% | ✅ Excellent |
| `app/database.py` | 95% | ✅ Excellent |
| `app/schemas.py` | 84% | ✅ Good |
| `app/routes.py` | 80% | ✅ Good |
| `app/config.py` | 36% | ⚠️ Config-heavy |
| `app/main.py` | 0% | ℹ️ Entry point only |

#### Coverage Target Achievement:
- **Target:** 60% minimum
- **Achieved:** 85% ✅
- **Achievement Rate:** 142% of target

### 3.4 Testing Tools & Configuration
- **Test Runner:** pytest 9.0.3
- **Coverage Tool:** pytest-cov 7.1.0
- **Test Fixtures:** conftest.py dengan Flask test client
- **Command:** `pytest --cov=app --cov-report=term-missing`

---

## 4. Continuous Integration Pipeline

### 4.1 GitHub Actions Workflow

#### Workflow File: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests with coverage
        run: |
          pytest --cov=app --cov-report=xml
      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml
```

### 4.2 Pipeline Execution Flow

```
1. Code Push/PR Created
        ↓
2. GitHub Actions Triggered
        ↓
3. Setup Environment (Python 3.11)
        ↓
4. Install Dependencies
        ↓
5. Run All Tests (21 test cases)
        ↓
6. Generate Coverage Report (85%)
        ↓
7. Upload Artifacts
        ↓
8. Workflow Status: PASS/FAIL
```

### 4.3 CI/CD Benefits
- ✅ **Automated Testing** - Tests run otomatis setiap push/PR
- ✅ **Early Bug Detection** - Bugs terdeteksi sebelum merge
- ✅ **Code Quality Assurance** - Coverage tracking
- ✅ **Build Artifact Preservation** - Coverage report tersimpan
- ✅ **Consistency** - Same testing environment setiap run

---

## 5. Hasil Pengujian

### 5.1 Test Execution Summary
```
========================= 21 tests collected =========================

PASSED:
  ✅ tests/test_unit_inventory.py::test_validate_item_payload_rejects_empty_name
  ✅ tests/test_unit_inventory.py::test_validate_item_payload_rejects_negative_quantity
  ✅ tests/test_unit_inventory.py::test_validate_item_payload_rejects_negative_price
  ✅ tests/test_unit_inventory.py::test_create_item_persists_record
  ✅ tests/test_unit_inventory.py::test_calculate_total_value
  ✅ tests/test_unit_inventory.py::test_update_item_changes_fields
  ✅ tests/test_unit_inventory.py::test_adjust_stock_increases_quantity
  ✅ tests/test_unit_inventory.py::test_adjust_stock_decreases_quantity
  ✅ tests/test_unit_inventory.py::test_adjust_stock_rejects_negative_result
  ✅ tests/test_unit_inventory.py::test_delete_item_removes_record
  ✅ tests/test_unit_inventory.py::test_search_items_matches_name
  ✅ tests/test_unit_inventory.py::test_list_items_returns_all
  ✅ tests/test_unit_inventory.py::test_partial_update_preserves_fields
  ✅ tests/test_unit_inventory.py::test_update_item_rejects_invalid_quantity
  ✅ tests/test_unit_inventory.py::test_create_item_requires_category_and_location
  ✅ tests/test_integration_api.py::test_get_empty_items
  ✅ tests/test_integration_api.py::test_create_item_endpoint
  ✅ tests/test_integration_api.py::test_get_item_endpoint
  ✅ tests/test_integration_api.py::test_update_item_endpoint
  ✅ tests/test_integration_api.py::test_adjust_stock_endpoint
  ✅ tests/test_integration_api.py::test_delete_item_endpoint

========================= 21 passed in 0.44s ==========================
========================= 85% coverage ==============================
```

### 5.2 Test Execution Time
- **Total Execution Time:** 0.44 seconds
- **Average per test:** ~21 ms
- **Performance:** ✅ Excellent

### 5.3 Coverage Metrics
| Metric | Value | Status |
|--------|-------|--------|
| Total Statements | 242 | - |
| Statements Covered | 205 | - |
| Statements Missed | 37 | - |
| Coverage Percentage | 85% | ✅ 142% of 60% target |

---

## 6. Kesimpulan & Rekomendasi

### 6.1 Pencapaian Requirement
| Requirement | Target | Achieved | Status |
|------------|--------|----------|--------|
| Unit Tests | ≥15 | 15 | ✅ Met |
| Integration Tests | ≥5 | 6 | ✅ Met |
| Code Coverage | ≥60% | 85% | ✅ Exceeded |
| CI/CD Pipeline | Required | ✅ | ✅ Met |
| Web UI | Required | ✅ | ✅ Met |
| REST API | Required | ✅ | ✅ Met |
| README Documentation | Required | ✅ | ✅ Met |

### 6.2 Kesimpulan
Sistem Manajemen Inventori telah berhasil dikembangkan dengan:
- ✅ **Testable Architecture** - Clean separation of concerns
- ✅ **Comprehensive Testing** - 21 test cases covering main flows
- ✅ **High Code Coverage** - 85% coverage (target 60%)
- ✅ **Automated CI/CD** - GitHub Actions pipeline siap production
- ✅ **Professional Web UI** - Responsive dan user-friendly
- ✅ **Good Documentation** - README + code comments lengkap

### 6.3 Rekomendasi untuk Pengembangan Selanjutnya
1. **Authentication & Authorization** - Tambah user login system
2. **Advanced Reporting** - Export laporan ke PDF/Excel
3. **Real-time Updates** - Implement WebSocket untuk live updates
4. **Advanced Search** - Filter by date range, price range, etc
5. **Performance Optimization** - Database indexing, query optimization
6. **Monitoring & Logging** - Application monitoring untuk production

---

## 7. Referensi

### 7.1 Teknologi & Framework
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- pytest Documentation: https://docs.pytest.org/
- GitHub Actions: https://docs.github.com/en/actions

### 7.2 Best Practices References
- Clean Code - Robert C. Martin
- Test-Driven Development (TDD) - Kent Beck
- Design Patterns - Gang of Four
- REST API Best Practices - API Design Standards

---

**Laporan ini menunjukkan bahwa semua requirement mata kuliah Software Testing telah terpenuhi dengan excellence.**

**Tanggal Laporan:** April 22, 2026  
**Status:** ✅ SELESAI
