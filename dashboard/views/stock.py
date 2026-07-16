from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from dashboard.models import Stock, ProductImage, CATEGORY_CHOICES
from django.core.paginator import Paginator
from dashboard.views.genric import BaseDeleteView

AVAILABLE_SIZES = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

AVAILABLE_COLORS = [
    ('#000000', 'Black'),
    ('#FFFFFF', 'White'),
    ('#FF0000', 'Red'),
    ('#00FF00', 'Green'),
    ('#0000FF', 'Blue'),
    ('#FFFF00', 'Yellow'),
    ('#FFA500', 'Orange'),
    ('#800080', 'Purple'),
    ('#FFC0CB', 'Pink'),
    ('#A52A2A', 'Brown'),
    ('#808080', 'Grey'),
]

@login_required
def stock_list(request):
    """List all stock items with pagination"""
    
    paginator = Paginator(Stock.objects.all().order_by('-created_at'), 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(request, "stock/stock_list.html", {
        "page_obj": page_obj,
        "category_choices": CATEGORY_CHOICES,
        "available_colors": AVAILABLE_COLORS,
    })

@login_required
@csrf_exempt
def create_stock(request):
    """Handle both rendering the create page (GET) and creating a new stock item (POST)"""
    if request.method == "POST":
        product_image = request.FILES.get("product_image")
        gallery_images = request.FILES.getlist("gallery")
        product_name = request.POST.get("product_name")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        description = request.POST.get("description")
        sizes = request.POST.get("sizes", "")
        colors = request.POST.get("colors", "") # Expecting comma separated hex codes
        errors = []

        if category not in [choice[0] for choice in CATEGORY_CHOICES]:
            errors.append("الفئة المختارة غير صالحة.")
        
        if not product_name or not product_name.strip():
            errors.append("اسم المنتج مطلوب.")

        if not description or not description.strip():
            errors.append("الوصف مطلوب.")

        try:
            quantity = int(quantity) if quantity else 0
            if quantity < 0:
                errors.append("الكمية يجب أن تكون موجبة.")
        except (ValueError, TypeError):
            errors.append("الكمية غير صالحة.")

        if not product_image:
            errors.append("صورة المنتج الرئيسية مطلوبة.")

        try:
            price = float(price) if price else 0.0
            if price < 0:
                errors.append("سعر البيع يجب أن يكون موجباً.")
        except (ValueError, TypeError):
            errors.append("سعر البيع غير صالح.")

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        # Create stock item
        stock = Stock.objects.create(
            product_name=product_name.strip(),
            description=description.strip(),
            quantity=quantity,
            price=price,
            category=category,
            product_image=product_image,
            sizes=sizes,
            colors=colors,
        )

        # Save gallery images
        for img in gallery_images:
            ProductImage.objects.create(product=stock, image=img)
        
        return JsonResponse({
            "success": True,
            "redirect_url": reverse("dash:stock_list"),
            "message": "تم إنشاء المنتج بنجاح."
        })
    
    return render(request, "stock/stock_create.html", {
        "category_choices": CATEGORY_CHOICES,
        "available_colors": AVAILABLE_COLORS,
        "predefined_sizes": AVAILABLE_SIZES,
    })

@login_required
@csrf_exempt
def edit_stock(request, pk):
    """Handle both rendering the edit page (GET) and updating a stock item (POST)"""
    stock = get_object_or_404(Stock, pk=pk)
    
    if request.method == "POST":
        product_image = request.FILES.get("product_image")
        gallery_images = request.FILES.getlist("gallery")
        deleted_gallery_ids = request.POST.get("deleted_gallery_images", "").split(",")
        
        product_name = request.POST.get("product_name")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        description = request.POST.get("description")
        sizes = request.POST.get("sizes", "")
        colors = request.POST.get("colors", "")
        errors = []

        if category not in [choice[0] for choice in CATEGORY_CHOICES]:
            errors.append("الفئة المختارة غير صالحة.")
        
        if not product_name or not product_name.strip():
            errors.append("اسم المنتج مطلوب.")

        if not description or not description.strip():
            errors.append("الوصف مطلوب.")

        try:
            quantity = int(quantity) if quantity else 0
            if quantity < 0:
                errors.append("الكمية يجب أن تكون موجبة.")
        except (ValueError, TypeError):
            errors.append("الكمية غير صالحة.")

        try:
            price = float(price) if price else 0.0
            if price < 0:
                errors.append("سعر البيع يجب أن يكون موجباً.")
        except (ValueError, TypeError):
            errors.append("سعر البيع غير صالح.")

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        # Update stock item
        stock.product_name = product_name.strip()
        stock.description = description.strip()
        stock.quantity = quantity
        stock.price = price
        stock.category = category
        stock.sizes = sizes
        stock.colors = colors
        if product_image:
            stock.product_image = product_image
        stock.save()

        # Handle gallery deletions
        if deleted_gallery_ids:
            ProductImage.objects.filter(product=stock, id__in=[id for id in deleted_gallery_ids if id]).delete()

        # Handle gallery additions
        for img in gallery_images:
            ProductImage.objects.create(product=stock, image=img)
        
        return JsonResponse({
            "success": True,
            "redirect_url": reverse("dash:stock_list"),
            "message": "تم تحديث المنتج بنجاح."
        })
    
    return render(request, "stock/stock_edit.html", {
        "product": stock,
        "category_choices": CATEGORY_CHOICES,
        "available_colors": AVAILABLE_COLORS,
        "predefined_sizes": AVAILABLE_SIZES,
    })


@login_required
def get_product_gallery(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    images = stock.gallery.all()
    data = {
        "images": [{"id": img.id, "url": img.image.url} for img in images]
    }
    return JsonResponse(data)

class delete_stock(BaseDeleteView):
    model = Stock