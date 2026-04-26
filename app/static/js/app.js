// API endpoints
const API_BASE = '/items';
const API_SUMMARY = '/summary';

// DOM Elements
const addItemForm = document.getElementById('addItemForm');
const itemsTableBody = document.getElementById('itemsTableBody');
const searchInput = document.getElementById('searchInput');
const refreshBtn = document.getElementById('refreshBtn');
const editModal = document.getElementById('editModal');
const editItemForm = document.getElementById('editItemForm');
const closeBtn = document.querySelector('.close');
const cancelEditBtn = document.getElementById('cancelEditBtn');
const alertToast = document.getElementById('alertToast');

// Event Listeners
addItemForm.addEventListener('submit', handleAddItem);
searchInput.addEventListener('input', handleSearch);
refreshBtn.addEventListener('click', loadItems);
closeBtn.addEventListener('click', closeEditModal);
cancelEditBtn.addEventListener('click', closeEditModal);
editItemForm.addEventListener('submit', handleEditItem);
window.addEventListener('click', closeEditModalOnClickOutside);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadItems();
    loadSummary();
});

/**
 * Load all items and display in table
 */
async function loadItems() {
    try {
        const response = await fetch(API_BASE);
        if (!response.ok) throw new Error('Failed to load items');

        const data = await response.json();
        const items = data.items || [];
        displayItems(items);
    } catch (error) {
        console.error('Error loading items:', error);
        showAlert('Gagal memuat data inventory', 'error');
        displayEmptyState();
    }
}

/**
 * Load and display summary statistics
 */
async function loadSummary() {
    try {
        const response = await fetch(API_SUMMARY);
        if (!response.ok) throw new Error('Failed to load summary');

        const data = await response.json();
        document.getElementById('totalItems').textContent = data.total_items;
        document.getElementById('totalValue').textContent = formatCurrency(data.total_stock_value);
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

/**
 * Display items in table
 */
function displayItems(items) {
    if (items.length === 0) {
        displayEmptyState();
        return;
    }

    itemsTableBody.innerHTML = items.map((item, index) => `
        <tr>
            <td class="no">${index + 1}</td>
            <td>${escapeHtml(item.name)}</td>
            <td>${escapeHtml(item.category)}</td>
            <td>${escapeHtml(item.location)}</td>
            <td class="quantity">${item.quantity}</td>
            <td class="price">${formatCurrency(item.unit_price)}</td>
            <td class="total-value">${formatCurrency(item.total_value)}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-sm btn-warning" onclick="openEditModal(${item.id})">Edit</button>
                    <button class="btn btn-sm btn-success" onclick="adjustStock(${item.id})">Stock</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteItem(${item.id})">Hapus</button>
                </div>
            </td>
        </tr>
    `).join('');
}

/**
 * Display empty state message
 */
function displayEmptyState() {
    itemsTableBody.innerHTML = `
        <tr class="empty-state">
            <td colspan="8" style="text-align: center; padding: 40px;">
                📭 Belum ada item. Tambahkan item baru terlebih dahulu.
            </td>
        </tr>
    `;
}

/**
 * Handle add item form submission
 */
async function handleAddItem(e) {
    e.preventDefault();

    const itemData = {
        name: document.getElementById('itemName').value.trim(),
        category: document.getElementById('itemCategory').value.trim(),
        location: document.getElementById('itemLocation').value.trim(),
        quantity: parseInt(document.getElementById('itemQuantity').value),
        unit_price: parseFloat(document.getElementById('itemPrice').value),
        description: document.getElementById('itemDescription').value.trim()
    };

    // Validation
    if (!itemData.name || !itemData.category || !itemData.location) {
        showAlert('Mohon isi semua field yang diperlukan', 'warning');
        return;
    }

    if (itemData.quantity < 0 || itemData.unit_price < 0) {
        showAlert('Jumlah dan harga tidak boleh negatif', 'warning');
        return;
    }

    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(itemData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Gagal menambah item');
        }

        showAlert('Item berhasil ditambahkan!', 'success');
        addItemForm.reset();
        loadItems();
        loadSummary();
    } catch (error) {
        console.error('Error adding item:', error);
        showAlert(error.message, 'error');
    }
}

/**
 * Open edit modal
 */
async function openEditModal(itemId) {
    try {
        const response = await fetch(`${API_BASE}/${itemId}`);
        if (!response.ok) throw new Error('Item not found');

        const item = await response.json();
        
        document.getElementById('editItemId').value = item.id;
        document.getElementById('editItemName').value = item.name;
        document.getElementById('editItemCategory').value = item.category;
        document.getElementById('editItemLocation').value = item.location;
        document.getElementById('editItemQuantity').value = item.quantity;
        document.getElementById('editItemPrice').value = item.unit_price;
        document.getElementById('editItemDescription').value = item.description || '';

        editModal.style.display = 'block';
    } catch (error) {
        console.error('Error opening edit modal:', error);
        showAlert('Gagal membuka form edit', 'error');
    }
}

/**
 * Close edit modal
 */
function closeEditModal() {
    editModal.style.display = 'none';
    editItemForm.reset();
}

/**
 * Close modal when clicking outside
 */
function closeEditModalOnClickOutside(event) {
    if (event.target === editModal) {
        closeEditModal();
    }
}

/**
 * Handle edit item form submission
 */
async function handleEditItem(e) {
    e.preventDefault();

    const itemId = document.getElementById('editItemId').value;
    const itemData = {
        name: document.getElementById('editItemName').value.trim(),
        category: document.getElementById('editItemCategory').value.trim(),
        location: document.getElementById('editItemLocation').value.trim(),
        quantity: parseInt(document.getElementById('editItemQuantity').value),
        unit_price: parseFloat(document.getElementById('editItemPrice').value),
        description: document.getElementById('editItemDescription').value.trim()
    };

    // Validation
    if (!itemData.name || !itemData.category || !itemData.location) {
        showAlert('Mohon isi semua field yang diperlukan', 'warning');
        return;
    }

    if (itemData.quantity < 0 || itemData.unit_price < 0) {
        showAlert('Jumlah dan harga tidak boleh negatif', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(itemData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Gagal mengubah item');
        }

        showAlert('Item berhasil diperbarui!', 'success');
        closeEditModal();
        loadItems();
        loadSummary();
    } catch (error) {
        console.error('Error editing item:', error);
        showAlert(error.message, 'error');
    }
}

/**
 * Adjust stock for an item
 */
async function adjustStock(itemId) {
    const amount = prompt('Masukkan jumlah perubahan (+ untuk tambah, - untuk kurang):');
    
    if (amount === null) return; // User canceled

    const parsedAmount = parseInt(amount);
    if (isNaN(parsedAmount)) {
        showAlert('Mohon masukkan angka yang valid', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/${itemId}/stock`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: parsedAmount })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Gagal mengubah stok');
        }

        showAlert(`Stok berhasil diubah sebesar ${parsedAmount}!`, 'success');
        loadItems();
        loadSummary();
    } catch (error) {
        console.error('Error adjusting stock:', error);
        showAlert(error.message, 'error');
    }
}

/**
 * Delete an item
 */
async function deleteItem(itemId) {
    if (!confirm('Apakah Anda yakin ingin menghapus item ini?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/${itemId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Gagal menghapus item');
        }

        showAlert('Item berhasil dihapus!', 'success');
        loadItems();
        loadSummary();
    } catch (error) {
        console.error('Error deleting item:', error);
        showAlert(error.message, 'error');
    }
}

/**
 * Handle search/filter
 */
async function handleSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        loadItems();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Search failed');

        const data = await response.json();
        const items = data.items || [];
        
        if (items.length === 0) {
            itemsTableBody.innerHTML = `
                <tr class="empty-state">
                    <td colspan="8" style="text-align: center; padding: 40px;">
                        🔍 Tidak ada hasil untuk "${escapeHtml(query)}"
                    </td>
                </tr>
            `;
            return;
        }

        displayItems(items);
    } catch (error) {
        console.error('Error searching:', error);
        showAlert('Gagal mencari item', 'error');
    }
}

/**
 * Utility: Format currency to Indonesian Rupiah
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

/**
 * Utility: Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Show alert toast
 */
function showAlert(message, type = 'info') {
    alertToast.textContent = message;
    alertToast.className = `alert-toast show ${type}`;
    
    setTimeout(() => {
        alertToast.classList.remove('show');
    }, 3000);
}
