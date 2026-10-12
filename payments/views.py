from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Payment
from orders.models import Order
import qrcode
from io import BytesIO
import base64


VIETNAM_BANKS = {
    '970436': 'Vietcombank (Ngoại thương Việt Nam)',
    'VCB': 'Vietcombank (Ngoại thương Việt Nam)',
    '970407': 'Techcombank (Kỹ thương Việt Nam)',
    'TCB': 'Techcombank (Kỹ thương Việt Nam)',
    '970422': 'MB Bank (Ngân hàng Quân Đội)',
    'MB': 'MB Bank (Ngân hàng Quân Đội)',
    '970415': 'VietinBank (Công Thương Việt Nam)',
    'CTG': 'VietinBank (Công Thương Việt Nam)',
    '970418': 'BIDV (Đầu tư và Phát triển VN)',
    'BIDV': 'BIDV (Đầu tư và Phát triển VN)',
    '970416': 'ACB (Á Châu)',
    'ACB': 'ACB (Á Châu)',
    '970423': 'TPBank (Tiên Phong)',
    'TPB': 'TPBank (Tiên Phong)',
    '970432': 'VPBank (Việt Nam Thịnh Vượng)',
    'VPB': 'VPBank (Việt Nam Thịnh Vượng)',
    '970405': 'Agribank (Nông nghiệp & PTNT)',
    'VBA': 'Agribank (Nông nghiệp & PTNT)',
    '970403': 'Sacombank (Sài Gòn Thương Tín)',
    'STB': 'Sacombank (Sài Gòn Thương Tín)',
    '970441': 'VIB (Quốc tế Việt Nam)',
    'VIB': 'VIB (Quốc tế Việt Nam)',
    '970443': 'SHB (Sài Gòn - Hà Nội)',
    'SHB': 'SHB (Sài Gòn - Hà Nội)',
    '970437': 'HDBank (Phát triển TP.HCM)',
    'HDB': 'HDBank (Phát triển TP.HCM)',
    '970426': 'MSB (Hàng Hải)',
    'MSB': 'MSB (Hàng Hải)',
    '970448': 'OCB (Phương Đông)',
    'OCB': 'OCB (Phương Đông)',
}


def get_bank_info():
    bank_id = str(getattr(settings, 'BANK_ID', '970422'))
    bank_name = getattr(settings, 'BANK_NAME', '')
    if not bank_name:
        bank_name = VIETNAM_BANKS.get(bank_id.upper(), f"Ngân hàng ({bank_id})")
    return {
        'bank_id': bank_id,
        'bank_name': bank_name,
        'account_no': getattr(settings, 'BANK_ACCOUNT_NO', '1234567890'),
        'account_name': getattr(settings, 'BANK_ACCOUNT_NAME', 'URBAN THREADS STORE'),
    }


def generate_vietqr(amount, order_number):
    bank_info = get_bank_info()
    bank_id = bank_info['bank_id']
    account_no = bank_info['account_no']
    account_name = bank_info['account_name']
    bank_template = getattr(settings, 'BANK_TEMPLATE', 'compact')
    
    desc = f'Thanh toan {order_number}'.replace(' ', '%20')
    vietqr_url = (f'https://img.vietqr.io/image/{bank_id}-{account_no}-'
                  f'{bank_template}.png?amount={int(amount)}&addInfo={desc}&accountName={account_name}')
    qr = qrcode.make(f'Bank:{bank_id}\nAccount:{account_no}\nAmount:{int(amount)}\nContent:{order_number}')
    buf = BytesIO()
    qr.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode()
    return vietqr_url, qr_b64


@login_required
def payment_qr_view(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    payment, _ = Payment.objects.get_or_create(order=order, defaults={'amount': order.total})
    vietqr_url, qr_b64 = generate_vietqr(order.total, order.order_number)
    bank_info = get_bank_info()
    return render(request, 'payments/payment_qr.html', {
        'order': order, 'payment': payment,
        'vietqr_url': vietqr_url, 'qr_b64': qr_b64, 'bank_info': bank_info,
    })


@login_required
def upload_receipt(request, payment_id):
    if request.user.is_staff:
        payment = get_object_or_404(Payment, id=payment_id)
    else:
        payment = get_object_or_404(Payment, id=payment_id, order__user=request.user)
    if request.method == 'POST' and request.FILES.get('receipt'):
        payment.receipt_image = request.FILES['receipt']
        payment.status = 'uploaded'
        payment.order.status = 'confirmed'
        payment.order.save()
        payment.save()
        messages.success(request, 'Đã gửi biện lai! Chúng tôi sẽ xác nhận trong 30 phút.')
        return redirect('order_thank_you', order_id=payment.order.id)
    return redirect('payment_qr', order_id=payment.order.id)
