// Navbar scroll effect
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const navbarBrand = document.querySelector('.navbar-brand');
    
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('bg-light');
            navLinks.forEach(link => {
                link.classList.add('text-dark');
                link.classList.remove('text-light');
            });
            navbarBrand.classList.add('text-dark');
            navbarBrand.classList.remove('text-light');
        } else {
            navbar.classList.remove('bg-light');
            navLinks.forEach(link => {
                link.classList.remove('text-dark');
                link.classList.add('text-light');
            });
            navbarBrand.classList.remove('text-dark');
            navbarBrand.classList.add('text-light');
        }
    }
});


// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Dealing with forms
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.form');
    const errorList = document.querySelector('#errorList');

    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(form);
            errorList.innerHTML = ''; // Clear previous errors

            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                const data = await response.json();

                if (data.success) {
                    if (data.message) {
                        const li = document.createElement('li');
                        li.textContent = data.message;
                        li.classList.add('alert', 'alert-success', 'mb-2');
                        li.setAttribute('data-aos', 'fade-up');
                        errorList.appendChild(li);
                    }
                    if (data.redirect_url) {
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 400); // let the animation finish
                    }
                } else {
                    if (data.errors) {
                        const renderMsg = (msg, cls = 'alert-warning') => {
                            const li = document.createElement('li');
                            li.textContent = msg;
                            li.classList.add('alert', 'alert-warning', 'mb-2');
                            li.setAttribute('data-aos', 'fade-left');
                            errorList.appendChild(li);
                        };

                        if (Array.isArray(data.errors)) {
                            data.errors.forEach(renderMsg);
                        } else if (typeof data.errors === 'object') {
                            Object.values(data.errors)
                                .flat()
                                .forEach(m => renderMsg(m));
                        }
                    }
                }
            } catch (error) {
                const li = document.createElement('li');
                li.textContent = 'An unexpected error occurred. Please try again.';
                li.classList.add('alert', 'alert-danger', 'mb-2');
                li.setAttribute('data-aos', 'fade-up');
                errorList.appendChild(li);
                console.error('Form submission error:', error);
            }
        });
    });
});

// ── Join Modal ──
document.addEventListener('DOMContentLoaded', function() {
    // File upload click trigger
    document.querySelectorAll('.join-file-upload[data-for]').forEach(function(el) {
        el.addEventListener('click', function() {
            var input = document.getElementById(this.dataset.for);
            if (input) input.click();
        });
    });

    // File upload show filename
    document.querySelectorAll('input[type="file"][data-filename]').forEach(function(input) {
        input.addEventListener('change', function() {
            var el = document.getElementById(this.dataset.filename);
            if (el && this.files && this.files[0]) {
                el.textContent = this.files[0].name;
            }
        });
    });
    // Form submit trigger via data-submit-form
    document.querySelectorAll('[data-submit-form]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var form = document.getElementById(this.dataset.submitForm);
            if (form) form.submit();
        });
    });

    const joinForm = document.getElementById('joinForm');
    const joinErrors = document.getElementById('joinErrors');

    if (joinForm) {
        joinForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            joinErrors.classList.add('d-none');
            joinErrors.innerHTML = '';

            const formData = new FormData(joinForm);

            try {
                const response = await fetch(joinForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });

                const data = await response.json();

                if (data.success) {
                    const modalEl = document.getElementById('joinModal');
                    const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                    modal.hide();
                    joinForm.reset();
                    document.querySelectorAll('.join-file-name').forEach(el => el.textContent = '');
                    if (typeof Swal !== 'undefined') {
                        Swal.fire({
                            icon: 'success',
                            title: 'تم بنجاح',
                            text: data.message,
                            confirmButtonColor: '#F48C06',
                        });
                    }
                } else {
                    if (data.errors && data.errors.length) {
                        const ul = document.createElement('ul');
                        ul.className = 'mb-0';
                        data.errors.forEach(function(msg) {
                            const li = document.createElement('li');
                            li.textContent = msg;
                            ul.appendChild(li);
                        });
                        joinErrors.appendChild(ul);
                        joinErrors.classList.remove('d-none');
                    }
                }
            } catch (error) {
                console.error('Join form error:', error);
            }
        });
    }
});