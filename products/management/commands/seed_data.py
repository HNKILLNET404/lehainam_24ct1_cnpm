"""
Management command: seed_data
Tao du lieu mau cho Urban Threads (danh muc, mau, size, san pham, anh, coupon, banner)
Chay: venv\\Scripts\\python manage.py seed_data
"""
import urllib.request
import uuid
import random
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Category, Color, Size, Product, ProductVariant, ProductImage
from promotions.models import Coupon, Banner


UNSPLASH_PRODUCTS = [
    ("https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80", "Ao thun trang"),
    ("https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&q=80", "Ao thun den"),
    ("https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600&q=80", "Ao thun xam"),
    ("https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=600&q=80", "Ao hoodie"),
    ("https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=600&q=80", "Ao sweater"),
    ("https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600&q=80", "Quan jeans"),
    ("https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&q=80", "Quan kaki"),
    ("https://images.unsplash.com/photo-1603252109303-2751441dd157?w=600&q=80", "Ao khoac"),
    ("https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=600&q=80", "Ao polo"),
    ("https://images.unsplash.com/photo-1614975059251-992f11792b9f?w=600&q=80", "Ao so mi"),
]


def download_image_bytes(url):
    """Download anh ve dang bytes"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read()
    except Exception as e:
        print(f"  [!] Khong tai duoc anh {url}: {e}")
        return None


class Command(BaseCommand):
    help = 'Tao du lieu mau cho website Urban Threads'

    def handle(self, *args, **options):
        self.stdout.write('[*] Bat dau tao du lieu mau...')

        # ── 1. COLORS ──────────────────────────────────────────────
        self.stdout.write('[*] Tao mau sac...')
        colors_data = [
            ('Đen', '#000000'), ('Trắng', '#FFFFFF'), ('Xám', '#808080'),
            ('Navy', '#1B2A4A'), ('Be', '#F5F0E8'), ('Nâu', '#6B4226'),
            ('Xanh lá', '#2D6A4F'), ('Đỏ', '#C62828'),
        ]
        colors = {}
        for name, hex_code in colors_data:
            color, _ = Color.objects.get_or_create(name=name, defaults={'hex_code': hex_code})
            colors[name] = color
        self.stdout.write(f'  + {len(colors)} mau sac')

        # ── 2. SIZES ──────────────────────────────────────────────
        self.stdout.write('[*] Tao kich thuoc...')
        sizes_data = [('S', 0), ('M', 1), ('L', 2), ('XL', 3), ('XXL', 4), ('30', 5), ('32', 6)]
        sizes = {}
        for name, order in sizes_data:
            size, _ = Size.objects.get_or_create(name=name, defaults={'order': order})
            sizes[name] = size
        self.stdout.write(f'  + {len(sizes)} kich co')

        # ── 3. CATEGORIES ──────────────────────────────────────────
        self.stdout.write('[*] Tao danh muc...')
        cats_data = [
            ('Áo Thun', 'ao-thun', 0),
            ('Áo Hoodie & Sweater', 'ao-hoodie-sweater', 1),
            ('Áo Khoác', 'ao-khoac', 2),
            ('Quần Dài', 'quan-dai', 3),
            ('Áo Polo & Sơ Mi', 'ao-polo-so-mi', 4),
        ]
        cats = {}
        for name, slug, order in cats_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'is_active': True, 'order': order}
            )
            cats[slug] = cat
        self.stdout.write(f'  + {len(cats)} danh muc')

        # ── 4. PRODUCTS ──────────────────────────────────────────────
        self.stdout.write('[*] Tao san pham...')
        products_data = [
            {
                'name': 'Áo Thun Basic Oversize',
                'slug': 'ao-thun-basic-oversize',
                'category': cats['ao-thun'],
                'description': 'Áo thun oversize form rộng thoải mái, chất liệu cotton 100% mềm mịn. Phù hợp mặc hàng ngày hay dạo phố.',
                'material': '100% Cotton Combed 30s',
                'gender': 'unisex',
                'base_price': 290000,
                'is_new_arrival': True,
                'is_best_seller': True,
                'is_featured': True,
                'img_idx': 0,
                'colors': ['Đen', 'Trắng', 'Xám'],
                'sizes': ['S', 'M', 'L', 'XL'],
            },
            {
                'name': 'Áo Thun Cổ Tròn Premium',
                'slug': 'ao-thun-co-tron-premium',
                'category': cats['ao-thun'],
                'description': 'Áo thun cổ tròn chất lượng cao, đường may chắc chắn. Form đứng vừa vặn phù hợp nhiều vóc dáng.',
                'material': '65% Cotton, 35% Polyester',
                'gender': 'male',
                'base_price': 250000,
                'sale_price': 199000,
                'is_new_arrival': True,
                'img_idx': 2,
                'colors': ['Đen', 'Navy', 'Be'],
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
            },
            {
                'name': 'Hoodie Nặng Dây Kéo Urban',
                'slug': 'hoodie-nang-day-keo-urban',
                'category': cats['ao-hoodie-sweater'],
                'description': 'Hoodie dày dặn, chất nỉ bông bên trong siêu ấm. Thiết kế tối giản với logo Urban Threads thêu nhỏ ở ngực trái.',
                'material': '80% Cotton, 20% Polyester fleece',
                'gender': 'unisex',
                'base_price': 590000,
                'is_featured': True,
                'is_best_seller': True,
                'img_idx': 3,
                'colors': ['Đen', 'Xám', 'Navy'],
                'sizes': ['S', 'M', 'L', 'XL'],
            },
            {
                'name': 'Sweater Cổ Tròn Vintage',
                'slug': 'sweater-co-tron-vintage',
                'category': cats['ao-hoodie-sweater'],
                'description': 'Sweater len cotton mềm mại, form boxy vintage. Cổ tay và gấu áo gân dệt co giãn tốt.',
                'material': '60% Cotton, 40% Acrylic',
                'gender': 'unisex',
                'base_price': 490000,
                'sale_price': 390000,
                'is_new_arrival': True,
                'img_idx': 4,
                'colors': ['Be', 'Nâu', 'Xanh lá'],
                'sizes': ['S', 'M', 'L', 'XL'],
            },
            {
                'name': 'Áo Khoác Gió Lightweight',
                'slug': 'ao-khoac-gio-lightweight',
                'category': cats['ao-khoac'],
                'description': 'Áo khoác gió siêu nhẹ, chống nước nhẹ. Dễ dàng gấp gọn trong túi khi không dùng. Phù hợp đi du lịch, ngoài trời.',
                'material': 'Nylon Ripstop chống nước',
                'gender': 'unisex',
                'base_price': 750000,
                'is_featured': True,
                'img_idx': 7,
                'colors': ['Đen', 'Navy', 'Xanh lá'],
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
            },
            {
                'name': 'Quần Jeans Slim Fit Nam',
                'slug': 'quan-jeans-slim-fit-nam',
                'category': cats['quan-dai'],
                'description': 'Quần jeans nam ôm vừa, vải denim 9oz co giãn 4 chiều thoải mái. Phù hợp nhiều style từ casual đến smart casual.',
                'material': 'Denim 9oz, 98% Cotton 2% Spandex',
                'gender': 'male',
                'base_price': 550000,
                'is_best_seller': True,
                'img_idx': 5,
                'colors': ['Đen', 'Navy'],
                'sizes': ['30', '32'],
            },
            {
                'name': 'Quần Kaki Chino Công Sở',
                'slug': 'quan-kaki-chino-cong-so',
                'category': cats['quan-dai'],
                'description': 'Quần kaki chino thoáng mát, form slim straight lịch sự. Phù hợp đi làm, họp, sự kiện.',
                'material': 'Cotton Kaki 230gsm',
                'gender': 'male',
                'base_price': 480000,
                'img_idx': 6,
                'colors': ['Be', 'Nâu', 'Xám', 'Đen'],
                'sizes': ['30', '32'],
            },
            {
                'name': 'Áo Polo Cotton Piqué',
                'slug': 'ao-polo-cotton-pique',
                'category': cats['ao-polo-so-mi'],
                'description': 'Áo polo vải piqué cotton thoáng mát, cổ bẻ gọn gàng. Phù hợp văn phòng và casual đơn giản.',
                'material': '100% Cotton Piqué 220gsm',
                'gender': 'male',
                'base_price': 380000,
                'sale_price': 299000,
                'is_new_arrival': True,
                'img_idx': 8,
                'colors': ['Trắng', 'Đen', 'Navy'],
                'sizes': ['S', 'M', 'L', 'XL'],
            },
            {
                'name': 'Áo Sơ Mi Oxford Button-Down',
                'slug': 'ao-so-mi-oxford-button-down',
                'category': cats['ao-polo-so-mi'],
                'description': 'Áo sơ mi vải Oxford thông hơi tốt, không nhăn sau giặt. Form slim fit hiện đại.',
                'material': 'Oxford Cotton 130gsm',
                'gender': 'male',
                'base_price': 450000,
                'is_featured': True,
                'img_idx': 9,
                'colors': ['Trắng', 'Be', 'Xanh lá'],
                'sizes': ['S', 'M', 'L', 'XL'],
            },
            {
                'name': 'Áo Thun Nữ Crop Ribbed',
                'slug': 'ao-thun-nu-crop-ribbed',
                'category': cats['ao-thun'],
                'description': 'Áo thun nữ dáng crop, vải gân thun co giãn 4 chiều ôm body. Phối với quần jeans hay chân váy đều đẹp.',
                'material': '95% Cotton 5% Elastane Ribbed',
                'gender': 'female',
                'base_price': 220000,
                'is_new_arrival': True,
                'is_best_seller': True,
                'img_idx': 1,
                'colors': ['Đen', 'Trắng', 'Be', 'Đỏ'],
                'sizes': ['S', 'M', 'L'],
            },
        ]

        created = 0
        for p_data in products_data:
            product, is_new = Product.objects.get_or_create(
                slug=p_data['slug'],
                defaults={
                    'name': p_data['name'],
                    'category': p_data['category'],
                    'description': p_data['description'],
                    'material': p_data.get('material', ''),
                    'gender': p_data.get('gender', 'unisex'),
                    'base_price': p_data['base_price'],
                    'sale_price': p_data.get('sale_price', None),
                    'is_active': True,
                    'is_new_arrival': p_data.get('is_new_arrival', False),
                    'is_best_seller': p_data.get('is_best_seller', False),
                    'is_featured': p_data.get('is_featured', False),
                }
            )

            # Download & attach image if not present
            if not product.images.exists():
                img_url, alt = UNSPLASH_PRODUCTS[p_data['img_idx']]
                self.stdout.write(f'  -> Dang tai anh cho {product.name}...')
                img_bytes = download_image_bytes(img_url)
                if img_bytes:
                    pi = ProductImage(product=product, is_main=True, alt_text=product.name)
                    pi.image.save(f'{product.slug}.jpg', ContentFile(img_bytes), save=True)

            # Create variants
            product_colors = [colors[c] for c in p_data.get('colors', ['Đen']) if c in colors]
            product_sizes = [sizes[s] for s in p_data.get('sizes', ['M']) if s in sizes]

            for color in product_colors:
                for size in product_sizes:
                    unique_sku = f"UT-{str(product.id)[:6].upper()}-{color.id}-{size.name}"
                    ProductVariant.objects.get_or_create(
                        product=product, color=color, size=size,
                        defaults={
                            'stock': random.randint(10, 50),
                            'sku': unique_sku,
                            'extra_price': 0
                        }
                    )

            created += 1
            self.stdout.write(f'  + OK: {product.name}')

        # ── 5. COUPONS ──────────────────────────────────────────────
        self.stdout.write('[*] Tao coupon khuyen mai...')
        Coupon.objects.get_or_create(
            code='WELCOME10',
            defaults={
                'description': 'Giam 10% cho don hang dau tien',
                'discount_type': 'percentage',
                'discount_value': 10,
                'minimum_order': 200000,
                'is_active': True
            }
        )
        Coupon.objects.get_or_create(
            code='GIAM50K',
            defaults={
                'description': 'Giam 50.000d cho don hang tu 500k',
                'discount_type': 'fixed',
                'discount_value': 50000,
                'minimum_order': 500000,
                'is_active': True
            }
        )
        self.stdout.write('  + Coupon WELCOME10 va GIAM50K da san sang')

        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Hoan thanh tao {created} san pham, variants, va coupons!'))
