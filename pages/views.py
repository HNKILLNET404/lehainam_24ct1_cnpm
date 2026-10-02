from django.shortcuts import render
from django.contrib import messages


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


def page_not_found(request, exception):
    """Custom 404 handler"""
    return render(request, '404.html', status=404)


def server_error(request):
    """Custom 500 handler"""
    return render(request, '500.html', status=500)
