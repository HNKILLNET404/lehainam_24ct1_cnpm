# URBAN THREADS — System Architecture
# =====================================
# PHIA TRUOC (Frontend):
#   - Framework CSS  : Tailwind CSS v3 (CDN)
#   - Framework JS   : Alpine.js v3 (CDN)
#   - Template Engine: Django Template Language (DTL)
#   - Files          : templates/ directory (HTML files)
#
# PHIA SAU (Backend):
#   - Framework : Django 5.1.1
#   - Language  : Python 3.10+
#   - Pattern   : MVT (Model - View - Template)
#   - Apps      : accounts, products, cart, orders,
#                 payments, reviews, wishlists, promotions, pages
#
# CO SO DU LIEU (Database):
#   - DBMS  : SQLite
#   - File  : db.sqlite3
#   - Tables:
#       accounts_user              (nguoi dung)
#       products_product           (san pham)
#       products_category          (danh muc)
#       products_productvariant    (bien the SKU)
#       cart_cart                  (gio hang)
#       cart_cartitem              (chi tiet gio hang)
#       orders_order               (don hang)
#       orders_orderitem           (chi tiet don hang)
#       payments_payment           (thanh toan VietQR)
#       reviews_review             (danh gia sao)
#       wishlists_wishlist         (yeu thich)
#       promotions_coupon          (ma giam gia)
#       promotions_banner          (banner quang cao)
#
# DICH VU NGOAI (External Service):
#   - VietQR API (Napas247): https://img.vietqr.io
#   - Ho tro: VCB, TCB, MB, ACB, BIDV, VPBank, TPBank...
