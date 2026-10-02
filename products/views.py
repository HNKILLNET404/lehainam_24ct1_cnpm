import unicodedata
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Product, Category, ProductVariant, Color, Size


def remove_accents(s):
    """Chuyển chuỗi tiếng Việt có dấu thành không dấu (chuẩn hóa tìm kiếm)"""
    if not s:
        return ''
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).replace('đ', 'd').replace('Đ', 'D').lower()


def search_products(query_str, base_queryset=None):
    """Tìm kiếm thông minh chuẩn thương mại điện tử:
    - Hỗ trợ cả gõ có dấu lẫn không dấu (áo thun / ao thun)
    - Ưu tiên cao nhất: Tên sản phẩm, Mã nhận dạng (slug), Màu sắc
    - Chỉ tìm trong mô tả và danh mục khi không có sản phẩm khớp trực tiếp
    """
    if not query_str or not query_str.strip():
        return Product.objects.none() if base_queryset is None else base_queryset

    raw_terms = query_str.strip().split()
    norm_terms = remove_accents(query_str).split()

    if base_queryset is None:
        qs = Product.objects.filter(is_active=True).prefetch_related('images', 'category', 'variants__color')
    else:
        qs = base_queryset.filter(is_active=True)

    # Tầng 1: Tìm kiếm chính xác cao (Tên sản phẩm, slug, màu sắc)
    tier1_qs = qs
    for raw_t, norm_t in zip(raw_terms, norm_terms):
        tier1_term = (
            Q(name__icontains=raw_t) |
            Q(slug__icontains=norm_t) |
            Q(variants__color__name__icontains=raw_t)
        )
        tier1_qs = tier1_qs.filter(tier1_term)

    if tier1_qs.exists():
        return tier1_qs.distinct()

    # Tầng 2: Nếu tầng 1 không có, mới tìm mở rộng trong chất liệu, danh mục và mô tả
    tier2_qs = qs
    for raw_t, norm_t in zip(raw_terms, norm_terms):
        tier2_term = (
            Q(category__name__icontains=raw_t) |
            Q(category__slug__icontains=norm_t) |
            Q(material__icontains=raw_t) |
            Q(description__icontains=raw_t)
        )
        tier2_qs = tier2_qs.filter(tier2_term)

    return tier2_qs.distinct()


def home(request):
    """Trang chủ"""
    new_arrivals = Product.objects.filter(is_active=True, is_new_arrival=True).prefetch_related('images', 'variants')[:8]
    best_sellers = Product.objects.filter(is_active=True, is_best_seller=True).prefetch_related('images', 'variants')[:8]
    featured = Product.objects.filter(is_active=True, is_featured=True).prefetch_related('images', 'variants')[:4]
    categories = Category.objects.filter(is_active=True, parent=None)[:6]
    on_sale = Product.objects.filter(is_active=True, sale_price__isnull=False).prefetch_related('images')[:6]
    context = {
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'featured': featured,
        'categories': categories,
        'on_sale': on_sale,
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    """Danh sách sản phẩm"""
    products = Product.objects.filter(is_active=True).prefetch_related('images', 'variants', 'category')

    # Filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    gender = request.GET.get('gender')
    if gender in ['male', 'female', 'unisex']:
        products = products.filter(gender=gender)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(base_price__gte=min_price)
    if max_price:
        products = products.filter(base_price__lte=max_price)

    colors = request.GET.getlist('color')
    if colors:
        products = products.filter(variants__color__id__in=colors).distinct()

    sizes = request.GET.getlist('size')
    if sizes:
        products = products.filter(variants__size__id__in=sizes).distinct()

    on_sale = request.GET.get('on_sale')
    if on_sale:
        products = products.filter(sale_price__isnull=False)

    # Search keyword
    q = request.GET.get('q', '').strip()
    if q:
        products = search_products(q, base_queryset=products)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    sort_options = {
        'newest': '-created_at',
        'price_asc': 'base_price',
        'price_desc': '-base_price',
        'best_seller': '-total_sold',
    }
    products = products.order_by(sort_options.get(sort, '-created_at'))

    # Paginate
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products_page = paginator.get_page(page)

    context = {
        'products': products_page,
        'categories': Category.objects.filter(is_active=True),
        'all_colors': Color.objects.all(),
        'all_sizes': Size.objects.all(),
        'current_sort': sort,
        'selected_colors': [int(c) for c in colors],
        'selected_sizes': [int(s) for s in sizes],
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    variants = product.variants.select_related('color', 'size').all()
    colors = Color.objects.filter(productvariant__product=product).distinct()
    sizes = Size.objects.filter(productvariant__product=product).distinct()
    reviews = product.reviews.select_related('user').order_by('-created_at')[:10]
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id).prefetch_related('images')[:4]

    # Build variant map for JS
    variant_map = {}
    for v in variants:
        key = f"{v.color.id if v.color else 'none'}-{v.size.id if v.size else 'none'}"
        variant_map[key] = {
            'id': v.id, 'stock': v.stock, 'price': str(v.final_price)
        }

    context = {
        'product': product,
        'images': images,
        'colors': colors,
        'sizes': sizes,
        'variants': variants,
        'variant_map': variant_map,
        'reviews': reviews,
        'related_products': related,
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    """Trang danh mục"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True).prefetch_related('images', 'variants')
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products_page = paginator.get_page(page)
    return render(request, 'products/category_detail.html', {'category': category, 'products': products_page})


def search_view(request):
    """Tìm kiếm sản phẩm"""
    q = request.GET.get('q', '').strip()
    products = search_products(q)
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products_page = paginator.get_page(page)
    return render(request, 'products/search_results.html', {'products': products_page, 'query': q})


def search_suggestions(request):
    """Gợi ý tìm kiếm (AJAX)"""
    from django.http import JsonResponse
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        qs = search_products(q)[:5]
        results = [{'name': p.name, 'slug': p.slug} for p in qs]
    return JsonResponse({'results': results})
