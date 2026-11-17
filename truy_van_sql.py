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

print("=" * 80)
print(f"  KẾT NỐI CƠ SỞ DỮ LIỆU: {os.path.basename(DB_PATH)}")
print("  TRUY VẤN PHÂN QUYỀN: ADMIN - NHÂN VIÊN - KHÁCH HÀNG (ĐÃ TÁCH BẠCH)")
print("=" * 80)

# 1. Truy vấn thống kê theo cột role (Cách 1 - Chuẩn CSDL hiện đại)
sql_by_role = """
SELECT 
    COUNT(*) AS tong_tai_khoan,
    SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) AS tong_admin,
    SUM(CASE WHEN role = 'staff' THEN 1 ELSE 0 END) AS tong_nhan_vien,
    SUM(CASE WHEN role = 'customer' THEN 1 ELSE 0 END) AS tong_khach_hang
FROM accounts_user;
"""
cur.execute(sql_by_role)
r_total, r_admin, r_staff, r_cust = cur.fetchone()

# 2. Truy vấn thống kê theo cờ boolean (Cách 2 - Hết trùng 1)
# Admin: is_superuser = 1 (is_staff = 0)
# Nhân viên: is_staff = 1 (is_superuser = 0)
# Khách hàng: is_staff = 0 AND is_superuser = 0
sql_by_flags = """
SELECT 
    COUNT(*) AS tong_tai_khoan,
    SUM(CASE WHEN is_superuser = 1 THEN 1 ELSE 0 END) AS tong_admin,
    SUM(CASE WHEN is_staff = 1 THEN 1 ELSE 0 END) AS tong_nhan_vien,
    SUM(CASE WHEN is_staff = 0 AND is_superuser = 0 THEN 1 ELSE 0 END) AS tong_khach_hang
FROM accounts_user;
"""
cur.execute(sql_by_flags)
f_total, f_admin, f_staff, f_cust = cur.fetchone()

print("\n[1] CÁC CÂU LỆNH SQL ĐỂ TRẢ LỜI GIẢNG VIÊN:")
print("-" * 80)
print("  CÁCH 1: TRUY VẤN THEO CỘT `role` (RÕ RÀNG NHẤT, CHUẨN THIẾT KẾ CSDL):")
print("    -- Tìm & Đếm Quản trị viên (Admin):")
print("    SELECT COUNT(*) AS tong_admin FROM accounts_user WHERE role = 'admin';")
print("    -- Tìm & Đếm Nhân viên (Staff):")
print("    SELECT COUNT(*) AS tong_nhan_vien FROM accounts_user WHERE role = 'staff';")
print("    -- Tìm & Đếm Khách hàng (Customer):")
print("    SELECT COUNT(*) AS tong_khach_hang FROM accounts_user WHERE role = 'customer';")

print("\n  CÁCH 2: TRUY VẤN THEO 2 CỘT PHÂN QUYỀN BOOLEAN (HẾT BỊ TRÙNG 1):")
print("    -- Admin: is_superuser = 1 (duy nhất Admin có giá trị 1)")
print("    SELECT COUNT(*) AS tong_admin FROM accounts_user WHERE is_superuser = 1;")
print("    -- Nhân viên: is_staff = 1 (duy nhất Nhân viên có giá trị 1, không cần AND nữa!)")
print("    SELECT COUNT(*) AS tong_nhan_vien FROM accounts_user WHERE is_staff = 1;")
print("    -- Khách hàng: Cả 2 cột đều mang giá trị 0")
print("    SELECT COUNT(*) AS tong_khach_hang FROM accounts_user WHERE is_staff = 0 AND is_superuser = 0;")

print("\n[2] KẾT QUẢ THỐNG KÊ TÀI KHOẢN TRONG DATABASE:")
print(f"    + Tổng tất cả tài khoản : {r_total}")
print(f"    + 👑 Tổng Admin         : {r_admin}")
print(f"    + 👔 Tổng Nhân viên     : {r_staff}")
print(f"    + 👤 Tổng Khách hàng    : {r_cust}")

# 3. Chi tiết từng tài khoản trong CSDL
print("\n[3] BẢNG DỮ LIỆU THỰC TẾ TRONG `accounts_user` (XEM TRONG DB BROWSER):")
print(f"    {'ID':<4} | {'Username':<18} | {'Email':<26} | {'is_super':<8} | {'is_staff':<8} | {'role':<10} | {'Vai trò thực tế'}")
print("    " + "-" * 98)
cur.execute("""
    SELECT id, username, email, is_superuser, is_staff, role
    FROM accounts_user 
    ORDER BY id ASC;
""")
for uid, username, email, is_sup, is_stf, role in cur.fetchall():
    if role == 'admin' or is_sup == 1:
        vtro = "👑 Admin Quản trị"
    elif role == 'staff' or is_stf == 1:
        vtro = "👔 Nhân viên (Staff)"
    else:
        vtro = "👤 Khách hàng"
    print(f"    {uid:<4} | {username:<18} | {email:<26} | {is_sup:<8} | {is_stf:<8} | {role:<10} | {vtro}")

print("\n" + "=" * 80)
conn.close()
