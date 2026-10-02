from django import template

register = template.Library()


@register.filter(name='currency')
def currency(val):
    """
    Format giá tiền dạng 200,000đ (dùng dấu phẩy phân cách hàng nghìn)
    """
    if val is None or val == '':
        return ''
    try:
        val_float = float(val)
        return f"{val_float:,.0f}đ"
    except (ValueError, TypeError):
        return val


@register.filter(name='comma')
def comma(val):
    """
    Format số dạng 200,000 (không có chữ đ)
    """
    if val is None or val == '':
        return ''
    try:
        val_float = float(val)
        return f"{val_float:,.0f}"
    except (ValueError, TypeError):
        return val
