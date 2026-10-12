# 🏗️ KIẾN TRÚC HỆ THỐNG — URBAN THREADS

## Stack công nghệ

| Lớp | Framework / Công nghệ | Phiên bản | Ngôn ngữ |
|---|---|---|---|
| **PHÍA TRƯỚC (Frontend)** | Tailwind CSS | CDN v3.x | CSS3 |
| **PHÍA TRƯỚC (Frontend)** | Alpine.js | CDN v3.x | JavaScript ES6 |
| **PHÍA TRƯỚC (Frontend)** | Django Template Engine (DTL) | 5.1.1 | HTML5 |
| **PHÍA SAU (Backend)** | Django | 5.1.1 | Python 3.10+ |
| **CƠ SỞ DỮ LIỆU** | SQLite | 3.x | SQL |
| **Cổng thanh toán** | VietQR API (Napas247) | - | REST API |

---

## Sơ đồ kiến trúc đầy đủ

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NGƯỜI DÙNG (User Layer)                               │
│  👤 Khách hàng (Customer)          🔑 Quản trị viên (Admin)             │
│     Trình duyệt Web                   Trình duyệt Web                   │
└───────────────────┬────────────────────────────┬────────────────────────┘
                    │ HTTP Request                │ HTTP Request /admin/
                    ▼                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│         PHÍA TRƯỚC — FRONTEND (Giao diện người dùng)                    │
│  Framework: Tailwind CSS v3 (CDN) + Alpine.js v3 (CDN)                  │
│  Engine: Django Template Language (DTL)                                  │
│                                                                          │
│  templates/products/home.html          ← Trang chủ & New Arrivals       │
│  templates/products/product_list.html  ← Danh mục & Bộ lọc sản phẩm   │
│  templates/products/product_detail.html← Chi tiết & Chọn Size/Màu SKU  │
│  templates/cart/cart.html              ← Giỏ hàng đầy đủ               │
│  templates/cart/mini_cart.html         ← Mini Cart Drawer (AJAX)        │
│  templates/orders/checkout.html        ← Trang đặt hàng Checkout        │
│  templates/payments/payment_qr.html    ← Quét mã VietQR thanh toán      │
│  templates/accounts/register.html      ← Form Đăng ký tài khoản         │
│  templates/accounts/login.html         ← Form Đăng nhập hệ thống        │
│  templates/accounts/order_history.html ← Lịch sử & trạng thái đơn hàng │
│  templates/wishlists/wishlist.html     ← Danh sách sản phẩm yêu thích   │
│  templates/promotions/promotions.html  ← Trang khuyến mãi & Coupon      │
│  templates/base.html                   ← Layout chính toàn hệ thống     │
└───────────────────────────┬─────────────────────────────────────────────┘
                            │ HTTP POST/GET Request
                            │ JSON Response (AJAX)
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│         PHÍA SAU — BACKEND (Xử lý nghiệp vụ)                           │
│  Framework: Django 5.1.1 | Ngôn ngữ: Python 3.10+                      │
│  Kiến trúc: MVT (Model - View - Template)                               │
│  Bộ định tuyến: urban_threads/urls.py                                   │
│  Cấu hình: urban_threads/settings.py                                    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Django Apps (9 module)                        │    │
│  │                                                                  │    │
│  │  accounts/views.py   ← Đăng ký, Đăng nhập, Sổ địa chỉ         │    │
│  │  products/views.py   ← Danh mục, Lọc, Tìm kiếm tiếng Việt     │    │
│  │  cart/views.py       ← Giỏ hàng, Coupon, Freeship bar          │    │
│  │  orders/views.py     ← Checkout, Lịch sử đơn hàng              │    │
│  │  payments/views.py   ← Sinh mã VietQR, Upload biên lai         │    │
│  │  reviews/views.py    ← Đánh giá sản phẩm 1-5 sao               │    │
│  │  wishlists/views.py  ← Wishlist AJAX                            │    │
│  │  promotions/views.py ← Quản lý mã Coupon, Banner               │    │
│  │  pages/views.py      ← Trang Giới thiệu, Liên hệ               │    │
│  └──────────────────────────┬───────────────────────────────────────┘   │
│                             │                                            │
│  ┌──────────────────────────▼───────────────────────────────────────┐   │
│  │              Django Admin (Bảng điều khiển quản trị)             │   │
│  │  products/admin.py   ← Quản lý sản phẩm, danh mục, kho          │   │
│  │  orders/admin.py     ← Quản lý đơn hàng 7 trạng thái            │   │
│  │  payments/admin.py   ← Duyệt thanh toán, xem ảnh biên lai       │   │
│  │  promotions/admin.py ← Quản lý Coupon, Banner quảng cáo         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────────────┬───────────────┘
               │ Django ORM (SQL)                         │ HTTP GET Request
               ▼                                          ▼
┌──────────────────────────────────┐    ┌────────────────────────────────┐
│  CƠ SỞ DỮ LIỆU                  │    │  DỊCH VỤ NGOÀI (External)      │
│  SQLite — db.sqlite3             │    │                                │
│                                  │    │  VietQR API (Napas247)         │
│  accounts_user                   │    │  https://img.vietqr.io         │
│    → id, email, password_hash    │    │  Sinh mã QR thanh toán động   │
│    → full_name, phone, is_staff  │    │  Hỗ trợ: VCB, TCB, MB,        │
│                                  │    │  ACB, BIDV, VPBank, TPBank...  │
│  products_product                │    │                                │
│    → id, name, slug, base_price  │    └────────────────────────────────┘
│  products_category               │
│    → id, name, slug              │
│  products_productvariant         │
│    → id, product_id, color_id    │
│    → size_id, sku, stock         │
│                                  │
│  cart_cart                       │
│    → id, user_id, coupon_code    │
│  cart_cartitem                   │
│    → id, cart_id, variant_id     │
│    → quantity                    │
│                                  │
│  orders_order                    │
│    → id (UUID), order_number     │
│    → total, status, full_name    │
│  orders_orderitem                │
│    → id, order_id, variant_id    │
│    → quantity, unit_price        │
│                                  │
│  payments_payment                │
│    → id, order_id, amount        │
│    → bank_id, status             │
│    → receipt_image               │
│                                  │
│  reviews_review                  │
│    → id, product_id, user_id     │
│    → rating (1-5), body          │
│                                  │
│  wishlists_wishlist              │
│    → id, user_id                 │
│    → products (M2M)              │
│                                  │
│  promotions_coupon               │
│    → id, code, discount_type     │
│    → discount_value, valid_to    │
│  promotions_banner               │
│    → id, title, image, link      │
└──────────────────────────────────┘
```

---

## Luồng dữ liệu (Data Flow)

### Luồng 1: Khách hàng đặt hàng & thanh toán VietQR
```
Khách hàng
  → [FRONTEND] templates/orders/checkout.html (Tailwind CSS + Alpine.js)
  → [BACKEND] orders/views.py → checkout_view()
  → [DB] INSERT INTO orders_order + orders_orderitem (db.sqlite3)
  → [BACKEND] payments/views.py → payment_qr_view() → generate_vietqr()
  → [EXTERNAL] GET https://img.vietqr.io/image/{BANK_ID}-{ACCOUNT_NO}.png?amount=...
  → [FRONTEND] templates/payments/payment_qr.html → Hiển thị mã QR
  → Khách hàng quét mã → Upload ảnh biên lai
  → [DB] UPDATE payments_payment SET status='uploaded'
  → [BACKEND] Admin duyệt → UPDATE payments_payment SET status='confirmed'
  → [DB] UPDATE orders_order SET status='processing'
```

### Luồng 2: Đăng ký tài khoản
```
Khách hàng
  → [FRONTEND] templates/accounts/register.html
  → [BACKEND] accounts/views.py → register_view()
  → [DB] SELECT FROM accounts_user WHERE email=? → Kiểm tra trùng
  → [BACKEND] PBKDF2_SHA256(password) → Băm mật khẩu
  → [DB] INSERT INTO accounts_user → Lưu tài khoản mới
  → [FRONTEND] Redirect → templates/accounts/login.html
```

### Luồng 3: Tìm kiếm sản phẩm tiếng Việt
```
Khách hàng nhập từ khóa (có dấu hoặc không dấu)
  → [BACKEND] products/views.py → search_products() → remove_accents()
  → Tier 1: [DB] SELECT FROM products_product WHERE name ICONTAINS keyword
  → Tier 2 (nếu rỗng): [DB] SELECT FROM products_product WHERE description/category ICONTAINS keyword
  → [FRONTEND] templates/products/search_results.html → Hiển thị kết quả
```
