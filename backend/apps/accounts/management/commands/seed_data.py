from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from apps.accounts.models import (
    Achievement,
    Address,
    MembershipLevel,
    Profile,
    User,
    UserMembership,
    Wallet,
)
from apps.blog.models import BlogCategory, BlogPost
from apps.catalog.models import Brand, Category, Color, Product, ProductSpecification, ProductVariant, RAMOption, StorageOption
from apps.cms.models import Banner, CustomerReview, FAQ, Menu, MenuItem, Page, Partner, SiteSettings
from apps.inventory.models import InventoryItem, Supplier, Warehouse
from apps.notifications.models import NotificationTemplate
from apps.orders.models import City, Province, ShippingMethod
from apps.promotions.models import Coupon, FlashSale, FlashSaleProduct, SpecialOffer
from apps.reviews.models import Review
from apps.search.models import PopularSearch
from apps.support.models import TicketDepartment


class Command(BaseCommand):
    help = "Seed the database with comprehensive sample data for PhonyShop"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing seed-related data before seeding",
        )

    def handle(self, *args, **options):
        self.stdout.write("Seeding PhonyShop database...")

        self._seed_site_settings()
        self._seed_membership_levels()
        self._seed_provinces_cities()
        self._seed_shipping_methods()
        self._seed_catalog()
        self._seed_promotions()
        self._seed_cms()
        self._seed_blog()
        self._seed_support()
        self._seed_achievements()
        self._seed_notification_templates()
        self._seed_search()
        self._seed_users()
        self._seed_inventory()
        self._seed_reviews()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))

    def _seed_site_settings(self):
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "site_name": "PhonyShop",
                "site_name_fa": "فونی‌شاپ",
                "phone": "+982112345678",
                "email": "info@phonyshop.com",
                "address": "Tehran, Valiasr St.",
                "address_fa": "تهران، خیابان ولیعصر",
                "tax_rate": Decimal("9"),
                "currency": "IRR",
                "currency_symbol": "تومان",
                "free_shipping_threshold": Decimal("5000000"),
            },
        )
        self.stdout.write("  Site settings created")

    def _seed_membership_levels(self):
        levels = [
            ("bronze", 0, Decimal("1"), Decimal("0")),
            ("silver", 500, Decimal("2"), Decimal("2")),
            ("gold", 2000, Decimal("3"), Decimal("5")),
            ("diamond", 5000, Decimal("5"), Decimal("8")),
            ("vip", 10000, Decimal("7"), Decimal("10")),
        ]
        for name, min_points, cashback, discount in levels:
            MembershipLevel.objects.get_or_create(
                name=name,
                defaults={
                    "min_points": min_points,
                    "cashback_percent": cashback,
                    "discount_percent": discount,
                    "color": "#CD7F32" if name == "bronze" else "#C0C0C0",
                },
            )
        self.stdout.write("  Membership levels created")

    def _seed_provinces_cities(self):
        provinces = [
            ("Tehran", "تهران", "THR", ["Tehran", "Shemiranat"]),
            ("Isfahan", "اصفهان", "ISF", ["Isfahan", "Kashan"]),
            ("Fars", "فارس", "FRS", ["Shiraz", "Marvdasht"]),
        ]
        for name, name_fa, code, cities in provinces:
            province, _ = Province.objects.get_or_create(
                code=code,
                defaults={"name": name, "name_fa": name_fa},
            )
            for city_name in cities:
                City.objects.get_or_create(
                    province=province,
                    name=city_name,
                    defaults={"name_fa": city_name},
                )
        self.stdout.write("  Provinces and cities created")

    def _seed_shipping_methods(self):
        ShippingMethod.objects.get_or_create(
            name="Standard Delivery",
            defaults={
                "name_fa": "ارسال عادی",
                "base_cost": Decimal("150000"),
                "estimated_days_min": 2,
                "estimated_days_max": 5,
                "is_free_above": Decimal("5000000"),
            },
        )
        ShippingMethod.objects.get_or_create(
            name="Express Delivery",
            defaults={
                "name_fa": "ارسال سریع",
                "base_cost": Decimal("300000"),
                "estimated_days_min": 1,
                "estimated_days_max": 2,
            },
        )
        self.stdout.write("  Shipping methods created")

    def _seed_catalog(self):
        brands_data = [
            ("Apple", "اپل"),
            ("Samsung", "سامسونگ"),
            ("Xiaomi", "شیائومی"),
            ("Google", "گوگل"),
        ]
        brands = {}
        for name, name_fa in brands_data:
            brand, _ = Brand.objects.get_or_create(
                name=name,
                defaults={"name_fa": name_fa, "slug": slugify(name)},
            )
            brands[name] = brand

        smartphones, _ = Category.objects.get_or_create(
            slug="smartphones",
            defaults={"name": "Smartphones", "name_fa": "گوشی هوشمند"},
        )
        tablets, _ = Category.objects.get_or_create(
            slug="tablets",
            defaults={"name": "Tablets", "name_fa": "تبلت", "parent": smartphones},
        )

        black, _ = Color.objects.get_or_create(name="Black", defaults={"name_fa": "مشکی", "hex_code": "#000000"})
        white, _ = Color.objects.get_or_create(name="White", defaults={"name_fa": "سفید", "hex_code": "#FFFFFF"})
        blue, _ = Color.objects.get_or_create(name="Blue", defaults={"name_fa": "آبی", "hex_code": "#0066CC"})

        storage_128, _ = StorageOption.objects.get_or_create(capacity="128GB", defaults={"capacity_gb": 128})
        storage_256, _ = StorageOption.objects.get_or_create(capacity="256GB", defaults={"capacity_gb": 256})
        storage_512, _ = StorageOption.objects.get_or_create(capacity="512GB", defaults={"capacity_gb": 512})

        ram_8, _ = RAMOption.objects.get_or_create(capacity="8GB", defaults={"capacity_gb": 8})
        ram_12, _ = RAMOption.objects.get_or_create(capacity="12GB", defaults={"capacity_gb": 12})

        products_data = [
            ("iPhone 15 Pro", "آیفون ۱۵ پرو", "Apple", "IP15P", Decimal("45000000"), True, True),
            ("iPhone 15", "آیفون ۱۵", "Apple", "IP15", Decimal("38000000"), True, False),
            ("Galaxy S24 Ultra", "گلکسی اس ۲۴ اولترا", "Samsung", "GS24U", Decimal("42000000"), True, True),
            ("Galaxy A54", "گلکسی A54", "Samsung", "GA54", Decimal("15000000"), False, True),
            ("Pixel 8 Pro", "پیکسل ۸ پرو", "Google", "PX8P", Decimal("35000000"), True, False),
            ("Redmi Note 13 Pro", "ردمی نوت ۱۳ پرو", "Xiaomi", "RN13P", Decimal("12000000"), False, True),
        ]

        for name, name_fa, brand_name, sku_prefix, price, featured, best_seller in products_data:
            slug = slugify(name)
            product, created = Product.objects.get_or_create(
                sku=f"{sku_prefix}-001",
                defaults={
                    "name": name,
                    "name_fa": name_fa,
                    "slug": slug,
                    "brand": brands[brand_name],
                    "category": smartphones,
                    "description": f"{name} - Premium smartphone with advanced features.",
                    "description_fa": f"{name_fa} - گوشی هوشمند پیشرفته",
                    "short_description": f"Buy {name} at the best price",
                    "base_price": price,
                    "compare_price": price * Decimal("1.1"),
                    "is_active": True,
                    "is_featured": featured,
                    "is_best_seller": best_seller,
                    "warranty_months": 18,
                    "advantages": ["Great camera", "Long battery life", "Premium build"],
                    "features": ["5G", "Wireless charging", "Water resistant"],
                },
            )
            if created:
                product.tags.add("smartphone", brand_name.lower())
                ProductVariant.objects.get_or_create(
                    sku=f"{sku_prefix}-001-BLK-256",
                    defaults={
                        "product": product,
                        "color": black,
                        "storage": storage_256,
                        "ram": ram_8,
                        "price": price,
                        "stock_quantity": 100,
                        "is_default": True,
                    },
                )
                ProductVariant.objects.get_or_create(
                    sku=f"{sku_prefix}-001-WHT-512",
                    defaults={
                        "product": product,
                        "color": white,
                        "storage": storage_512,
                        "ram": ram_12,
                        "price": price * Decimal("1.15"),
                        "stock_quantity": 50,
                    },
                )
                ProductSpecification.objects.get_or_create(
                    product=product,
                    name="Display",
                    defaults={
                        "group_name": "Display",
                        "value": "6.7 inch OLED",
                        "sort_order": 1,
                    },
                )
                ProductSpecification.objects.get_or_create(
                    product=product,
                    name="Processor",
                    defaults={
                        "group_name": "Performance",
                        "value": "A17 Pro / Snapdragon 8 Gen 3",
                        "sort_order": 1,
                    },
                )

        self.stdout.write("  Catalog data created")

    def _seed_promotions(self):
        now = timezone.now()
        Coupon.objects.get_or_create(
            code="WELCOME10",
            defaults={
                "description": "10% off for new customers",
                "discount_type": "percentage",
                "discount_value": Decimal("10"),
                "min_order_amount": Decimal("1000000"),
                "max_discount_amount": Decimal("2000000"),
                "usage_limit": 1000,
                "is_active": True,
            },
        )
        Coupon.objects.get_or_create(
            code="FLAT500K",
            defaults={
                "description": "500,000 off orders above 5M",
                "discount_type": "fixed",
                "discount_value": Decimal("500000"),
                "min_order_amount": Decimal("5000000"),
                "is_active": True,
            },
        )

        flash_sale, _ = FlashSale.objects.get_or_create(
            title="Weekend Flash Sale",
            defaults={
                "title_fa": "فروش ویژه آخر هفته",
                "discount_percent": Decimal("15"),
                "starts_at": now - timedelta(days=1),
                "ends_at": now + timedelta(days=2),
                "is_active": True,
            },
        )
        product = Product.objects.filter(is_featured=True).first()
        if product:
            variant = product.variants.first()
            FlashSaleProduct.objects.get_or_create(
                flash_sale=flash_sale,
                product=product,
                variant=variant,
                defaults={"sale_price": product.base_price * Decimal("0.85")},
            )

        offer, created = SpecialOffer.objects.get_or_create(
            title="Trade-in Bonus",
            defaults={
                "title_fa": "پاداش تعویض گوشی",
                "description": "Get extra credit when trading in your old phone",
                "discount_text": "Up to 5M",
                "link_url": "/trade-in",
                "is_active": True,
            },
        )
        if created and not offer.image:
            from django.core.files.base import ContentFile

            offer.image.save("trade-in.jpg", ContentFile(b"placeholder"), save=True)
        self.stdout.write("  Promotions created")

    def _seed_cms(self):
        from django.core.files.base import ContentFile

        banner, created = Banner.objects.get_or_create(
            title="Summer Sale",
            defaults={
                "title_fa": "حراج تابستانه",
                "subtitle": "Up to 30% off on selected phones",
                "link_url": "/catalog/products/?is_featured=true",
                "button_text": "Shop Now",
                "location": "home_hero",
                "sort_order": 1,
            },
        )
        if created and not banner.image:
            banner.image.save("summer-sale.jpg", ContentFile(b"placeholder"), save=True)

        for i, (q, a) in enumerate([
            ("How long does shipping take?", "Standard delivery takes 2-5 business days."),
            ("What is the return policy?", "You can return products within 7 days of delivery."),
            ("Do you offer warranty?", "All products come with official warranty."),
        ], 1):
            FAQ.objects.get_or_create(
                question=q,
                defaults={"answer": a, "category": "General", "sort_order": i},
            )

        page, _ = Page.objects.get_or_create(
            slug="about-us",
            defaults={
                "title": "About Us",
                "title_fa": "درباره ما",
                "content": "<p>PhonyShop is Iran's leading online mobile phone store.</p>",
            },
        )

        menu, _ = Menu.objects.get_or_create(name="Main Header", defaults={"location": "header"})
        category = Category.objects.filter(parent__isnull=True).first()
        if category:
            MenuItem.objects.get_or_create(
                menu=menu,
                title="Smartphones",
                defaults={"category": category, "sort_order": 1},
            )
        MenuItem.objects.get_or_create(
            menu=menu,
            title="About",
            defaults={"page": page, "sort_order": 2},
        )

        Partner.objects.get_or_create(name="Apple Authorized", defaults={"sort_order": 1})
        Partner.objects.get_or_create(name="Samsung Partner", defaults={"sort_order": 2})

        CustomerReview.objects.get_or_create(
            author_name="Ali Rezaei",
            defaults={
                "content": "Great service and fast delivery!",
                "content_fa": "خدمات عالی و ارسال سریع!",
                "rating": 5,
                "is_featured": True,
            },
        )
        self.stdout.write("  CMS content created")

    def _seed_blog(self):
        category, _ = BlogCategory.objects.get_or_create(
            slug="tech-news",
            defaults={"name": "Tech News", "name_fa": "اخبار فناوری"},
        )
        admin = User.objects.filter(is_superuser=True).first()
        if admin:
            BlogPost.objects.get_or_create(
                slug="best-phones-2026",
                defaults={
                    "title": "Best Phones of 2026",
                    "title_fa": "بهترین گوشی‌های ۲۰۲۶",
                    "author": admin,
                    "category": category,
                    "excerpt": "Our top picks for the best smartphones.",
                    "content": "<p>Discover the best phones available in 2026.</p>",
                    "is_published": True,
                    "published_at": timezone.now(),
                },
            )
        self.stdout.write("  Blog posts created")

    def _seed_support(self):
        departments = [
            ("Sales", "فروش", "sales@phonyshop.com"),
            ("Technical Support", "پشتیبانی فنی", "support@phonyshop.com"),
            ("Returns", "مرجوعی", "returns@phonyshop.com"),
        ]
        for name, name_fa, email in departments:
            TicketDepartment.objects.get_or_create(
                name=name,
                defaults={"name_fa": name_fa, "email": email},
            )
        self.stdout.write("  Support departments created")

    def _seed_achievements(self):
        achievements = [
            ("First Purchase", "اولین خرید", 100),
            ("Loyal Customer", "مشتری وفادار", 500),
            ("Reviewer", "نقدکننده", 50),
        ]
        for name, name_fa, points in achievements:
            Achievement.objects.get_or_create(
                name=name,
                defaults={"name_fa": name_fa, "points_reward": points, "description": f"Earned by completing {name}"},
            )
        self.stdout.write("  Achievements created")

    def _seed_notification_templates(self):
        NotificationTemplate.objects.get_or_create(
            name="order_confirmation",
            defaults={
                "notification_type": "order",
                "title_template": "Order {{ order_number }} confirmed",
                "message_template": "Your order totaling {{ total }} has been placed successfully.",
                "email_template": "Order {{ order_number }} confirmed. Total: {{ total }}",
                "is_active": True,
            },
        )
        self.stdout.write("  Notification templates created")

    def _seed_search(self):
        for query in ["iphone", "samsung", "galaxy", "pixel", "xiaomi"]:
            PopularSearch.objects.get_or_create(query=query, defaults={"search_count": 100, "is_featured": True})
        self.stdout.write("  Popular searches created")

    def _seed_users(self):
        admin, admin_created = self._get_or_create_user(
            email="admin@phonyshop.com",
            username="admin",
            password="admin123",
            first_name="Admin",
            last_name="User",
            is_superuser=True,
            is_staff=True,
            phone="+982112345678",
            preferred_language="fa",
        )
        customer, customer_created = self._get_or_create_user(
            email="customer@phonyshop.com",
            username="customer",
            password="customer123",
            first_name="Ali",
            last_name="Rezaei",
            phone="+989121234567",
            preferred_language="fa",
        )

        if admin:
            Profile.objects.update_or_create(
                user=admin,
                defaults={
                    "first_name_fa": "مدیر",
                    "last_name_fa": "سیستم",
                    "bio": "مدیر پلتفرم فونی‌شاپ",
                },
            )

        if customer:
            Profile.objects.update_or_create(
                user=customer,
                defaults={
                    "first_name_fa": "علی",
                    "last_name_fa": "رضایی",
                    "bio": "مشتری وفادار فونی‌شاپ",
                },
            )
            wallet, _ = Wallet.objects.get_or_create(user=customer)
            wallet.balance = Decimal("12500000")
            wallet.bonus_balance = Decimal("500000")
            wallet.save(update_fields=["balance", "bonus_balance"])

            gold_level = MembershipLevel.objects.filter(name="gold").first()
            if gold_level:
                UserMembership.objects.update_or_create(
                    user=customer,
                    defaults={"level": gold_level, "points": 2450, "total_spent": Decimal("15000000")},
                )

            tehran = Province.objects.filter(code="THR").first()
            city = City.objects.filter(province=tehran).first() if tehran else None
            if tehran and city:
                Address.objects.update_or_create(
                    user=customer,
                    title="منزل",
                    defaults={
                        "recipient_name": "علی رضایی",
                        "phone": "+989121234567",
                        "province": tehran,
                        "city": city,
                        "postal_code": "1969712345",
                        "address_line": "خیابان ولیعصر، پلاک ۱۲۳، واحد ۴",
                        "is_default": True,
                    },
                )

        self.stdout.write("  Users: admin@phonyshop.com / admin123")
        self.stdout.write("  Users: customer@phonyshop.com / customer123")

    def _get_or_create_user(self, email, username, password, **extra):
        user = User.objects.filter(email=email).first()
        if user:
            return user, False
        if extra.pop("is_superuser", False):
            user = User.objects.create_superuser(
                username=username, email=email, password=password, **extra
            )
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password, **extra
            )
        return user, True

    def _seed_inventory(self):
        warehouse, _ = Warehouse.objects.get_or_create(
            code="WH-MAIN",
            defaults={"name": "Main Warehouse", "address": "Tehran Industrial Zone", "is_default": True},
        )
        supplier, _ = Supplier.objects.get_or_create(
            name="Mobile Distributors Inc.",
            defaults={"contact_person": "John Doe", "email": "orders@distributor.com"},
        )
        for variant in ProductVariant.objects.all()[:10]:
            InventoryItem.objects.get_or_create(
                variant=variant,
                warehouse=warehouse,
                defaults={"quantity": variant.stock_quantity, "supplier": supplier},
            )
        self.stdout.write("  Inventory created")

    def _seed_reviews(self):
        user = User.objects.filter(email="customer@phonyshop.com").first()
        product = Product.objects.first()
        if user and product:
            Review.objects.get_or_create(
                user=user,
                product=product,
                defaults={
                    "rating": 5,
                    "title": "Excellent phone!",
                    "content": "Very satisfied with the purchase. Fast delivery and genuine product.",
                    "pros": ["Great camera", "Smooth performance"],
                    "cons": ["Expensive"],
                    "is_approved": True,
                },
            )
            product.average_rating = Decimal("5.00")
            product.review_count = 1
            product.save(update_fields=["average_rating", "review_count"])
        self.stdout.write("  Reviews created")
