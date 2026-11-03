import sys, urllib.request, http.cookiejar, urllib.parse, re
sys.stdout.reconfigure(encoding='utf-8')

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

resp = opener.open('https://urbanthreads-vn.onrender.com/admin/login/')
html = resp.read().decode('utf-8')
csrf_token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html).group(1)

params = urllib.parse.urlencode({
    'csrfmiddlewaretoken': csrf_token,
    'username': 'admin@urbanthreads.com',
    'password': 'admin123',
    'next': '/admin/'
}).encode('utf-8')

opener.open(urllib.request.Request('https://urbanthreads-vn.onrender.com/admin/login/', data=params, headers={'Referer': 'https://urbanthreads-vn.onrender.com/admin/login/'}))

resp = opener.open('https://urbanthreads-vn.onrender.com/admin/orders/order/1768718a-fed9-471d-9a6a-5d41425a1e90/change/')
print('HTTP Status Code:', resp.getcode())
html = resp.read().decode('utf-8')
title = re.search(r'<title>(.*?)</title>', html)
print('Page Title:', title.group(1) if title else 'No title')
print('Has QR link:', 'Xem QR Code' in html)
print('Has Order items table:', ('Chi tiết đơn hàng' in html) or ('Sản phẩm' in html))
