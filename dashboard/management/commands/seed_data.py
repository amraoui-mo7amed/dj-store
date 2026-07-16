from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from dashboard.models import Stock

class Command(BaseCommand):
    help = "Seed sample products"

    def handle(self, *args, **options):
        now = timezone.now()

        # ── Products ──
        products_data = [
            {"product_name": "خيمة تخييم 4 مواسم", "category": "clothing", "price": 25000, "quantity": 15, "description": "خيمة مقاومة للرياح والأمطار تتسع لـ 4 أشخاص"},
            {"product_name": "حقيبة ظهر 60 لتر", "category": "clothing", "price": 12000, "quantity": 25, "description": "حقيبة ظهر متعددة الجيوب مقاومة للماء"},
            {"product_name": "كيس نوم حراري", "category": "home", "price": 8500, "quantity": 30, "description": "كيس نوم مناسب للأجواء الباردة حتى -5 درجات"},
            {"product_name": "موقد غاز محمول", "category": "kitchen", "price": 4500, "quantity": 20, "description": "موقد غاز صغير للطهي في الرحلات"},
            {"product_name": "مصباح أمامي LED", "category": "electronics", "price": 3200, "quantity": 40, "description": "مصباح أمامي قابل لإعادة الشحن بقوة 500 لومن"},
        ]

        created_products = 0
        for p in products_data:
            _, was_created = Stock.objects.get_or_create(
                product_name=p["product_name"],
                defaults={
                    "category": p["category"],
                    "price": p["price"],
                    "quantity": p["quantity"],
                    "description": p["description"],
                }
            )
            if was_created:
                created_products += 1

        self.stdout.write(self.style.SUCCESS(f"✓ تم إنشاء {created_products} منتجات"))
        self.stdout.write(self.style.SUCCESS("تم البذر بنجاح"))
