// Store for multiple uploads to accumulate files across multiple selections
window.uploaderFiles = {};

// Image upload component — click add button to trigger file input (delegated)
document.addEventListener('click', function(e) {
    var btn = e.target.closest('.add-image-btn[data-for]');
    if (btn) {
        var input = document.getElementById(btn.dataset.for);
        if (input) input.click();
    }
});

// Image upload component — handle file selection (delegated)
document.addEventListener('change', function(e) {
    var input = e.target.closest('input[type="file"][data-wrapper]');
    if (input) {
        var multiple = input.dataset.multiple === 'true';
        window.handleImageUpload(input, input.dataset.wrapper, multiple);
    }
});

window.handleImageUpload = function(input, wrapperId, multiple = false) {
    const wrapper = document.getElementById(wrapperId);
    if (!wrapper || !input.files.length) return;
    
    const addButton = wrapper.querySelector('.add-image-btn');
    const newFiles = Array.from(input.files);
    
    if (!multiple) {
        // Single mode
        window.uploaderFiles[wrapperId] = [newFiles[0]];
        const existingPreviews = wrapper.querySelectorAll('.image-preview-container');
        existingPreviews.forEach(p => p.remove());
        if (addButton) addButton.style.display = 'none';
    } else {
        // Multiple mode
        if (!window.uploaderFiles[wrapperId]) window.uploaderFiles[wrapperId] = [];
        newFiles.forEach(file => window.uploaderFiles[wrapperId].push(file));
    }
    
    // Create previews
    const filesToPreview = !multiple ? [newFiles[0]] : newFiles;
    
    filesToPreview.forEach(file => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const container = document.createElement('div');
            container.className = 'image-preview-container';
            if (!multiple) container.classList.add('w-100');

            var img = document.createElement('img');
            img.src = e.target.result;
            img.alt = 'Preview';
            img.className = 'img-fluid w-100 h-100';
            img.style.objectFit = 'contain';
            container.appendChild(img);

            var rmBtn = document.createElement('button');
            rmBtn.type = 'button';
            rmBtn.className = 'remove-btn';
            rmBtn.innerHTML = '<i class="fas fa-times"></i>';
            rmBtn.addEventListener('click', function() {
                window.removeImage(this, wrapperId, multiple);
            });
            container.appendChild(rmBtn);

            if (multiple) {
                wrapper.insertBefore(container, addButton);
            } else {
                wrapper.appendChild(container);
            }
        };
        reader.readAsDataURL(file);
    });

    syncInput(input, wrapperId);
    
    // For gallery, we clear the internal input value so the same file can be picked again to trigger onchange
    // BUT we must only do this after we have stored the files elsewhere or if we handle it during submit
}

window.removeImage = function(btn, wrapperId, multiple) {
    const wrapper = document.getElementById(wrapperId);
    const addButton = wrapper.querySelector('.add-image-btn');
    const container = btn.parentElement;
    
    if (multiple && window.uploaderFiles[wrapperId]) {
        const previews = Array.from(wrapper.querySelectorAll('.image-preview-container'));
        const actualIndex = previews.indexOf(container);
        if (actualIndex > -1) {
            window.uploaderFiles[wrapperId].splice(actualIndex, 1);
        }
    } else {
        window.uploaderFiles[wrapperId] = [];
    }
    
    container.remove();
    
    if (!multiple && addButton) {
        addButton.style.display = 'flex';
    }
    
    const input = wrapper.closest('.image-upload-section').querySelector('input[type="file"]');
    syncInput(input, wrapperId);
}

function syncInput(input, wrapperId) {
    if (!window.uploaderFiles[wrapperId] || !input) return;
    
    const dt = new DataTransfer();
    window.uploaderFiles[wrapperId].forEach(file => dt.items.add(file));
    input.files = dt.files;
}
