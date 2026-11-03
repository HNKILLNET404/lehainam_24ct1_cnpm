import urllib.request
import zlib
import base64
import os

def render_puml_to_png(puml_code, out_path):
    compressed = zlib.compress(puml_code.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    url = f'https://kroki.io/plantuml/png/{encoded}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as resp:
        with open(out_path, 'wb') as f:
            f.write(resp.read())
    print('Rendered:', out_path)

# 1. Use Case Chi tiết Thêm sản phẩm vào giỏ hàng
puml_uc_cart = """@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam packageStyle rectangle

actor "Khách hàng" as User

rectangle "Phân hệ Giỏ hàng (Cart Module)" {
    usecase "Xem chi tiết sản phẩm" as UC_Detail
    usecase "Chọn biến thể (Size / Màu sắc)" as UC_Variant
    usecase "Thêm sản phẩm vào giỏ hàng" as UC_AddToCart
    usecase "Kiểm tra tồn kho biến thể" as UC_CheckStock
    usecase "Cập nhật số lượng giỏ hàng" as UC_UpdateQty
    usecase "Xem nhanh giỏ hàng (Mini Cart)" as UC_MiniCart
    usecase "Áp dụng mã giảm giá (Coupon)" as UC_Coupon
    usecase "Kiểm tra tiến trình Freeship" as UC_Freeship
}

User --> UC_Detail
User --> UC_AddToCart
User --> UC_MiniCart

UC_AddToCart ..> UC_Variant : <<include>>
UC_AddToCart ..> UC_CheckStock : <<include>>
UC_AddToCart ..> UC_UpdateQty : <<include>>

UC_MiniCart <.. UC_Coupon : <<extend>>
UC_MiniCart ..> UC_Freeship : <<include>>
@enduml"""

# 2. Use Case Chi tiết Thanh toán đơn hàng & VietQR
puml_uc_pay = """@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam packageStyle rectangle

actor "Khách hàng" as User
actor "Hệ thống VietQR" as VietQR <<Service>>
actor "Quản trị viên (Admin)" as Admin

rectangle "Phân hệ Thanh toán & Đặt hàng (Checkout & Payment)" {
    usecase "Tiến hành đặt hàng (Checkout)" as UC_Checkout
    usecase "Nhập thông tin giao hàng & chọn ship" as UC_Address
    usecase "Tạo đơn hàng (Status: Pending)" as UC_CreateOrder
    usecase "Sinh mã VietQR động theo đơn" as UC_GenQR
    usecase "Quét mã QR chuyển khoản ngân hàng" as UC_ScanQR
    usecase "Tải lên biên lai giao dịch (Receipt)" as UC_UploadBill
    usecase "Duyệt thanh toán 1-click & xác nhận đơn" as UC_Approve
}

User --> UC_Checkout
User --> UC_ScanQR
User --> UC_UploadBill

UC_Checkout ..> UC_Address : <<include>>
UC_Checkout ..> UC_CreateOrder : <<include>>
UC_Checkout ..> UC_GenQR : <<include>>

UC_GenQR --> VietQR

Admin --> UC_Approve
UC_Approve ..> UC_UploadBill : <<include>>
@enduml"""

# 3. Use Case Tổng quan đẹp
puml_uc_overview = """@startuml
title BIỂU ĐỒ USE CASE TỔNG QUAN - HỆ THỐNG URBAN THREADS

left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 10
skinparam defaultFontName Arial
skinparam defaultFontSize 11

skinparam actor {
    BackgroundColor #FEF9E7
    BorderColor #D9531E
    FontSize 12
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #1A5276
    ArrowColor #2C3E50
    FontSize 11
}

actor "Khách vãng lai\\n(Guest)" as Guest
actor "Khách hàng\\n(Customer)" as Customer
actor "Quản trị viên\\n(Admin)" as Admin
actor "Hệ thống\\nVietQR" as VietQR <<Service>>

Customer -up-|> Guest

rectangle "Hệ Thống Website Thời Trang Urban Threads" {

    package "Tài khoản & Xác thực" {
        usecase "UC01: Đăng ký tài khoản" as UC_Register
        usecase "UC02: Đăng nhập / Đăng xuất" as UC_Login
        usecase "UC03: Quản lý hồ sơ cá nhân" as UC_Profile
        usecase "UC04: Quản lý sổ địa chỉ" as UC_Address
        usecase "UC05: Xem lịch sử đơn hàng" as UC_OrderHistory
    }

    package "Sản phẩm & Mua sắm" {
        usecase "UC06: Xem danh mục & Lọc sản phẩm" as UC_Browse
        usecase "UC07: Tìm kiếm tiếng Việt thông minh" as UC_Search
        usecase "UC08: Xem chi tiết & Biến thể SKU" as UC_Detail
        usecase "UC09: Thêm vào danh sách yêu thích" as UC_Wishlist
        usecase "UC10: Quản lý giỏ hàng & Mini Cart" as UC_Cart
        usecase "UC11: Áp dụng mã giảm giá (Coupon)" as UC_Coupon
        usecase "UC12: Đặt hàng (Checkout)" as UC_Checkout
        usecase "UC13: Quét mã thanh toán VietQR" as UC_PayQR
        usecase "UC14: Tải lên biên lai chuyển khoản" as UC_Receipt
    }

    package "Quản trị Hệ thống (Admin Dashboard)" {
        usecase "UC15: Quản lý danh mục & sản phẩm" as UC_AdminProduct
        usecase "UC16: Quản lý biến thể & tồn kho SKU" as UC_AdminStock
        usecase "UC17: Quản lý & Cập nhật đơn hàng" as UC_AdminOrder
        usecase "UC18: Duyệt thanh toán & Đối soát bill" as UC_AdminPayment
        usecase "UC19: Quản lý khuyến mãi & Banner" as UC_AdminPromo
    }
}

Guest --> UC_Register
Guest --> UC_Login
Guest --> UC_Browse
Guest --> UC_Search
Guest --> UC_Detail
Guest --> UC_Cart

Customer --> UC_Profile
Customer --> UC_Address
Customer --> UC_OrderHistory
Customer --> UC_Wishlist
Customer --> UC_Checkout

UC_Cart <.. UC_Coupon : <<extend>>
UC_Checkout ..> UC_PayQR : <<include>>
UC_Checkout ..> UC_Receipt : <<include>>
UC_PayQR --> VietQR

Admin --> UC_AdminProduct
Admin --> UC_AdminStock
Admin --> UC_AdminOrder
Admin --> UC_AdminPayment
Admin --> UC_AdminPromo

@enduml"""

os.makedirs('D:/urban-threads/use_cases', exist_ok=True)
render_puml_to_png(puml_uc_cart, 'D:/urban-threads/use_cases/usecase_them_gio_hang.png')
render_puml_to_png(puml_uc_pay, 'D:/urban-threads/use_cases/usecase_thanh_toan.png')
render_puml_to_png(puml_uc_overview, 'D:/urban-threads/use_cases/usecase_tong_quan.png')
print('All Use Case diagrams rendered successfully!')
