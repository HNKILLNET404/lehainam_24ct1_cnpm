# -*- coding: utf-8 -*-
"""
SCRIPT TRUY VẤN TRỰC TIẾP CƠ SỞ DỮ LIỆU: urban_threads.sqlite3
Chạy lệnh: python truy_van_sql.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "urban_threads.sqlite3")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=" * 75)
print(f"  KẾT NỐI CƠ SỞ DỮ LIỆU: {os.path.basename(DB_PATH)}")
print("=" * 75)

# 1. Truy vấn tổng hợp số lượng Admin, Nhân viên, Khách hàng
sql_summary = """
SELECT 
    COUNT(*) AS tong_tai_khoan,
    SUM(CASE WHEN is_superuser = 1 THEN 1 ELSE 0 END) AS tong_admin,
    SUM(CASE WHEN is_staff = 1 AND is_superuser = 0 THEN 1 ELSE 0 END) AS tong_nhan_vien,
    SUM(CASE WHEN is_staff = 0 AND is_superuser = 0 THEN 1 ELSE 0 END) AS tong_khach_hang
FROM accounts_user;
"""
cur.execute(sql_summary)
total_all, total_admin, total_staff, total_cust = cur.fetchone()

print("\n[1] CÂU LỆNH SQL TRUY VẤN TỔNG ADMIN / NHÂN VIÊN / KHÁCH HÀNG:")
print("    -- Đếm Tổng Admin:")
print("    SELECT COUNT(*) AS tong_admin FROM accounts_user WHERE is_superuser = 1;")
print("    -- Đếm Tổng Nhân viên (Staff):")
print("    SELECT COUNT(*) AS tong_nhan_vien FROM accounts_user WHERE is_staff = 1 AND is_superuser = 0;")
print("    -- Đếm Tổng Khách hàng:")
print("    SELECT COUNT(*) AS tong_khach_hang FROM accounts_user WHERE is_staff = 0 AND is_superuser = 0;")

print("\n[2] KẾT QUẢ THỐNG KÊ TÀI KHOẢN TRONG DATABASE (urban_threads.sqlite3):")
print(f"    + Tổng tất cả tài khoản : {total_all}")
print(f"    + 👑 Tổng Admin         : {total_admin}")
print(f"    + 👔 Tổng Nhân viên     : {total_staff}")
print(f"    + 👤 Tổng Khách hàng    : {total_cust}")

# 2. Chi tiết từng tài khoản
print("\n[3] DANH SÁCH CHI TIẾT BẢNG accounts_user:")
print(f"    {'ID':<4} | {'Email':<30} | {'Họ tên':<20} | {'Vai trò'}")
print("    " + "-" * 70)
cur.execute("""
    SELECT id, email, first_name || ' ' || last_name, is_superuser, is_staff 
    FROM accounts_user 
    ORDER BY is_superuser DESC, is_staff DESC, id ASC;
""")
for uid, email, fullname, is_super, is_stf in cur.fetchall():
    role = "Admin Quản trị" if is_super else ("Nhân viên (Staff)" if is_stf else "Khách hàng")
    print(f"    {uid:<4} | {email:<30} | {fullname.strip():<20} | {role}")

# 3. Thống kê Sản phẩm & Đơn hàng
cur.execute("SELECT COUNT(*), SUM(stock) FROM products_product JOIN products_productvariant ON products_product.id = products_productvariant.product_id;")
prod_row = cur.fetchone()
cur.execute("SELECT COUNT(*) FROM products_product;")
total_products = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM orders_order;")
total_orders = cur.fetchone()[0]

print("\n[4] THỐNG KÊ SẢN PHẨM & ĐƠN HÀNG:")
print(f"    + Tổng số mẫu Sản phẩm (products_product) : {total_products}")
print(f"    + Tổng số lượng Tồn kho (stock)           : {prod_row[1] or 0}")
print(f"    + Tổng số Đơn hàng (orders_order)         : {total_orders}")
print("=" * 75)

conn.close()
