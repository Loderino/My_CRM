/**
 * Скрипты для страницы списка клиентов
 */

// Клик по строке клиента
document.querySelectorAll('.client-row').forEach(row => {
    row.addEventListener('click', function(e) {
        // Не переходить, если клик по кнопке или бейджу
        if (e.target.closest('.btn-icon, .contact-badge, .note-indicator')) {
            return;
        }
        const clientId = this.dataset.clientId;
        window.location.href = `/clients/${clientId}`;
    });
});

// Поиск по кнопке
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

// Изменение количества на странице
function changePerPage(value) {
    const url = new URL(window.location.href);
    url.searchParams.set('per_page', value);
    url.searchParams.set('page', '1');
    window.location.href = url.toString();
}

// Подтверждение удаления (если есть кнопка удаления)
function confirmDelete(clientName, clientId) {
    if (confirm(`Удалить клиента "${clientName}"? Это действие нельзя отменить.`)) {
        window.location.href = `/clients/${clientId}/delete`;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Можно добавить логи, если нужно
    // console.log('Страница клиентов загружена');
});