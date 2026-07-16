document.addEventListener('DOMContentLoaded', () => {
    const page = document.querySelector('[data-product-page]');
    if (!page) return;

    const productPrice = parseFloat(page.dataset.productPrice);
    const qtyInput = document.getElementById('quantity');
    const totalDisplay = document.getElementById('finalTotal');
    const mobileTotalDisplays = document.querySelectorAll('.mobile-total');

    function updatePrice() {
        const total = (productPrice * parseInt(qtyInput.value)).toLocaleString('fr-DZ', { minimumFractionDigits: 2 });
        if (totalDisplay) totalDisplay.textContent = total;
        mobileTotalDisplays.forEach(el => el.textContent = total);
    }

    // Stepper buttons
    document.querySelectorAll('[data-qty-change]').forEach(btn => {
        btn.addEventListener('click', () => {
            const delta = parseInt(btn.dataset.qtyChange);
            let current = parseInt(qtyInput.value);
            let max = parseInt(qtyInput.max) || 999;
            if (current + delta >= 1 && current + delta <= max) {
                qtyInput.value = current + delta;
                updatePrice();
            }
        });
    });

    // Gallery thumbnails
    const mainImg = document.getElementById('mainImage');
    document.querySelectorAll('[data-gallery-thumb]').forEach(thumb => {
        thumb.addEventListener('click', () => {
            const url = thumb.dataset.galleryThumb;
            if (mainImg.src === url) return;

            mainImg.classList.add('fade-out');
            setTimeout(() => {
                mainImg.src = url;
                mainImg.classList.remove('fade-out');
            }, 200);

            document.querySelectorAll('[data-gallery-thumb]').forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        });
    });

    // Mobile description toggle
    const descToggle = document.querySelector('[data-desc-toggle]');
    if (descToggle) {
        descToggle.addEventListener('click', () => {
            const content = document.getElementById('mobileDesc');
            content.classList.toggle('active');
            descToggle.classList.toggle('active');
        });
    }

    // Custom Select Logic
    function closeAllCustomSelects() {
        document.querySelectorAll('.custom-select-wrapper.open').forEach(w => w.classList.remove('open'));
    }

    document.querySelectorAll('[data-custom-select-trigger]').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            const wrapper = trigger.closest('.custom-select-wrapper');
            const isOpen = wrapper.classList.contains('open');
            closeAllCustomSelects();
            if (!isOpen) wrapper.classList.add('open');
        });
    });

    document.querySelectorAll('[data-custom-option]').forEach(option => {
        option.addEventListener('click', () => {
            const wrapper = option.closest('.custom-select-wrapper');
            const trigger = wrapper.querySelector('.custom-select-trigger');
            const triggerText = trigger.querySelector('.trigger-text');
            const nativeSelectId = wrapper.dataset.nativeSelect;
            const nativeSelect = document.getElementById(nativeSelectId);

            triggerText.textContent = option.textContent.trim();
            nativeSelect.value = option.dataset.value;
            wrapper.classList.remove('open');

            wrapper.querySelectorAll('.custom-option').forEach(o => o.classList.remove('selected'));
            option.classList.add('selected');

            // Trigger change event for native select
            nativeSelect.dispatchEvent(new Event('change'));

            if (nativeSelectId === 'wilaya-dropdown') {
                const communeWrapper = document.querySelector('[data-native-select="commune-dropdown"]');
                const communeSelect = document.getElementById('commune-dropdown');
                const communeOptions = document.getElementById('commune-custom-options');
                const communeTriggerText = communeWrapper.querySelector('.trigger-text');

                communeTriggerText.textContent = 'جاري التحميل...';
                communeSelect.value = '';
                communeOptions.innerHTML = '<div class="custom-option">جاري التحميل...</div>';

                fetch(`/get-communes/${nativeSelect.value}/`)
                    .then(r => r.json())
                    .then(data => {
                        communeOptions.innerHTML = '';
                        communeSelect.innerHTML = '<option value="" selected disabled>البلدية</option>';
                        communeTriggerText.textContent = 'اختر البلدية';

                        data.communes.forEach(c => {
                            // Add to native select
                            const nativeOpt = document.createElement('option');
                            nativeOpt.value = c.commune_name;
                            nativeOpt.textContent = c.commune_name;
                            communeSelect.appendChild(nativeOpt);

                            // Add to custom dropdown
                            const opt = document.createElement('div');
                            opt.className = 'custom-option';
                            opt.dataset.value = c.commune_name;
                            opt.dataset.customOption = '';
                            opt.textContent = c.commune_name;
                            opt.addEventListener('click', () => {
                                communeTriggerText.textContent = opt.textContent;
                                communeSelect.value = opt.dataset.value;
                                communeWrapper.classList.remove('open');
                                communeOptions.querySelectorAll('.custom-option').forEach(o => o.classList.remove('selected'));
                                opt.classList.add('selected');
                                communeSelect.dispatchEvent(new Event('change'));
                            });
                            communeOptions.appendChild(opt);
                        });
                    });
            }
        });
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-select-wrapper')) {
            closeAllCustomSelects();
        }
    });

    // Variant Selectors
    document.querySelectorAll('[data-variant-pill]').forEach(pill => {
        pill.addEventListener('click', () => {
            const group = pill.closest('.pill-options');
            group.querySelectorAll('[data-variant-pill]').forEach(i => i.classList.remove('selected'));
            pill.classList.add('selected');
            const inputId = group.id === 'sizeSelector' ? 'selected_size_input' : '';
            if (inputId) document.getElementById(inputId).value = pill.dataset.value;
        });
    });

    document.querySelectorAll('[data-color-option]').forEach(dot => {
        dot.addEventListener('click', () => {
            const group = dot.closest('.color-options');
            group.querySelectorAll('[data-color-option]').forEach(i => i.classList.remove('selected'));
            dot.classList.add('selected');
            document.getElementById('selected_color_input').value = dot.dataset.value;
        });
    });

    // Sticky Bar Logic
    const stickyBar = document.getElementById('stickyBar');
    if (stickyBar) {
        const updateStickyBar = () => {
            const form = document.getElementById('premiumOrderForm');
            if (!form) return;
            const formRect = form.getBoundingClientRect();
            // Show bar if we scrolled past 500px AND the form is not fully in view
            if (window.scrollY > 500 && formRect.top > window.innerHeight) {
                stickyBar.classList.add('visible');
            } else {
                stickyBar.classList.remove('visible');
            }
        };
        window.addEventListener('scroll', updateStickyBar);
        updateStickyBar();
    }

    document.querySelector('[data-scroll-to-form]')?.addEventListener('click', () => {
        document.getElementById('premiumOrderForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    // Form Submission
    const orderForm = document.getElementById('premiumOrderForm');
    if (orderForm) {
        orderForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Basic Validation
            const wilayaInput = document.getElementById('wilaya-dropdown');
            const communeInput = document.getElementById('commune-dropdown');
            const sizeInput = document.getElementById('selected_size_input');
            const colorInput = document.getElementById('selected_color_input');

            if (!wilayaInput.value) {
                Swal.fire({ icon: 'warning', title: 'تنبيه', text: 'يرجى اختيار الولاية' });
                return;
            }
            if (!communeInput.value) {
                Swal.fire({ icon: 'warning', title: 'تنبيه', text: 'يرجى اختيار البلدية' });
                return;
            }
            if (sizeInput && !sizeInput.value) {
                Swal.fire({ icon: 'warning', title: 'تنبيه', text: 'يرجى اختيار المقاس المطلوب' });
                return;
            }
            if (colorInput && !colorInput.value) {
                Swal.fire({ icon: 'warning', title: 'تنبيه', text: 'يرجى اختيار اللون المفضل' });
                return;
            }

            const submitBtn = this.querySelector('.cta-order-btn');
            const btnMain = submitBtn.querySelector('.btn-main');
            const loader = submitBtn.querySelector('.btn-loader');

            submitBtn.disabled = true;
            btnMain.classList.add('d-none');
            loader.classList.remove('d-none');

            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'تم إرسال طلبك بنجاح!',
                        text: 'شكرًا لثقتك بنا، سيتصل بك فريقنا لتأكيد الطلب خلال دقائق.',
                        confirmButtonText: 'عرض تفاصيل الطلب',
                        confirmButtonColor: '#1B4332'
                    }).then(() => window.location.href = '/order/' + data.ref_code + '/confirmation/');
                } else {
                    throw new Error(data.errors ? data.errors.join('\n') : 'فشل إرسال الطلب');
                }
            })
            .catch(err => {
                submitBtn.disabled = false;
                btnMain.classList.remove('d-none');
                loader.classList.add('d-none');
                Swal.fire({ icon: 'error', title: 'خطأ', text: err.message });
            });
        });
    }
});
