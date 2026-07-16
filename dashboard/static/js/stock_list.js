let deletedGalleryImages = [];

function previewImage(input, previewId, containerClass) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            let existingPreview = document.getElementById(previewId);
            if (existingPreview) {
                existingPreview.src = e.target.result;
                existingPreview.style.display = 'block';
                
                let container = input.closest('.' + containerClass);
                if (container) {
                    let icon = container.querySelector('.icon');
                    let text = container.querySelector('.text');
                    if (icon) icon.style.display = 'none';
                    if (text) text.style.display = 'none';
                }
            }
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function setupSizeBoxes(containerId, inputId, initialSizes = '') {
    const container = document.getElementById(containerId);
    const input = document.getElementById(inputId);
    if (!container || !input) return;

    const selectedSizes = new Set(initialSizes ? initialSizes.split(',').map(s => s.trim()) : []);

    container.querySelectorAll('.size-option').forEach(option => {
        const size = option.dataset.size;
        if (selectedSizes.has(size)) {
            option.classList.add('selected');
        }

        option.addEventListener('click', () => {
            if (option.classList.contains('selected')) {
                option.classList.remove('selected');
                selectedSizes.delete(size);
            } else {
                option.classList.add('selected');
                selectedSizes.add(size);
            }
            input.value = Array.from(selectedSizes).join(',');
        });
    });
}

function setupColorBoxes(containerId, inputId, initialColors = '') {
    const container = document.getElementById(containerId);
    const input = document.getElementById(inputId);
    if (!container || !input) return;

    // Handle spaces in comma-separated list
    const selectedColors = new Set(initialColors ? initialColors.split(',').map(c => c.trim()) : []);

    container.querySelectorAll('.color-option').forEach(option => {
        const color = option.dataset.color;
        if (selectedColors.has(color)) {
            option.classList.add('selected');
        }

        option.addEventListener('click', () => {
            if (option.classList.contains('selected')) {
                option.classList.remove('selected');
                selectedColors.delete(color);
            } else {
                option.classList.add('selected');
                selectedColors.add(color);
            }
            input.value = Array.from(selectedColors).join(',');
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Basic file previews
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            previewImage(this, 'product_image_preview', 'custum-file-upload');
        });
    }

    const editFileInput = document.getElementById('edit_file');
    if (editFileInput) {
        editFileInput.addEventListener('change', function() {
            previewImage(this, 'edit_image_preview', 'custum-file-upload');
        });
    }

    // Initialize Color Boxes for Create
    setupColorBoxes('createColorContainer', 'createColorsInput');

    window.removeGalleryImage = function(btn, imageId) {
        deletedGalleryImages.push(imageId);
        btn.parentElement.remove();
    };

    // Handle Form Submissions
    const forms = ['createProductForm', 'editProductForm'];
    forms.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                
                // Add deleted gallery images
                if (formId === 'editProductForm') {
                    formData.append('deleted_gallery_images', deletedGalleryImages.join(','));
                }
                
                fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            icon: 'success',
                            title: 'نجاح',
                            text: data.message,
                        }).then(() => {
                            if (data.redirect_url) {
                                window.location.href = data.redirect_url;
                            } else {
                                window.location.reload();
                            }
                        });
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'خطأ',
                            text: data.errors.join('\n'),
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire({
                        icon: 'error',
                        title: 'خطأ',
                        text: 'حدث خطأ غير متوقع',
                    });
                });
            });
        }
    });
});
