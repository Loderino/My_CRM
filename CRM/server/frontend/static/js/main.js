function showWidgetSelector() {
    document.getElementById('widget-modal').style.display = 'flex';
}

function hideWidgetSelector() {
    document.getElementById('widget-modal').style.display = 'none';
}

function addWidget(type) {
    // Здесь будет логика добавления виджета
    console.log('Добавить виджет:', type);
    hideWidgetSelector();
}

function removeWidget(button) {
    if (confirm('Удалить виджет?')) {
        button.closest('.widget').remove();
    }
}

// Закрытие модалки по клику вне её
window.onclick = function(event) {
    const modal = document.getElementById('widget-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}