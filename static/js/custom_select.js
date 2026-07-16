function initCustomSelects() {
    document.querySelectorAll('.custom-select-wrapper').forEach(function(wrapper) {
        var display = wrapper.querySelector('.custom-select-display');
        var list = wrapper.querySelector('.custom-select-list');

        if (!display || !list) return;

        display.addEventListener('click', function(e) {
            e.stopPropagation();
            list.classList.toggle('show');
            display.classList.toggle('active');
        });

        list.querySelectorAll('li').forEach(function(item) {
            item.addEventListener('click', function(e) {
                e.stopPropagation();
                var hiddenInput = wrapper.querySelector('input[type="hidden"]');
                display.textContent = item.textContent;
                if (hiddenInput) hiddenInput.value = item.dataset.value;
                list.classList.remove('show');
                display.classList.remove('active');
                var arrow = document.createElement('span');
                arrow.className = 'arrow';
                arrow.innerHTML = '<i class="fas fa-caret-down"></i>';
                display.appendChild(arrow);
            });
        });
    });
}

document.addEventListener('click', function() {
    document.querySelectorAll('.custom-select-list.show').forEach(function(l) {
        l.classList.remove('show');
    });
    document.querySelectorAll('.custom-select-display.active').forEach(function(d) {
        d.classList.remove('active');
    });
});

document.addEventListener('DOMContentLoaded', initCustomSelects);
