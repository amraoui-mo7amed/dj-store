document.addEventListener('DOMContentLoaded', function() {
    // Main image upload — click preview to trigger file input
    document.querySelectorAll('[data-trigger]').forEach(function(el) {
        el.addEventListener('click', function() {
            var input = document.getElementById(el.dataset.trigger);
            if (input) input.click();
        });
    });

    // Main image upload — preview on file select
    document.querySelectorAll('input[type="file"][data-preview]').forEach(function(input) {
        input.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                var display = document.getElementById(this.dataset.preview);
                var placeholder = document.querySelector('.csf-placeholder');

                reader.onload = function(e) {
                    display.src = e.target.result;
                    display.classList.remove('d-none');
                    if (placeholder) placeholder.style.display = 'none';
                };

                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // Custom select — toggle dropdown
    document.addEventListener('click', function(e) {
        var trigger = e.target.closest('.custom-select-trigger');
        if (trigger) {
            var wrapper = trigger.closest('.custom-select-wrapper');
            if (wrapper) {
                wrapper.classList.toggle('active');
            }
        }
    });

    // Custom select — pick option
    document.addEventListener('click', function(e) {
        var option = e.target.closest('.custom-option');
        if (option) {
            var wrapper = option.closest('.custom-select-wrapper');
            var triggerText = wrapper.querySelector('.trigger-text');
            var hiddenInput = wrapper.querySelector('input[type="hidden"]');

            wrapper.querySelectorAll('.custom-option').forEach(function(opt) {
                opt.classList.remove('selected');
            });
            option.classList.add('selected');

            triggerText.textContent = option.textContent.trim();
            hiddenInput.value = option.dataset.value;
            wrapper.classList.remove('active');

            hiddenInput.dispatchEvent(new Event('change'));
        }
    });

    // Close dropdown on outside click
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.custom-select-wrapper')) {
            document.querySelectorAll('.custom-select-wrapper').forEach(function(w) {
                w.classList.remove('active');
            });
        }
    });

    // Initialize size boxes
    setupSizeBoxes('createSizeContainer', 'createSizesInput');

    // Form submission with SweetAlert
    var form = document.querySelector('.create-stock-page');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var btn = form.querySelector('.csf-btn-primary');
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> جاري الحفظ...';

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value }
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'تم بنجاح',
                        text: data.message,
                        confirmButtonColor: '#ea580c',
                    }).then(function() {
                        window.location.href = data.redirect_url || '/dashboard/stock/';
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'خطأ',
                        text: data.errors ? data.errors.join('\n') : 'حدث خطأ غير متوقع',
                        confirmButtonColor: '#ea580c',
                    });
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-check-circle me-1"></i> حفظ المنتج ونشره';
                }
            })
            .catch(function() {
                Swal.fire({
                    icon: 'error',
                    title: 'خطأ',
                    text: 'حدث خطأ في الاتصال',
                    confirmButtonColor: '#ea580c',
                });
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-check-circle me-1"></i> حفظ المنتج ونشره';
            });
        });
    }
});
