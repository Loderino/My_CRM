/**
 * Скрипты для страницы списка заказов
 */

// Клик по строке заказа
document.querySelectorAll('.order-row').forEach(row => {
    row.addEventListener('click', function(e) {
        if (e.target.closest('.btn-icon, .tool-badge, .client-link')) {
            return;
        }
        const orderId = this.dataset.orderId;
        window.location.href = `/orders/${orderId}`;
    });
});

// Поиск
function applySearch() {
    const search = document.getElementById('searchInput').value;
    const perPage = document.getElementById('perPageSelect').value;
    const url = new URL(window.location.href);
    url.searchParams.set('page', '1');
    url.searchParams.set('per_page', perPage);
    if (search) {
        url.searchParams.set('search', search);
    } else {
        url.searchParams.delete('search');
    }
    window.location.href = url.toString();
}

// Поиск по Enter
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            applySearch();
        }
    });
}

// Пагинация
function changePerPage(value) {
    const url = new URL(window.location.href);
    url.searchParams.set('per_page', value);
    url.searchParams.set('page', '1');
    window.location.href = url.toString();
}