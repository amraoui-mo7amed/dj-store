from django.db import models
from django.utils import timezone
from django.db import models, transaction
from django.utils import timezone
from django.db.models import F, Sum, FloatField
import uuid
from django.contrib.auth import get_user_model
from utils import get_algerian_wilayas
from django.utils.translation import gettext_lazy as _

wilayas = get_algerian_wilayas()
wilayas_choices = [(code, name) for code, name in wilayas]

userModel = get_user_model()

CATEGORY_CHOICES = [
        ('clothing', 'ملابس'),
        ('electronics', 'إلكترونيات'),
        ('home', 'منزلية'),
        ('kitchen', 'مطبخ'),
        ('health_beauty', 'صحة وجمال'),
        ('children', 'أطفال'),
        ('books', 'كتب'),
        ('sports', 'رياضة'),
    ]


class Stock(models.Model):
    product_image = models.ImageField(upload_to='stock_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # selling price
    sales_count = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='clothing')
    uuid = models.CharField(max_length=6, unique=True, default=uuid.uuid4().hex[:6], editable=False)
    sizes = models.CharField(max_length=255, null=True, blank=True, help_text="Comma-separated sizes (e.g. S,M,L,XL)")
    colors = models.CharField(max_length=255, null=True, blank=True, help_text="Comma-separated colors (e.g. #FF0000,#0000FF)")
    
    def __str__(self):
        return f"Stock: {self.product_name}"
    
    def get_sizes_list(self):
        return [s.strip() for s in self.sizes.split(',')] if self.sizes else []

    def get_colors_list(self):
        return [c.strip() for c in self.colors.split(',')] if self.colors else []

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4().hex[:6]
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='stock_gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Gallery for {self.product.product_name}"
    
class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الإنتظار'),
        ('confirmed', 'تم التأكيد'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('cancelled', 'تم الإلغاء'),
    ]
    name = models.CharField(max_length=150, default='')
    phone = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=150, default='')
    wilaya = models.CharField(max_length=150, default='')
    commune = models.CharField(max_length=150, default='')
    product = models.ForeignKey("Stock", on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=0)
    selected_size = models.CharField(max_length=50, null=True, blank=True)
    selected_color = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ref_code = models.CharField(max_length=8, editable=False, default='')
    
    def __str__(self):
        return f"Order {self.ref_code}: {self.quantity} x {self.product.product_name}"
    
    @property
    def get_wilaya_name(self):
        wilaya_dict = dict(wilayas_choices)
        return wilaya_dict.get(self.wilaya)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.ref_code = uuid.uuid4().hex[:8].upper()
            with transaction.atomic():
                Stock.objects.filter(pk=self.product.pk).update(
                    quantity=F('quantity') - self.quantity,
                    sales_count=F('sales_count') + 1
                )
                super().save(*args, **kwargs)
                self.product.refresh_from_db()
        else:
            super().save(*args, **kwargs)


class userNotification(models.Model):
    user = models.ForeignKey(userModel, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('المستخدم'))
    message = models.TextField(_('الرسالة'))
    url = models.CharField(_('الرابط'), max_length=500, blank=True)
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    is_read = models.BooleanField(_('مقروءة'), default=False)
    icon = models.CharField()

    class Meta:
        verbose_name = _('إشعار المستخدم')
        verbose_name_plural = _('إشعارات المستخدمين')
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."
    
    
class FeedBack(models.Model):
    picture = models.ImageField(upload_to='feedback/pictures', null=True, blank=True)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Profile(models.Model):
    user = models.OneToOneField(userModel, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(_("رقم الهاتف"), max_length=20, blank=True)
    avatar = models.ImageField(_("الصورة الشخصية"), upload_to='profiles/avatars/', blank=True, null=True)
    bio = models.TextField(_("نبذة"), blank=True)
    wilaya = models.CharField(_("الولاية"), max_length=100, blank=True, choices=wilayas_choices)

    def __str__(self):
        return f"ملف {self.user.username}"
