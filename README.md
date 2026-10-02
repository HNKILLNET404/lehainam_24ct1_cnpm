# 🛍️ Urban Threads — Website Thương Mại Điện Tử Thời Trang Streetwear

> **Đề tài:** Xây dựng website bán quần áo thời trang streetwear phong cách hiện đại  
> **Sinh viên thực hiện:** Lê Hải Nam  
> **MSSV:** 2451220069  
> **Lớp:** 24CT1 — Chuyên ngành Công Nghệ Phần Mềm  

---

## 📌 1. Giới thiệu dự án
**Urban Threads** là website thương mại điện tử chuyên kinh doanh các sản phẩm thời trang đường phố (Streetwear: Áo thun, Hoodie, Quần, Phụ kiện...).  
Hệ thống được xây dựng hoàn chỉnh với 2 phân hệ:
* **Khách hàng (Customer Portal):** Xem danh mục, tìm kiếm tiếng Việt thông minh 2 tầng, chọn size/màu sắc biến thể, giỏ hàng slide AJAX (Mini Cart Drawer), áp dụng mã giảm giá, kiểm tra ngưỡng miễn phí ship và thanh toán chuyển khoản quét mã **VietQR động** tích hợp mọi ngân hàng.
* **Quản trị viên (Admin Dashboard):** Quản lý sản phẩm, tồn kho SKU từng kích cỡ/màu sắc, duyệt đơn hàng 7 trạng thái, xem trước biên lai chuyển khoản và xác nhận thanh toán 1-click.

---

## 🛠️ 2. Công nghệ sử dụng
* **Backend:** Python 3.10+, **Django 5.1.1** (Kiến trúc MVT gồm 9 apps chuyên biệt: `accounts`, `products`, `cart`, `orders`, `payments`, `reviews`, `wishlists`, `promotions`, `pages`).
* **Frontend:** **Tailwind CSS** (CDN), **Alpine.js** (Reactive UI), HTML5, JavaScript ES6.
* **Cơ sở dữ liệu:** SQLite (Development) / Sẵn sàng cho PostgreSQL/MySQL.
* **Cổng thanh toán:** **VietQR API** (tương thích tất cả ngân hàng tại Việt Nam: VCB, TCB, MB, ACB, BIDV, VPBank, TPBank...).
* **Bảo mật:** CSRF protection, PBKDF2 Password Hashing, XSS & SQL Injection protection.

---

## 🚀 3. Hướng dẫn cài đặt & chạy thử nghiệm

### Bước 1: Clone dự án về máy
```bash
git clone https://github.com/HNKILLNET404/lehainam_24ct1_cnpm.git
cd lehainam_24ct1_cnpm
```

### Bước 2: Tạo và kích hoạt môi trường ảo
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 4: Chạy server
```bash
python manage.py runserver
```

Truy cập trang web tại: **`http://127.0.0.1:8000/`**  
Trang quản trị Admin: **`http://127.0.0.1:8000/admin/`**

---

## 🔐 4. Tài khoản quản trị & Dữ liệu mẫu
* **Tài khoản Admin:**
  * Email: `admin@urbanthreads.com`
  * Mật khẩu: ``
* **Mã giảm giá mẫu:**
  * `WELCOME10`: Giảm 10% đơn hàng
  * `GIAM50K`: Giảm 50.000đ cho đơn từ 300.000đ
  * *Tự động miễn phí ship (Freeship)* cho đơn từ 500.000đ trở lên.

---

## 📁 5. Tài liệu & Biểu đồ thiết kế
* File Slide PowerPoint khảo sát yêu cầu: `slide_khao_sat_yeu_cau_urban_threads.pptx`
* Sơ đồ phân tích Use Case & Lưu đồ toán học: trong thư mục `use_cases/`
* Sơ đồ quan hệ thực thể: `use_cases/er_diagram.mermaid`
