document.addEventListener('DOMContentLoaded', function () {
  // Initialize Colors
  var initialColors = document.getElementById('editColorsInput');
  if (initialColors && typeof setupColorBoxes === 'function') {
    setupColorBoxes('editColorContainer', 'editColorsInput', initialColors.value);
  }

  // Initialize Sizes
  var initialSizes = document.getElementById('editSizesInput');
  if (initialSizes && typeof setupSizeBoxes === 'function') {
    setupSizeBoxes('editSizeContainer', 'editSizesInput', initialSizes.value);
  }

  // Initialize Main Image Preview
  var mainImgWrapper = document.getElementById('productImageWrapper');
  if (mainImgWrapper) {
    var initialData = document.getElementById('initialMainImage');
    if (initialData) {
      var mainImgUrl = initialData.getAttribute('data-url');
      if (mainImgUrl) {
        var addButton = mainImgWrapper.querySelector('.add-image-btn');
        if (addButton) addButton.style.display = 'none';

        var container = document.createElement('div');
        container.className = 'image-preview-container';

        var imgEl = document.createElement('img');
        imgEl.src = mainImgUrl;
        imgEl.alt = 'Current';
        imgEl.className = 'img-fluid w-100 h-100 preview-img-contain';
        container.appendChild(imgEl);

        var rmBtn = document.createElement('button');
        rmBtn.type = 'button';
        rmBtn.className = 'remove-btn';
        rmBtn.innerHTML = '<i class="fas fa-times"></i>';
        rmBtn.addEventListener('click', function() {
          window.removeImage(this, 'productImageWrapper', false);
        });
        container.appendChild(rmBtn);

        mainImgWrapper.appendChild(container);
      }
    }
  }

  // Initialize Gallery Previews
  var galleryWrapper = document.getElementById('editGalleryWrapper');
  if (galleryWrapper) {
    var galleryAddButton = galleryWrapper.querySelector('.add-image-btn');
    var galleryItems = document.querySelectorAll('#initialGallery .gallery-item-data');

    galleryItems.forEach(function (item) {
      var imgUrl = item.getAttribute('data-url');
      var imgId = item.getAttribute('data-id');
      if (!imgUrl) return;

      var container = document.createElement('div');
      container.className = 'image-preview-container';
      var delBtn = document.createElement('button');
      delBtn.type = 'button';
      delBtn.className = 'remove-btn';
      delBtn.innerHTML = '<i class="fas fa-times"></i>';
      delBtn.addEventListener('click', function() {
        window.removeGalleryImage(this, imgId);
      });

      container.innerHTML = '<img src="' + imgUrl + '" alt="Gallery" class="img-fluid w-100 h-100 preview-img-contain">';
      container.appendChild(delBtn);
      if (galleryAddButton) {
        galleryWrapper.insertBefore(container, galleryAddButton);
      } else {
        galleryWrapper.appendChild(container);
      }
    });
  }
});
