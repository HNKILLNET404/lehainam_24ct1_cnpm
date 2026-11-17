from .models import Category


def categories_processor(request):
    """Inject categories into all templates"""
    main_categories = Category.objects.filter(is_active=True, parent=None).order_by('order')
    return {'main_categories': main_categories}
