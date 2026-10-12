from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Review
from products.models import Product


@login_required
@require_POST
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    rating = int(request.POST.get('rating', 5))
    title = request.POST.get('title', '')
    body = request.POST.get('body', '')
    if not body.strip():
        messages.error(request, 'Vui lòng nhập nội dung đánh giá.')
        return redirect('product_detail', slug=product.slug)
    Review.objects.update_or_create(
        product=product, user=request.user,
        defaults={'rating': rating, 'title': title, 'body': body}
    )
    messages.success(request, 'Đã gửi đánh giá của bạn!')
    return redirect('product_detail', slug=product.slug)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    slug = review.product.slug
    review.delete()
    messages.success(request, 'Đã xóa đánh giá.')
    return redirect('product_detail', slug=slug)
