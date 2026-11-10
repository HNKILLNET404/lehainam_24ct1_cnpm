from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse


def about_view(request):
    return render(request, 'pages/about.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message_body = request.POST.get('message', '')

        if name and email and message_body:
            messages.success(request, f'Cảm ơn {name}! Chúng tôi đã nhận được tin nhắn và sẽ phản hồi sớm nhất.')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin bắt buộc.')

    return render(request, 'pages/contact.html')


def size_guide_view(request):
    """Hướng dẫn chọn size"""
    return render(request, 'pages/size_guide.html')


def returns_policy_view(request):
    """Chính sách đổi trả"""
    return render(request, 'pages/returns.html')


def faq_view(request):
    """Câu hỏi thường gặp"""
    return render(request, 'pages/faq.html')


def terms_view(request):
    """Điều khoản dịch vụ"""
    return render(request, 'pages/terms.html')


def privacy_view(request):
    """Chính sách bảo mật"""
    return render(request, 'pages/privacy.html')


def cookie_policy_view(request):
    """Chính sách Cookie"""
    return render(request, 'pages/cookie_policy.html')


def newsletter_subscribe(request):
    """Đăng ký nhận bản tin khuyến mãi"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email and '@' in email:
            msg = 'Cảm ơn bạn đã đăng ký nhận bản tin khuyến mãi từ Urban Threads!'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': msg})
            messages.success(request, msg)
        else:
            msg = 'Vui lòng nhập địa chỉ email hợp lệ.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': msg}, status=400)
            messages.error(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def page_not_found(request, exception):
    """Custom 404 handler"""
    return render(request, '404.html', status=404)


def server_error(request):
    """Custom 500 handler"""
    return render(request, '500.html', status=500)

