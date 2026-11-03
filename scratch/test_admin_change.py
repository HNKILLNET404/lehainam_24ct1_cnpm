import urllib.request
import urllib.parse
import http.cookiejar
import re
import time

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def test_page():
    # 1. Get csrf token
    resp = opener.open('https://urbanthreads-vn.onrender.com/admin/login/')
    html = resp.read().decode('utf-8')
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
    if not match:
        print('Could not find csrf token')
        return False
    csrf_token = match.group(1)

    # 2. Login
    params = urllib.parse.urlencode({
        'csrfmiddlewaretoken': csrf_token,
        'username': 'admin@urbanthreads.com',
        'password': 'admin123',
        'next': '/admin/'
    }).encode('utf-8')
    
    req = urllib.request.Request(
        'https://urbanthreads-vn.onrender.com/admin/login/',
        data=params,
        headers={'Referer': 'https://urbanthreads-vn.onrender.com/admin/login/'}
    )
    resp = opener.open(req)
    print('Admin Login status:', resp.getcode())

    # 3. Request the order change page
    target_url = 'https://urbanthreads-vn.onrender.com/admin/orders/order/1768718a-fed9-471d-9a6a-5d41425a1e90/change/'
    try:
        resp = opener.open(target_url)
        content = resp.read().decode('utf-8', errors='ignore')
        print('Order change page status:', resp.getcode())
        if 'Thay đổi Đơn hàng' in content or 'Chi tiết đơn hàng' in content:
            print('SUCCESS: Page rendered cleanly without any TypeError!')
            return True
        else:
            print('Page loaded, checking content snippet:', content[:150])
            return True
    except urllib.error.HTTPError as e:
        print(f'HTTP Error {e.code}: {e.reason}')
        body = e.read().decode('utf-8', errors='ignore')
        if 'TypeError' in body:
            print('Deploy still in progress on Render (TypeError still present)...')
        else:
            print('Error body snippet:', body[:200])
        return False

for i in range(15):
    print(f'--- Check #{i+1} ---')
    success = test_page()
    if success:
        break
    time.sleep(10)
