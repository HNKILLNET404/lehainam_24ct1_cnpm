import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

from report_builder_helpers import (
    set_cell_background, set_cell_margins, set_cell_borders,
    format_paragraph, add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet_p, add_image_safe, add_screenshot_placeholder
)

doc = docx.Document()

# ==================== PAGE SETUP ====================
section = doc.sections[0]
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(3.0)   # 3cm le trai chuan dong gay
section.right_margin = Cm(2.0)  # 2cm le phai
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)

# Set Normal style
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(13)
style_normal.font.color.rgb = RGBColor(0, 0, 0)
style_normal.paragraph_format.line_spacing = 1.5
style_normal.paragraph_format.space_after = Pt(6)

# =========================================================================
# TRANG BÌA (COVER PAGE)
# =========================================================================
p = doc.add_paragraph()
format_paragraph(p, space_before=0, space_after=2, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.CENTER)
r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC KIẾN TRÚC ĐÀ NẴNG\nKHOA CÔNG NGHỆ THÔNG TIN\n-------------------- *** --------------------")
r.font.name = "Times New Roman"
r.font.size = Pt(13)
r.font.bold = True

# Logo
logo_path = 'D:/urban-threads/use_cases/logo_truong.jpg'
if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(16)
    p_logo.paragraph_format.space_after = Pt(16)
    r_logo = p_logo.add_run()
    r_logo.add_picture(logo_path, width=Inches(2.0))

# Tiêu đề báo cáo
p_title = doc.add_paragraph()
format_paragraph(p_title, space_before=10, space_after=6, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.CENTER)
r_rep = p_title.add_run("BÁO CÁO HỌC PHẦN\nMÔN: CÔNG NGHỆ PHẦN MỀM\n\n")
r_rep.font.name = "Times New Roman"
r_rep.font.size = Pt(16)
r_rep.font.bold = True
r_rep.font.color.rgb = RGBColor(15, 23, 42)

r_sub = p_title.add_run("ĐỀ TÀI:\nXÂY DỰNG HỆ THỐNG QUẢN LÝ THÔNG TIN WEBSITE BÁN QUẦN ÁO THỜI TRANG STREETWEAR URBAN THREADS")
r_sub.font.name = "Times New Roman"
r_sub.font.size = Pt(15)
r_sub.font.bold = True
r_sub.font.color.rgb = RGBColor(194, 65, 12) # Cam gach noi bat

# Thông tin sinh viên & giảng viên
p_info = doc.add_paragraph()
format_paragraph(p_info, space_before=24, space_after=30, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.LEFT)
p_info.paragraph_format.left_indent = Inches(1.5)

info_lines = [
    ("Giảng viên hướng dẫn:  ", "ThS. Phạm Thị Dung"),
    ("Sinh viên thực hiện:      ", "Lê Hải Nam"),
    ("Mã số sinh viên (MSSV): ", "2451220069"),
    ("Lớp:                              ", "24CT1"),
    ("Khoa:                            ", "Công Nghệ Thông Tin"),
]
for label, val in info_lines:
    r_lbl = p_info.add_run(label)
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(13)
    r_lbl.font.bold = True
    r_val = p_info.add_run(val + "\n")
    r_val.font.name = "Times New Roman"
    r_val.font.size = Pt(13)

# Địa điểm & thời gian
p_date = doc.add_paragraph()
format_paragraph(p_date, space_before=20, space_after=0, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.CENTER)
r_d = p_date.add_run("Đà Nẵng, tháng 11 năm 2026")
r_d.font.name = "Times New Roman"
r_d.font.size = Pt(12.5)
r_d.font.italic = True

doc.add_page_break()

# =========================================================================
# LỜI NÓI ĐẦU
# =========================================================================
p = add_heading_1(doc, "LỜI NÓI ĐẦU")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_body_p(doc, "Trong thời đại chuyển đổi số và bùng nổ của thương mại điện tử toàn cầu, phương thức mua sắm của người tiêu dùng — đặc biệt là thế hệ trẻ Gen Z và Millennials — đã có những bước chuyển biến sâu sắc. Thay vì mua sắm trực tiếp truyền thống, người tiêu dùng ngày nay ưu tiên các nền tảng trực tuyến với khả năng tra cứu thông tin nhanh chóng, so sánh mẫu mã, lựa chọn biến thể kích cỡ và thanh toán linh hoạt chỉ qua vài thao tác đơn giản trên thiết bị thông minh. Đối với ngành công nghiệp thời trang đường phố (Streetwear), website không đơn thuần là một kênh giới thiệu sản phẩm mà còn là nơi thể hiện bản sắc thương hiệu, văn hóa lối sống và kết nối cộng đồng người tiêu dùng trẻ tuổi.")

add_body_p(doc, "Xuất phát từ nhu cầu thực tiễn đó, trong khuôn khổ học phần Công nghệ phần mềm dưới sự giảng dạy tận tình của cô Phạm Thị Dung, em đã lựa chọn và thực hiện đề tài: \"Xây dựng hệ thống quản lý thông tin Website bán áo thời trang Urban Threads\". Dự án tập trung nghiên cứu, thiết kế và phát triển một nền tảng thương mại điện tử hoàn chỉnh theo mô hình MVT (Model - View - Template) sử dụng ngôn ngữ Python và framework Django 5.x, kết hợp thiết kế giao diện hiện đại với Tailwind CSS và Alpine.js. Đặc biệt, hệ thống tích hợp giải pháp thanh toán chuyển khoản ngân hàng quét mã VietQR động hỗ trợ đa ngân hàng tại Việt Nam, cùng công cụ tìm kiếm tiếng Việt thông minh và hệ thống quản trị kiểm soát đơn hàng, tồn kho trực quan 1-click.")

add_body_p(doc, "Đề tài này là cơ hội quý báu giúp em củng cố kiến thức nền tảng về vòng đời phát triển phần mềm (SDLC), từ giai đoạn khảo sát yêu cầu, xây dựng luồng người dùng (User Flow), mô hình hóa Use Case, biểu đồ tuần tự (Sequence Diagram) cho đến lập trình thực nghiệm và kiểm thử. Em xin gửi lời cảm ơn chân thành đến cô Phạm Thị Dung đã truyền đạt kiến thức và đồng hành hướng dẫn em trong suốt quá trình hoàn thành báo cáo này.")

doc.add_page_break()

# =========================================================================
# MỤC LỤC
# =========================================================================
p_ml = add_heading_1(doc, "MỤC LỤC")
p_ml.alignment = WD_ALIGN_PARAGRAPH.CENTER

toc_items = [
    ("LỜI NÓI ĐẦU", "2"),
    ("MỤC LỤC", "3"),
    ("CHƯƠNG 1: TỔNG QUAN CƠ SỞ LÝ THUYẾT & THIẾT KẾ LUỒNG", "4"),
    ("    1.1. Giới thiệu và cài đặt về công nghệ, ngôn ngữ, dữ liệu", "4"),
    ("        1.1.1. Giới thiệu ngôn ngữ Python và Framework Django 5.x", "4"),
    ("        1.1.2. Công nghệ xây dựng giao diện Tailwind CSS và Alpine.js", "5"),
    ("        1.1.3. Hệ thống cơ sở dữ liệu và Cổng thanh toán VietQR", "6"),
    ("        1.1.4. Hướng dẫn chi tiết cài đặt môi trường thực hiện đề tài", "7"),
    ("    1.2. Phân tích yêu cầu hệ thống đề tài", "8"),
    ("        1.2.1. Khảo sát các website tham khảo thực tế", "8"),
    ("        1.2.2. Bảng phân tích yêu cầu chức năng (Functional Requirements)", "9"),
    ("        1.2.3. Bảng phân tích yêu cầu phi chức năng (Non-Functional Requirements)", "11"),
    ("        1.2.4. Mô hình toán học và giải thuật (Đăng ký & Đăng nhập)", "12"),
    ("    1.3. Thiết kế luồng người dùng (User Flow - Bước 1 Thiết kế phần mềm)", "13"),
    ("        1.3.1. Luồng người dùng chức năng Đăng ký tài khoản (Register Flow)", "13"),
    ("        1.3.2. Luồng người dùng chức năng Đăng nhập hệ thống (Login Flow)", "14"),
    ("        1.3.3. Luồng người dùng chức năng Thêm sản phẩm vào giỏ hàng (Cart Flow)", "15"),
    ("        1.3.4. Luồng người dùng chức năng Thanh toán đơn hàng qua VietQR", "16"),
    ("        1.3.5. Tổng hợp 4 luồng người dùng chính trên bảng thiết kế FigJam", "17"),
    ("CHƯƠNG 2: BIỂU ĐỒ VÀ THIẾT KẾ HỆ THỐNG", "18"),
    ("    2.1. Biểu đồ Use Case", "18"),
    ("        2.1.1. Biểu đồ Use Case tổng quan hệ thống Urban Threads", "18"),
    ("        2.1.2. Biểu đồ Use Case chi tiết chức năng Thêm sản phẩm vào giỏ hàng", "19"),
    ("        2.1.3. Biểu đồ Use Case chi tiết chức năng Thanh toán đơn hàng qua VietQR", "20"),
    ("    2.2. Biểu đồ tuần tự (Sequence Diagram)", "21"),
    ("        2.2.1. Biểu đồ tuần tự chức năng Đăng ký tài khoản", "21"),
    ("        2.2.2. Biểu đồ tuần tự chức năng Đăng nhập", "22"),
    ("        2.2.3. Biểu đồ tuần tự chức năng Thêm sản phẩm vào giỏ hàng", "23"),
    ("        2.2.4. Biểu đồ tuần tự chức năng Thanh toán đơn hàng và Đối soát VietQR", "24"),
    ("    2.3. Sơ đồ cơ sở dữ liệu (ER Diagram)", "25"),
    ("CHƯƠNG 3: TRÌNH BÀY DEMO HỆ THỐNG", "26"),
    ("    3.1. Giao diện Trang chủ và Danh mục sản phẩm", "26"),
    ("    3.2. Giao diện Đăng nhập, Đăng ký và Tìm kiếm thông minh", "27"),
    ("    3.3. Trang chi tiết sản phẩm và chọn biến thể (Size / Màu)", "28"),
    ("    3.4. Giỏ hàng và Ngăn kéo giỏ hàng (Mini Cart Drawer)", "29"),
    ("    3.5. Trang thanh toán và Cổng quét mã VietQR tự động", "30"),
    ("    3.6. Trang quản trị Admin Dashboard", "31"),
    ("    3.7. Kế hoạch triển khai dự án (Gantt Chart)", "32"),
    ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "33"),
    ("LỜI CẢM ƠN", "34")
]

for title, page in toc_items:
    p_t = doc.add_paragraph()
    format_paragraph(p_t, space_before=1, space_after=3, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.LEFT)
    r_tit = p_t.add_run(title)
    r_tit.font.name = "Times New Roman"
    r_tit.font.size = Pt(12)
    if "CHƯƠNG" in title or title in ["LỜI NÓI ĐẦU", "MỤC LỤC", "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "LỜI CẢM ƠN"]:
        r_tit.font.bold = True
    
    # Dot leader
    dots_len = max(5, 75 - len(title))
    r_dot = p_t.add_run(" " + "." * dots_len + " ")
    r_dot.font.name = "Times New Roman"
    r_dot.font.size = Pt(11)
    r_dot.font.color.rgb = RGBColor(148, 163, 184)
    
    r_pg = p_t.add_run(page)
    r_pg.font.name = "Times New Roman"
    r_pg.font.size = Pt(12)
    r_pg.font.bold = True

doc.add_page_break()

# =========================================================================
# CHƯƠNG 1: TỔNG QUAN CƠ SỞ LÝ THUYẾT & THIẾT KẾ LUỒNG
# =========================================================================
add_heading_1(doc, "CHƯƠNG 1: TỔNG QUAN CƠ SỞ LÝ THUYẾT & THIẾT KẾ LUỒNG")

add_heading_2(doc, "1.1. GIỚI THIỆU VÀ CÀI ĐẶT VỀ CÔNG NGHỆ, NGÔN NGỮ, DỮ LIỆU")

add_heading_3(doc, "1.1.1. GIỚI THIỆU NGÔN NGỮ PYTHON VÀ FRAMEWORK DJANGO 5.X")
add_body_p(doc, "Python là một trong những ngôn ngữ lập trình bậc cao phổ biến nhất hiện nay nhờ cú pháp rõ ràng, súc tích, thư viện tiêu chuẩn đồ sộ và khả năng áp dụng rộng rãi từ lập trình web, tự động hóa cho đến trí tuệ nhân tạo. Trên nền tảng Python, Django là framework phát triển web hàng đầu, được xây dựng theo triết lý \"Batteries-included\" — cung cấp sẵn hầu như toàn bộ các công cụ và linh kiện cần thiết để xây dựng một ứng dụng web hoàn chỉnh từ quy mô nhỏ đến cấp doanh nghiệp.")

add_body_p(doc, "Django hoạt động theo kiến trúc MVT (Model - View - Template), một biến thể hiện đại của mô hình MVC truyền thống:")
add_bullet_p(doc, "Chịu trách nhiệm định nghĩa cấu trúc dữ liệu và logic nghiệp vụ. Django ORM (Object-Relational Mapping) cho phép lập trình viên thao tác với bảng dữ liệu hoàn toàn bằng các đối tượng Python, không cần phải viết các câu lệnh SQL thủ công, giúp tăng tốc độ phát triển và ngăn chặn triệt để lỗ hổng SQL Injection.", "• Model (Mô hình dữ liệu): ")
add_bullet_p(doc, "Tiếp nhận yêu cầu HTTP từ người dùng thông qua URL dispatcher, tương tác với tầng Model để truy vấn hoặc cập nhật dữ liệu, xử lý nghiệp vụ bán hàng (thêm giỏ, áp coupon, sinh mã QR) và chuyển dữ liệu sang Template để hiển thị.", "• View (Tầng điều khiển / Xử lý nghiệp vụ): ")
add_bullet_p(doc, "Sử dụng Django Template Language (DTL) để kết hợp mã HTML với các biến, bộ lọc định dạng tiền tệ (filters) và thẻ điều kiện (tags) nhằm kết xuất ra giao diện động gửi về cho trình duyệt của khách hàng.", "• Template (Tầng trình bày giao diện): ")

add_body_p(doc, "Các ưu điểm vượt trội của Django 5.x được khai thác trong đề tài:")
add_body_p(doc, "1. Hệ thống xác thực và phân quyền người dùng (Authentication System) tích hợp sẵn, hỗ trợ phân chia nhóm quyền quản trị (Superuser, Staff) và khách hàng.")
add_body_p(doc, "2. Giao diện quản trị tự động Django Admin cực kỳ mạnh mẽ, cho phép cấu hình tùy biến bộ lọc, tìm kiếm, hiển thị ảnh xem trước và thao tác hàng loạt.")
add_body_p(doc, "3. Cơ chế bảo mật đa lớp: Tự động gắn thẻ CSRF token chống giả mạo request, bảo vệ chống XSS (Cross-Site Scripting), Clickjacking và cơ chế băm mật khẩu chuẩn PBKDF2 với thuật toán SHA-256.")

add_heading_3(doc, "1.1.2. CÔNG NGHỆ XÂY DỰNG GIAO DIỆN TAILWIND CSS VÀ ALPINE.JS")
add_body_p(doc, "Giao diện người dùng của website Urban Threads được thiết kế theo phong cách thời trang đường phố (Streetwear Monochrome) tối giản và hiện đại, sử dụng hai công nghệ frontend tiên tiến:")
add_bullet_p(doc, "Framework CSS theo xu hướng Utility-First, cung cấp hàng ngàn lớp tiện ích dựng sẵn giúp lập trình viên tùy biến giao diện trực tiếp ngay trong mã HTML mà không cần phải viết các tệp CSS riêng lẻ cồng kềnh. Tailwind CSS mang lại khả năng đáp ứng (Responsive Design) hoàn hảo trên tất cả kích thước màn hình từ điện thoại thông minh, máy tính bảng đến máy tính để bàn.", "• Tailwind CSS: ")
add_bullet_p(doc, "Thư viện JavaScript siêu nhẹ (chỉ khoảng 15KB) nhưng mang đầy đủ tính năng phản ứng (Reactive) tương tự Vue.js hoặc React. Trong đề tài, Alpine.js được sử dụng để điều khiển các thành phần tương tác tức thì: Ngăn kéo giỏ hàng trượt ra từ bên phải màn hình (Mini Cart Drawer), bộ chuyển đổi biến thể sản phẩm (đổi màu, chọn size tự động đổi giá và kiểm tra tồn kho), bộ đếm thông báo Toast và xem phóng to ảnh sản phẩm.", "• Alpine.js: ")

add_heading_3(doc, "1.1.3. HỆ THỐNG CƠ SỞ DỮ LIỆU VÀ CỔNG THANH TOÁN VIETQR")
add_bullet_p(doc, "Hệ thống sử dụng cơ sở dữ liệu SQLite trong môi trường phát triển và thử nghiệm nhờ ưu điểm nhỏ gọn, không cần cấu hình server riêng và tệp cơ sở dữ liệu được lưu trực tiếp tại db.sqlite3 trong thư mục gốc. Thông qua Django ORM, hệ thống hoàn toàn sẵn sàng chuyển đổi sang các hệ quản trị cơ sở dữ liệu mạnh mẽ như PostgreSQL hoặc MySQL khi triển khai thực tế trên máy chủ đám mây.", "• Cơ sở dữ liệu SQLite: ")
add_bullet_p(doc, "Nhằm bắt kịp xu hướng thanh toán không dùng tiền mặt tại Việt Nam, đề tài xây dựng module tích hợp chuẩn VietQR (Napas247). Khi khách hàng đặt hàng, hệ thống tự động sinh mã QR chứa đúng số tài khoản thụ hưởng, số tiền chính xác của đơn hàng và cú pháp chuyển khoản DHxxxxxxxx. Hệ thống cho phép cấu hình linh hoạt sang bất kỳ ngân hàng nào tại Việt Nam (Vietcombank, Techcombank, MB Bank, ACB, BIDV, VPBank...) thông qua tệp môi trường .env mà không cần sửa đổi mã nguồn.", "• Cổng thanh toán VietQR động: ")

add_heading_3(doc, "1.1.4. HƯỚNG DẪN CHI TIẾT CÀI ĐẶT MÔI TRƯỜNG THỰC HIỆN ĐỀ TÀI")
add_body_p(doc, "Để triển khai và vận hành website Urban Threads trên môi trường cục bộ, các bước thực hiện như sau:")
add_body_p(doc, "• Bước 1: Cài đặt Python: Tải và cài đặt Python phiên bản 3.10 trở lên từ trang chủ python.org. Chú ý đánh dấu vào tùy chọn \"Add Python to PATH\" trước khi bấm Install.")
add_body_p(doc, "• Bước 2: Mở thư mục dự án: Mở cửa sổ dòng lệnh (Command Prompt hoặc PowerShell) và điều hướng đến thư mục dự án: cd D:\\urban-threads")
add_body_p(doc, "• Bước 3: Tạo môi trường ảo (Virtual Environment): Tạo môi trường ảo độc lập để cô lập các gói thư viện: python -m venv venv")
add_body_p(doc, "• Bước 4: Kích hoạt môi trường ảo: Kích hoạt môi trường ảo: venv\\Scripts\\activate (Trên thanh dòng lệnh sẽ xuất hiện tiền tố (venv)).")
add_body_p(doc, "• Bước 5: Cài đặt các thư viện phụ thuộc: Cài đặt toàn bộ các thư viện được định nghĩa trong tệp requirements.txt bằng lệnh: pip install -r requirements.txt (gồm Django, Pillow, qrcode, python-decouple, django-crispy-forms, crispy-tailwind...).")
add_body_p(doc, "• Bước 6: Khởi chạy máy chủ phát triển: Chạy lệnh: python manage.py runserver. Truy cập website tại địa chỉ http://127.0.0.1:8000/ và trang quản trị tại http://127.0.0.1:8000/admin/.")

add_heading_2(doc, "1.2. PHÂN TÍCH YÊU CẦU HỆ THỐNG ĐỀ TÀI")

add_heading_3(doc, "1.2.1. KHẢO SÁT CÁC WEBSITE THAM KHẢO THỰC TẾ")
add_body_p(doc, "Để đảm bảo hệ thống vừa đáp ứng đầy đủ tính năng thương mại điện tử chuyên nghiệp, vừa mang phong cách thẩm mỹ thời thượng của ngành thời trang đường phố, dự án đã tiến hành khảo sát và chắt lọc kinh nghiệm từ 3 website thương mại điện tử hàng đầu:")
add_body_p(doc, "1. Chivalry Warehouse (https://chivalry-warehouse.com/): Local brand streetwear nổi tiếng tại Việt Nam với phong cách Rock & Grunge độc đáo. Đề tài học hỏi thiết kế thanh điều hướng cố định (Sticky Header), cách phân loại danh mục sản phẩm thời trang (Áo thun, Hoodie, Quần, Phụ kiện, Sale), các nhãn dán trạng thái sản phẩm (New Arrival, Best Seller, Sale) và bộ chọn thuộc tính biến thể màu sắc (Color swatches) trực quan.")
add_body_p(doc, "2. Represent Clo (https://representclo.com/): Thương hiệu thời trang đường phố cao cấp hàng đầu Vương Quốc Anh (UK High-end Streetwear). Đề tài học hỏi phong cách thiết kế Monochrome tối giản sang trọng, bố cục lưới sản phẩm thông thoáng, thư viện ảnh gallery chi tiết nhiều góc chụp, bảng hướng dẫn chọn kích cỡ (Size Guide) và khu vực gợi ý sản phẩm liên quan (Related Products).")
add_body_p(doc, "3. Culture Kings (https://culturekings.com.au/): Chuỗi bán lẻ streetwear và sneakers quy mô lớn nhất Australia. Đề tài học hỏi và triển khai tính năng Ngăn kéo giỏ hàng trượt ra từ bên phải màn hình (Mini Cart Drawer) mà không cần tải lại trang, thanh tiến trình miễn phí vận chuyển (Free shipping progress bar đạt mốc 500.000đ), cơ chế lọc sản phẩm đa tiêu chí và bộ tìm kiếm thông minh.")

add_heading_3(doc, "1.2.2. BẢNG PHÂN TÍCH YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS - FR)")
add_body_p(doc, "Các yêu cầu chức năng của hệ thống Urban Threads được phân chia và quản lý chi tiết qua bảng tiêu chuẩn dưới đây:")

# Table FR
fr_data = [
    ("Mã", "Tên yêu cầu", "Mô tả yêu cầu", "Ưu tiên", "Tiêu chí nghiệm thu", "Tình trạng"),
    ("FR-01", "Đăng ký tài khoản", "Người dùng đăng ký tài khoản mới bằng Email và mật khẩu bảo mật.", "Cao", "Nhập đúng thông tin tạo tài khoản thành công; trùng email báo lỗi.", "Hoàn thành"),
    ("FR-02", "Đăng nhập / Đăng xuất", "Người dùng đăng nhập bằng Email/Password, có ghi nhớ phiên và đăng xuất an toàn.", "Cao", "Đăng nhập đúng vào trang chủ; sai mật khẩu báo lỗi; hủy session an toàn.", "Hoàn thành"),
    ("FR-03", "Sổ địa chỉ giao hàng", "Người dùng quản lý nhiều địa chỉ nhận hàng (thêm, sửa, xóa, mặc định).", "Trung bình", "Dữ liệu lưu vào tài khoản; tự động điền địa chỉ mặc định khi đặt hàng.", "Hoàn thành"),
    ("FR-04", "Lịch sử đơn hàng", "Người dùng theo dõi danh sách đơn hàng đã mua và tiến trình 5 bước.", "Cao", "Hiển thị mã đơn DHxxxx, danh sách sản phẩm, giá tiền và trạng thái.", "Hoàn thành"),
    ("FR-05", "Duyệt danh mục & Lọc", "Phân loại sản phẩm (Áo, Quần, Phụ kiện, Sale) kèm bộ lọc giá, màu, size.", "Cao", "Lọc chính xác theo nhiều tiêu chí đồng thời; sắp xếp giá tăng/giảm.", "Hoàn thành"),
    ("FR-06", "Tìm kiếm thông minh", "Tìm kiếm sản phẩm theo từ khóa tiếng Việt đa tầng (có dấu và không dấu).", "Cao", "Gõ 'ao thun' hay 'áo thun' đều trả về kết quả đúng; gợi ý AJAX.", "Hoàn thành"),
    ("FR-07", "Chi tiết & Biến thể SKU", "Trang chi tiết hiển thị gallery ảnh, bảng chọn size/màu và tồn kho tương ứng.", "Cao", "Đổi màu/size tự động cập nhật SKU, giá bán và cảnh báo còn/hết hàng.", "Hoàn thành"),
    ("FR-08", "Danh sách yêu thích", "Khách hàng lưu các sản phẩm yêu thích (Wishlist) vào tài khoản cá nhân.", "Trung bình", "Bấm icon trái tim thêm/xóa nhanh bằng AJAX không tải lại trang.", "Hoàn thành"),
    ("FR-09", "Giỏ hàng & Mini Cart", "Thêm sản phẩm vào giỏ, xem nhanh qua ngăn kéo trượt từ bên phải màn hình.", "Cao", "Mini Cart trượt mượt mà; tăng giảm số lượng, xóa item và tính tổng tiền.", "Hoàn thành"),
    ("FR-10", "Mã giảm giá & Freeship", "Áp dụng coupon khuyến mãi và hiển thị thanh tiến trình đạt ngưỡng Freeship.", "Cao", "Nhập mã hợp lệ tự trừ tiền; đạt từ 500,000đ tự động miễn phí ship.", "Hoàn thành"),
    ("FR-11", "Thanh toán VietQR động", "Tự động sinh mã VietQR động theo chuẩn Napas247 cho ngân hàng.", "Cao", "Mã QR chứa đúng số tiền, STK và nội dung DHxxxx; nút 1-click copy.", "Hoàn thành"),
    ("FR-12", "Upload biên lai đối soát", "Khách hàng tải lên ảnh chụp màn hình chuyển khoản sau khi quét mã QR.", "Cao", "Tải ảnh JPG/PNG; tự động cập nhật trạng thái đơn sang 'Đã xác nhận'.", "Hoàn thành"),
    ("FR-13", "Quản lý sản phẩm & Kho", "Admin thêm, sửa, xóa sản phẩm, danh mục, gallery và tồn kho biến thể.", "Cao", "Dữ liệu lưu chuẩn CSDL; có thumbnail ảnh; kiểm soát tồn kho từng SKU.", "Hoàn thành"),
    ("FR-14", "Quản lý đơn hàng", "Theo dõi vòng đời đơn hàng qua 5 trạng thái, lọc thời gian và cập nhật nhanh.", "Cao", "Cập nhật trạng thái chuẩn xác; tự động trừ tồn kho khi đặt hàng.", "Hoàn thành"),
    ("FR-15", "Duyệt thanh toán 1-click", "Admin kiểm tra ảnh biên lai do khách gửi và duyệt thanh toán trực tiếp.", "Cao", "Xem trước ảnh bill phóng to; bấm 1 nút xác nhận tiền về.", "Hoàn thành"),
    ("FR-16", "Quản lý khuyến mãi", "Tạo mã coupon (% hoặc số tiền), giới hạn lượt dùng và banner trang chủ.", "Trung bình", "Mã hết hạn tự động từ chối; banner cập nhật đúng thứ tự hiển thị.", "Hoàn thành"),
]

t_fr = doc.add_table(rows=len(fr_data), cols=6)
t_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_idx, row in enumerate(t_fr.rows):
    is_head = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        val = fr_data[r_idx][c_idx]
        cell.text = val
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (is_head or c_idx in [0, 3, 5]) else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.runs[0]
        r.font.name = "Times New Roman"
        r.font.size = Pt(10 if not is_head else 10.5)
        if is_head:
            r.font.bold = True
            set_cell_background(cell, "E2E8F0")
        set_cell_borders(cell, color="CBD5E1", sz="4", val="single")

p_space = doc.add_paragraph()
p_space.paragraph_format.space_after = Pt(8)

add_heading_3(doc, "1.2.3. BẢNG PHÂN TÍCH YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS - NFR)")
nfr_data = [
    ("Mã", "Tên yêu cầu", "Mô tả yêu cầu", "Ưu tiên", "Tiêu chí nghiệm thu", "Tình trạng"),
    ("NFR-01", "Hiệu năng tải trang", "Trang chủ, danh mục và chi tiết sản phẩm phản hồi nhanh.", "Cao", "Thời gian phản hồi dưới 2 giây; tối ưu truy vấn ORM và WhiteNoise.", "Hoàn thành"),
    ("NFR-02", "Bảo mật hệ thống", "Bảo vệ an toàn dữ liệu người dùng, mật khẩu và chống tấn công.", "Cao", "Mã hóa PBKDF2/SHA256, tự động kiểm tra CSRF token, chống XSS, SQLi.", "Hoàn thành"),
    ("NFR-03", "Thiết kế Responsive", "Giao diện hiển thị tối ưu trên Điện thoại, Tablet và Laptop.", "Cao", "Layout co giãn linh hoạt bằng Tailwind CSS; menu mobile mượt mà.", "Hoàn thành"),
    ("NFR-04", "Linh hoạt cấu hình QR", "Khả năng thay đổi tài khoản ngân hàng không ảnh hưởng mã nguồn.", "Cao", "Chỉnh sửa BANK_ID trong tệp .env (VCB, TCB, MB, ACB, BIDV...).", "Hoàn thành"),
]
t_nfr = doc.add_table(rows=len(nfr_data), cols=6)
t_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_idx, row in enumerate(t_nfr.rows):
    is_head = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        val = nfr_data[r_idx][c_idx]
        cell.text = val
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (is_head or c_idx in [0, 3, 5]) else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.runs[0]
        r.font.name = "Times New Roman"
        r.font.size = Pt(10 if not is_head else 10.5)
        if is_head:
            r.font.bold = True
            set_cell_background(cell, "E2E8F0")
        set_cell_borders(cell, color="CBD5E1", sz="4", val="single")

p_space = doc.add_paragraph()
p_space.paragraph_format.space_after = Pt(8)

add_heading_3(doc, "1.2.4. MÔ HÌNH TOÁN HỌC VÀ GIẢI THUẬT (ĐĂNG KÝ & ĐĂNG NHẬP)")
add_body_p(doc, "Theo chuẩn phân tích yêu cầu công nghệ phần mềm, mô hình giải thuật toán học của hai chức năng nền tảng — Đăng ký tài khoản và Đăng nhập hệ thống — được mô hình hóa theo không gian trạng thái toán học và lưu đồ giải thuật như sau:")
add_body_p(doc, "A. Mô hình toán học cho chức năng Đăng ký tài khoản:")
add_bullet_p(doc, "X = { (email, password, confirm_password, full_name, phone) }", "• Không gian đầu vào: ")
add_bullet_p(doc, "D = { u_1, u_2, ..., u_n } với u_i.email là các email đã tồn tại trong bảng accounts_user.", "• Trạng thái cơ sở dữ liệu hiện hành: ")
add_bullet_p(doc, "Valid(X) = (Format(email) == True) ∧ (Length(password) ≥ 8) ∧ (password == confirm_password) ∧ (∀u ∈ D: u.email ≠ email)", "• Điều kiện kiểm tra logic (Validation): ")
add_bullet_p(doc, "f_register(X) = { Thêm User(email, PBKDF2(password), full_name) vào D → Thành công, Chuyển hướng /login/\n{ Trả về thông báo lỗi tương ứng nếu Valid(X) == False", "• Hàm chuyển trạng thái (Mapping Function): ")

add_body_p(doc, "B. Mô hình toán học cho chức năng Đăng nhập:")
add_bullet_p(doc, "Y = { (email, password) }", "• Không gian đầu vào: ")
add_bullet_p(doc, "f_login(Y) = { Khởi tạo Session(u.id), Ghi Cookie, Phân luồng quyền nếu (∃u ∈ D: u.email == email ∧ u.is_active == True ∧ Verify(password, u.password_hash) == True)\n{ Từ chối truy cập và xuất thông báo lỗi nếu không thỏa mãn điều kiện xác thực.", "• Hàm xác thực người dùng: ")

# =========================================================================
# 1.3. THIẾT KẾ LUỒNG NGƯỜI DÙNG (USER FLOW) - THEO CHUẨN BÀI GIẢNG 4.1
# =========================================================================
add_heading_2(doc, "1.3. THIẾT KẾ LUỒNG NGƯỜI DÙNG (USER FLOW - BƯỚC 1 THEO CHUẨN THIẾT KẾ PHẦN MỀM)")

add_body_p(doc, "Theo chuẩn quy trình \"4.1 Thiết kế phần mềm\" được giảng dạy trong học phần, giai đoạn thiết kế trải nghiệm người dùng (UI/UX Design) bao gồm 3 bước tuần tự cốt lõi: Bước 1 (User Flow — Luồng người dùng: Mô tả các bước người dùng thực hiện để hoàn thành công việc), Bước 2 (Wireframe — Bản phác thảo bố cục vị trí thành phần), và Bước 3 (Mockup — Bản thiết kế giao diện chi tiết hoàn chỉnh).")

add_body_p(doc, "Dưới đây là thiết kế chi tiết 4 luồng người dùng (User Flow) cho 4 chức năng cốt lõi của đề tài Urban Threads, được xây dựng theo đúng hệ thống quy chuẩn hình khối quốc tế trên nền tảng Figma/FigJam:")
add_bullet_p(doc, "Điểm bắt đầu (START) và Điểm kết thúc (END) của luồng công việc.", "• Hình Oval xám: ")
add_bullet_p(doc, "Các màn hình giao diện hoặc bước xử lý nghiệp vụ của hệ thống.", "• Hình Chữ nhật tím (Process): ")
add_bullet_p(doc, "Dữ liệu do người dùng nhập liệu hoặc lựa chọn từ giao diện (Form / Input).", "• Hình Bình hành xanh dương (Input): ")
add_bullet_p(doc, "Điểm rẽ nhánh điều kiện logic (Decision: Đúng/Sai, Hợp lệ/Lỗi, Còn hàng/Hết hàng).", "• Hình Thoi xanh lá (Decision): ")
add_bullet_p(doc, "Cơ sở dữ liệu lưu trữ SQLite (Database).", "• Hình Trụ vàng (Data/Database): ")

# 1.3.1. Đăng ký
add_heading_3(doc, "1.3.1. LUỒNG NGƯỜI DÙNG CHỨC NĂNG ĐĂNG KÝ TÀI KHOẢN (REGISTER FLOW)")
add_body_p(doc, "Luồng người dùng chức năng Đăng ký tài khoản mô tả toàn bộ quá trình từ khi khách hàng truy cập trang đăng ký (/accounts/register/), điền form thông tin cá nhân (Email, Họ tên, SĐT, Password, Nhập lại password). Hệ thống tiến hành kiểm tra tính khớp của mật khẩu 2 lần và kiểm tra tính duy nhất của Email trong CSDL SQLite. Nếu dữ liệu hợp lệ, hệ thống thực hiện băm mật khẩu bảo mật chuẩn PBKDF2_SHA256, ghi thông tin vào bảng accounts_user, tự động tạo phiên đăng nhập (Session) và chuyển hướng khách hàng về Trang chủ.")

img_uf_dk = 'D:/urban-threads/user_flow/userflow đk.png'
add_image_safe(doc, img_uf_dk, "Hình 1.1: Biểu đồ User Flow chức năng Đăng ký tài khoản (Thiết kế trên FigJam)", width_in=6.2)

# 1.3.2. Đăng nhập
add_heading_3(doc, "1.3.2. LUỒNG NGƯỜI DÙNG CHỨC NĂNG ĐĂNG NHẬP HỆ THỐNG (LOGIN FLOW)")
add_body_p(doc, "Luồng người dùng chức năng Đăng nhập mô tả hành trình khách hàng mở trang Đăng nhập (/accounts/login/), nhập thông tin định danh gồm Email và Mật khẩu rồi bấm \"Đăng nhập\". Hệ thống truy vấn bảng accounts_user để xác thực tài khoản. Trường hợp thông tin không chính xác, hệ thống xuất thông báo lỗi yêu cầu nhập lại. Khi xác thực thành công, hệ thống cấp Session Cookie và kiểm tra quyền quản trị (is_staff): nếu là Quản trị viên (Admin) sẽ chuyển tới Trang quản trị (/admin/), nếu là Khách hàng thông thường sẽ chuyển về Trang chủ (/).")

img_uf_dn = 'D:/urban-threads/user_flow/userflow đn.png'
add_image_safe(doc, img_uf_dn, "Hình 1.2: Biểu đồ User Flow chức năng Đăng nhập hệ thống (Thiết kế trên FigJam)", width_in=6.2)

# 1.3.3. Thêm giỏ hàng
add_heading_3(doc, "1.3.3. LUỒNG NGƯỜI DÙNG CHỨC NĂNG THÊM SẢN PHẨM VÀO GIỎ HÀNG (ADD TO CART FLOW)")
add_body_p(doc, "Luồng người dùng chức năng Thêm vào giỏ hàng mô tả hành trình từ khi khách hàng xem trang chi tiết sản phẩm thời trang (/products/<slug>/), lựa chọn các thuộc tính biến thể (Màu sắc, Size S/M/L/XL) và Số lượng mua. Khi bấm \"Thêm vào giỏ hàng\", hệ thống kiểm tra tồn kho kho hàng thực tế (Stock > 0). Nếu còn hàng, hệ thống kiểm tra sản phẩm đã tồn tại trong giỏ hàng hay chưa để cộng dồn số lượng hoặc tạo mới dòng CartItem trong CSDL. Cuối cùng, hệ thống kích hoạt ngăn kéo Mini Cart trượt ra mượt mà và cập nhật số đếm badge giỏ hàng tức thì.")

img_uf_cart = 'D:/urban-threads/user_flow/userflow thêm sp vào giỏ hàng.png'
add_image_safe(doc, img_uf_cart, "Hình 1.3: Biểu đồ User Flow chức năng Thêm sản phẩm vào giỏ hàng (Thiết kế trên FigJam)", width_in=6.2)

# 1.3.4. Thanh toán QR
add_heading_3(doc, "1.3.4. LUỒNG NGƯỜI DÙNG CHỨC NĂNG THANH TOÁN ĐƠN HÀNG QUA VIETQR (CHECKOUT & PAYMENT FLOW)")
add_body_p(doc, "Luồng người dùng chức năng Thanh toán mô tả quy trình chuyển đổi từ giỏ hàng sang đơn hàng hoàn tất. Sau khi kiểm tra giỏ hàng có sản phẩm và tài khoản đã đăng nhập, khách hàng nhập thông tin nhận hàng (Họ tên, SĐT, Địa chỉ, Phương thức vận chuyển). Hệ thống tự động tính phí ship và tổng tiền thanh toán, khởi tạo bản ghi đơn hàng (orders_order) ở trạng thái Chờ thanh toán (Pending), trừ tồn kho và làm rỗng giỏ hàng. Màn hình thanh toán hiển thị mã VietQR động chứa chính xác số tiền và cú pháp DHxxxxxxxx. Khách hàng quét mã chuyển khoản qua App ngân hàng và tải lên ảnh biên lai giao dịch để hoàn tất đơn hàng.")

img_uf_pay = 'D:/urban-threads/user_flow/userflow thanh toán qr.png'
add_image_safe(doc, img_uf_pay, "Hình 1.4: Biểu đồ User Flow chức năng Thanh toán đơn hàng qua VietQR (Thiết kế trên FigJam)", width_in=6.2)

# 1.3.5. Tổng quan 4 luồng
add_heading_3(doc, "1.3.5. TỔNG HỢP 4 LUỒNG NGƯỜI DÙNG CHÍNH TRÊN BẢNG THIẾT KẾ FIGJAM")
add_body_p(doc, "Nhằm mang lại cái nhìn toàn cảnh về hành trình trải nghiệm người dùng xuyên suốt toàn bộ hệ thống Urban Threads, hình 1.5 dưới đây tổng hợp 4 User Flow chính trên cùng một bảng làm việc (Canvas) FigJam theo đúng bố cục phân khu chuẩn:")

img_uf_all = 'D:/urban-threads/user_flow/user flow 4 chức năng.png'
add_image_safe(doc, img_uf_all, "Hình 1.5: Tổng hợp 4 luồng người dùng chính (User Flow Overview) trên FigJam", width_in=6.2)

doc.add_page_break()

# =========================================================================
# CHƯƠNG 2: BIỂU ĐỒ VÀ THIẾT KẾ HỆ THỐNG
# =========================================================================
add_heading_1(doc, "CHƯƠNG 2: BIỂU ĐỒ VÀ THIẾT KẾ HỆ THỐNG")

add_heading_2(doc, "2.1. BIỂU ĐỒ USE CASE")
add_body_p(doc, "Biểu đồ Use Case thể hiện tương tác giữa các tác nhân (Actors) bên ngoài với các chức năng bên trong hệ thống Urban Threads. Hệ thống bao gồm 3 tác nhân chính:")
add_body_p(doc, "1. Khách hàng (Customer / Guest): Đăng ký, đăng nhập, tìm kiếm sản phẩm, quản lý giỏ hàng, áp dụng coupon, quét mã VietQR thanh toán và xem lịch sử đơn hàng.")
add_body_p(doc, "2. Quản trị viên (Admin): Đăng nhập quản trị, quản lý danh mục và sản phẩm, quản lý biến thể tồn kho SKU, quản lý trạng thái đơn hàng, duyệt thanh toán 1-click qua ảnh biên lai.")
add_body_p(doc, "3. Cổng VietQR (External Service): Dịch vụ sinh mã VietQR động theo chuẩn Napas247 phục vụ giao dịch chuyển khoản.")

add_heading_3(doc, "2.1.1. BIỂU ĐỒ USE CASE TỔNG QUAN HỆ THỐNG URBAN THREADS")
img_uc_all = 'D:/urban-threads/use_cases/usecase_tong_quan.png'
add_image_safe(doc, img_uc_all, "Hình 2.1: Biểu đồ Use Case tổng quan hệ thống Urban Threads", width_in=6.0)

add_heading_3(doc, "2.1.2. BIỂU ĐỒ USE CASE CHI TIẾT CHỨC NĂNG THÊM SẢN PHẨM VÀO GIỎ HÀNG")
add_body_p(doc, "Phân hệ Giỏ hàng cho phép khách hàng tương tác linh hoạt với các ca sử dụng con. Khi thực hiện ca sử dụng \"Thêm sản phẩm vào giỏ hàng\", hệ thống bắt buộc phải thực hiện các quan hệ <<include>>: Chọn biến thể (Size/Màu), Kiểm tra tồn kho kho hàng, và Cập nhật số lượng giỏ hàng. Tại màn hình xem nhanh giỏ hàng (Mini Cart), khách hàng có thể áp dụng mã giảm giá (quan hệ <<extend>>) hoặc quan sát tiến trình Freeship (quan hệ <<include>>).")

img_uc_cart = 'D:/urban-threads/use_cases/usecase_them_gio_hang.png'
add_image_safe(doc, img_uc_cart, "Hình 2.2: Biểu đồ Use Case chi tiết chức năng Thêm sản phẩm vào giỏ hàng", width_in=5.5)

# Bảng đặc tả Use case Giỏ hàng
add_body_p(doc, "Bảng 2.1: Đặc tả Use Case chi tiết — Thêm sản phẩm vào giỏ hàng", italic=True)
uc_cart_spec = [
    ("Thuộc tính", "Nội dung chi tiết"),
    ("Tên Use Case", "Thêm sản phẩm vào giỏ hàng (Add to Cart)"),
    ("Tác nhân (Actor)", "Khách vãng lai (Guest) hoặc Khách hàng đã đăng nhập (Customer)"),
    ("Mục đích", "Cho phép người dùng chọn biến thể sản phẩm yêu thích và đưa vào giỏ hàng phục vụ mua sắm."),
    ("Tiền điều kiện", "Người dùng đang ở trang chi tiết sản phẩm (/products/<slug>/), sản phẩm ở trạng thái kích hoạt (is_active=True)."),
    ("Hậu điều kiện", "Dòng sản phẩm (CartItem) được lưu vào CSDL, tổng số lượng giỏ hàng tăng lên, ngăn kéo Mini Cart trượt ra."),
    ("Luồng sự kiện chính (Basic Flow)", "1. Người dùng chọn màu sắc và kích cỡ (Size) mong muốn.\n2. Người dùng chọn số lượng sản phẩm cần mua (mặc định là 1).\n3. Người dùng bấm nút \"Thêm vào giỏ hàng\".\n4. Hệ thống gửi yêu cầu POST /cart/add/ kèm variant_id và quantity.\n5. Hệ thống truy vấn CSDL kiểm tra tồn kho: Stock > 0.\n6. Hệ thống kiểm tra sản phẩm trong giỏ: nếu đã có thì cộng dồn số lượng, nếu chưa thì tạo CartItem mới.\n7. Hệ thống tính lại tổng số lượng và tổng tiền giỏ hàng.\n8. Hệ thống trả về phản hồi JSON thành công.\n9. Giao diện mở ngăn kéo Mini Cart và hiển thị thông báo Toast thành công."),
    ("Luồng ngoại lệ (Alternative Flow)", "4a. Biến thể sản phẩm đã hết hàng trong kho (Stock = 0):\n- Hệ thống trả về thông báo lỗi \"Sản phẩm đã hết hàng\".\n- Nút thêm giỏ hàng bị vô hiệu hóa, không tạo dòng trong giỏ hàng.\n4b. Số lượng mua vượt quá số lượng tồn kho còn lại:\n- Hệ thống tự động điều chỉnh số lượng mua bằng đúng số lượng tồn kho tối đa."),
]
t_uc_cart = doc.add_table(rows=len(uc_cart_spec), cols=2)
t_uc_cart.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_idx, row in enumerate(t_uc_cart.rows):
    is_head = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        cell.text = uc_cart_spec[r_idx][c_idx]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_head else (WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.runs[0]
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5 if not is_head else 11)
        if is_head or c_idx == 0:
            r.font.bold = True
        if is_head:
            set_cell_background(cell, "E2E8F0")
        set_cell_borders(cell, color="CBD5E1", sz="4", val="single")

p_space = doc.add_paragraph()
p_space.paragraph_format.space_after = Pt(8)

add_heading_3(doc, "2.1.3. BIỂU ĐỒ USE CASE CHI TIẾT CHỨC NĂNG THANH TOÁN ĐƠN HÀNG QUA VIETQR")
add_body_p(doc, "Phân hệ Thanh toán mô tả sự phối hợp giữa 3 tác nhân: Khách hàng (người đặt mua và thanh toán), Cổng VietQR (dịch vụ sinh mã thanh toán Napas247 tự động) và Quản trị viên Admin (người đối soát và duyệt thanh toán). Ca sử dụng \"Đặt hàng (Checkout)\" bắt buộc bao gồm: Nhập địa chỉ, Tạo đơn hàng, Sinh mã VietQR, Tải lên biên lai và Quản trị viên duyệt thanh toán 1-click.")

img_uc_pay = 'D:/urban-threads/use_cases/usecase_thanh_toan.png'
add_image_safe(doc, img_uc_pay, "Hình 2.3: Biểu đồ Use Case chi tiết chức năng Thanh toán đơn hàng qua VietQR", width_in=5.5)

# Bảng đặc tả Use case Thanh toán
add_body_p(doc, "Bảng 2.2: Đặc tả Use Case chi tiết — Thanh toán đơn hàng qua VietQR", italic=True)
uc_pay_spec = [
    ("Thuộc tính", "Nội dung chi tiết"),
    ("Tên Use Case", "Thanh toán đơn hàng qua VietQR (Checkout & VietQR Payment)"),
    ("Tác nhân (Actor)", "Khách hàng (Customer), Cổng VietQR (Service), Quản trị viên (Admin)"),
    ("Mục đích", "Xác nhận đơn hàng, thanh toán không tiền mặt qua mã VietQR chuẩn ngân hàng và đối soát biên lai."),
    ("Tiền điều kiện", "Khách hàng đã đăng nhập tài khoản, giỏ hàng có ít nhất 1 sản phẩm."),
    ("Hậu điều kiện", "Đơn hàng được lưu vào CSDL (orders_order), tồn kho sản phẩm được cập nhật trừ đi, giỏ hàng làm rỗng, biên lai thanh toán được lưu trữ."),
    ("Luồng sự kiện chính (Basic Flow)", "1. Khách hàng kiểm tra giỏ hàng và bấm \"Tiến hành thanh toán\".\n2. Khách hàng nhập địa chỉ nhận hàng và chọn phương thức vận chuyển (Tiêu chuẩn, Hỏa tốc).\n3. Khách hàng bấm \"Xác nhận đặt hàng\".\n4. Hệ thống tạo bản ghi đơn hàng mới với mã DHxxxxxxxx ở trạng thái Chờ thanh toán.\n5. Hệ thống gọi API VietQR sinh mã QR động chứa số tài khoản, số tiền và nội dung chuyển khoản.\n6. Hệ thống chuyển hướng khách hàng sang trang hiển thị mã QR thanh toán (/payments/qr/<id>/).\n7. Khách hàng mở App ngân hàng, quét mã QR và xác nhận chuyển khoản.\n8. Khách hàng chụp ảnh màn hình chuyển khoản thành công và tải lên hệ thống.\n9. Hệ thống lưu ảnh biên lai vào bảng payments_payment và cập nhật trạng thái đơn sang \"Đã xác nhận\".\n10. Hệ thống hiển thị trang Cảm ơn & Chi tiết đơn hàng."),
    ("Luồng ngoại lệ (Alternative Flow)", "1a. Giỏ hàng trống khi bấm thanh toán:\n- Hệ thống cảnh báo \"Giỏ hàng của bạn đang trống\" và chuyển về trang giỏ hàng.\n1b. Khách hàng chưa đăng nhập:\n- Hệ thống chuyển hướng sang trang Đăng nhập kèm tham số ?next=checkout.\n8a. Khách hàng chưa thể chuyển khoản ngay:\n- Đơn hàng vẫn được lưu ở trạng thái Chờ xác nhận trong mục Lịch sử đơn hàng, khách hàng có thể mở lại mã QR để thanh toán sau."),
]
t_uc_pay = doc.add_table(rows=len(uc_pay_spec), cols=2)
t_uc_pay.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_idx, row in enumerate(t_uc_pay.rows):
    is_head = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        cell.text = uc_pay_spec[r_idx][c_idx]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_head else (WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.runs[0]
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5 if not is_head else 11)
        if is_head or c_idx == 0:
            r.font.bold = True
        if is_head:
            set_cell_background(cell, "E2E8F0")
        set_cell_borders(cell, color="CBD5E1", sz="4", val="single")

p_space = doc.add_paragraph()
p_space.paragraph_format.space_after = Pt(8)

add_heading_2(doc, "2.2. BIỂU ĐỒ TUẦN TỰ (SEQUENCE DIAGRAM)")
add_body_p(doc, "Biểu đồ tuần tự mô tả dòng thông điệp trao đổi giữa đối tượng Người dùng, Giao diện Web (View UI), Bộ xử lý nghiệp vụ (Service View) và Cơ sở dữ liệu SQLite theo trình tự thời gian cho 4 kịch bản trọng tâm:")

# 2.2.1. Seq Đăng ký
add_heading_3(doc, "2.2.1. BIỂU ĐỒ TUẦN TỰ CHỨC NĂNG ĐĂNG KÝ TÀI KHOẢN")
add_body_p(doc, "Quy trình thực hiện gồm 11 bước tuần tự: Khách hàng nhập form và bấm Đăng ký ➔ Giao diện gửi POST request tới RegisterView ➔ View truy vấn kiểm tra email trong bảng accounts_user. Nếu email đã tồn tại, hệ thống báo lỗi. Nếu hợp lệ, hệ thống băm mật khẩu PBKDF2_SHA256, INSERT bản ghi mới, tạo Session đăng nhập và chuyển hướng về Trang chủ.")

img_seq_dk = 'D:/urban-threads/use_cases/sequence_dang_ky.png'
add_image_safe(doc, img_seq_dk, "Hình 2.4: Biểu đồ tuần tự chức năng Đăng ký tài khoản (PlantUML)", width_in=6.0)

# 2.2.2. Seq Đăng nhập
add_heading_3(doc, "2.2.2. BIỂU ĐỒ TUẦN TỰ CHỨC NĂNG ĐĂNG NHẬP HỆ THỐNG")
add_body_p(doc, "Quy trình thực hiện gồm 9 bước tuần tự: Khách hàng nhập email và password ➔ Gửi POST tới LoginView ➔ View truy vấn CSDL SQLite. Nếu so khớp mật khẩu thất bại, hệ thống báo lỗi. Nếu xác thực thành công, hệ thống tạo Session đăng nhập và kiểm tra quyền: nếu là Staff/Admin chuyển tới /admin/, nếu là Khách hàng chuyển về Trang chủ /.")

img_seq_dn = 'D:/urban-threads/use_cases/sequence_dang_nhap.png'
add_image_safe(doc, img_seq_dn, "Hình 2.5: Biểu đồ tuần tự chức năng Đăng nhập hệ thống (PlantUML)", width_in=6.0)

# 2.2.3. Seq Thêm giỏ hàng
add_heading_3(doc, "2.2.3. BIỂU ĐỒ TUẦN TỰ CHỨC NĂNG THÊM SẢN PHẨM VÀO GIỎ HÀNG")
add_body_p(doc, "Quy trình gồm 10 bước: Khách hàng chọn size, màu, số lượng và bấm \"Thêm vào giỏ hàng\" ➔ Gửi request AJAX POST /cart/add/ tới CartAddView ➔ View truy vấn bảng products_productvariant kiểm tra tồn kho. Rẽ nhánh: nếu Stock <= 0 báo lỗi hết hàng; nếu Stock > 0 và đã có trong giỏ thì UPDATE số lượng; nếu chưa có thì INSERT CartItem mới ➔ Cập nhật tổng số lượng giỏ hàng và phản hồi JSON để giao diện mở Mini Cart.")

img_seq_cart = 'D:/urban-threads/use_cases/sequence_them_gio_hang.png'
add_image_safe(doc, img_seq_cart, "Hình 2.6: Biểu đồ tuần tự chức năng Thêm sản phẩm vào giỏ hàng (PlantUML)", width_in=6.0)

# 2.2.4. Seq Thanh toán
add_heading_3(doc, "2.2.4. BIỂU ĐỒ TUẦN TỰ CHỨC NĂNG THANH TOÁN ĐƠN HÀNG VÀ ĐỐI SOÁT VIETQR")
add_body_p(doc, "Quy trình gồm 18 bước hoàn chỉnh: Khách hàng điền địa chỉ giao hàng và xác nhận đặt mua ➔ POST tới CheckoutView ➔ View kiểm tra giỏ hàng, tạo bản ghi orders_order, trừ tồn kho SKU, xóa giỏ hàng ➔ Sinh mã VietQR động theo đơn ➔ Khách hàng quét mã chuyển khoản và tải lên ảnh biên lai ➔ View lưu ảnh biên lai vào payments_payment, chuyển đơn sang \"Đã xác nhận\" và hiển thị màn hình Cảm ơn.")

img_seq_pay = 'D:/urban-threads/use_cases/sequence_thanh_toan.png'
add_image_safe(doc, img_seq_pay, "Hình 2.7: Biểu đồ tuần tự chức năng Thanh toán đơn hàng và Đối soát VietQR (PlantUML)", width_in=6.0)

add_heading_2(doc, "2.3. SƠ ĐỒ CƠ SỞ DỮ LIỆU (ER DIAGRAM)")
add_body_p(doc, "Cơ sở dữ liệu của hệ thống Urban Threads được thiết kế theo mô hình quan hệ chuẩn hóa 3NF, bao gồm các bảng thực thể cốt lõi sau:")
add_bullet_p(doc, "Lưu trữ thông tin tài khoản người dùng (id, email, password, full_name, phone, is_staff, is_active).", "• USER (Bảng accounts_user): ")
add_bullet_p(doc, "Danh mục sản phẩm thời trang đường phố (id, name, slug, description, is_active).", "• CATEGORY (Bảng products_category): ")
add_bullet_p(doc, "Thông tin chung sản phẩm (id, category_id, name, slug, base_price, gender, is_active, is_featured, total_sold).", "• PRODUCT (Bảng products_product): ")
add_bullet_p(doc, "Biến thể chi tiết quản lý theo từng kích cỡ và màu sắc (id, product_id, color_id, size_id, sku, stock, final_price).", "• PRODUCT_VARIANT (Bảng products_productvariant): ")
add_bullet_p(doc, "Quản lý giỏ hàng lưu trữ session hoặc gắn với tài khoản người dùng (cart_cart, cart_cartitem).", "• CART & CART_ITEM: ")
add_bullet_p(doc, "Quản lý đơn hàng (mã đơn DHxxxxxxxx, tổng tiền, phí ship, địa chỉ nhận hàng, trạng thái 5 bước) và chi tiết từng mặt hàng.", "• ORDER & ORDER_ITEM: ")
add_bullet_p(doc, "Lưu trữ thông tin thanh toán chuyển khoản, mã ngân hàng bank_id, trạng thái và ảnh chụp biên lai upload của khách hàng.", "• PAYMENT (Bảng payments_payment): ")

doc.add_page_break()

# =========================================================================
# CHƯƠNG 3: TRÌNH BÀY DEMO HỆ THỐNG
# =========================================================================
add_heading_1(doc, "CHƯƠNG 3: TRÌNH BÀY DEMO HỆ THỐNG")

add_body_p(doc, "Hệ thống website thương mại điện tử Urban Threads đã được triển khai thực tế thành công và chạy 24/7 trên môi trường máy chủ đám mây Cloud tại tên miền chính thức: https://urbanthreads-vn.onrender.com (hoặc kiểm thử cục bộ tại http://127.0.0.1:8000/). Dưới đây là kết quả thực nghiệm chi tiết từng phân hệ giao diện của website:")

# 3.1
add_heading_2(doc, "3.1. GIAO DIỆN TRANG CHỦ VÀ DANH MỤC SẢN PHẨM")
add_body_p(doc, "Trang chủ website Urban Threads được thiết kế nổi bật với Hero Banner thời trang đường phố, khu vực hiển thị sản phẩm mới (New Arrivals), sản phẩm bán chạy (Best Sellers) và danh mục phân loại (Áo thun, Hoodie, Áo khoác, Quần jeans...). Các khối sản phẩm hiển thị đầy đủ hình ảnh chất lượng cao, giá bán định dạng chuẩn Việt Nam (200,000đ), nhãn trạng thái và nút thêm giỏ nhanh.")

add_screenshot_placeholder(doc, "ẢNH CHỤP GIAO DIỆN TRANG CHỦ (HERO BANNER & SẢN PHẨM MỚI)", "Truy cập https://urbanthreads-vn.onrender.com/ chụp màn hình phần đầu Trang chủ", "Hình 3.1: Giao diện Trang chủ Website Urban Threads — Phong cách Streetwear Monochrome")

add_screenshot_placeholder(doc, "ẢNH CHỤP GIAO DIỆN TRANG DANH MỤC & BỘ LỌC ĐA TIÊU CHÍ", "Truy cập https://urbanthreads-vn.onrender.com/products/ chụp danh sách sản phẩm và bộ lọc", "Hình 3.2: Giao diện Danh mục sản phẩm thời trang và Bộ lọc theo giá, màu sắc, kích cỡ")

# 3.2
add_heading_2(doc, "3.2. GIAO DIỆN ĐĂNG NHẬP, ĐĂNG KÝ VÀ TÌM KIẾM THÔNG MINH")
add_body_p(doc, "Giao diện đăng ký và đăng nhập được thiết kế gọn gàng, hỗ trợ kiểm tra định dạng email và mật khẩu trực tiếp. Thanh tìm kiếm trên thanh điều hướng tích hợp thuật toán tìm kiếm tiếng Việt thông minh 2 tầng: hỗ trợ tìm kiếm cả từ khóa có dấu và không dấu (ví dụ: khách gõ \"ao khoac\" hay \"áo khoác\" đều trả về kết quả chính xác tuyệt đối).")

add_screenshot_placeholder(doc, "ẢNH CHỤP GIAO DIỆN ĐĂNG KÝ TÀI KHOẢN MỚI", "Truy cập https://urbanthreads-vn.onrender.com/accounts/register/ chụp form đăng ký", "Hình 3.3: Giao diện Đăng ký tài khoản thành viên mới với kiểm tra hợp lệ dữ liệu")

add_screenshot_placeholder(doc, "ẢNH CHỤP GIAO DIỆN ĐĂNG NHẬP HỆ THỐNG", "Truy cập https://urbanthreads-vn.onrender.com/accounts/login/ chụp form đăng nhập", "Hình 3.4: Giao diện Đăng nhập hệ thống bằng Email và Mật khẩu")

add_screenshot_placeholder(doc, "ẢNH CHỤP KẾT QUẢ TÌM KIẾM TIẾNG VIỆT THÔNG MINH", "Gõ từ khóa 'ao thun' hoặc 'hoodie' trên thanh tìm kiếm chụp lại kết quả", "Hình 3.5: Tính năng tìm kiếm tiếng Việt thông minh hỗ trợ cả từ khóa có dấu và không dấu")

# 3.3
add_heading_2(doc, "3.3. TRANG CHI TIẾT SẢN PHẨM VÀ CHỌN BIẾN THỂ (SIZE / MÀU)")
add_body_p(doc, "Trang chi tiết sản phẩm cho phép người dùng xem thư viện ảnh gallery nhiều góc độ, xem thông tin chi tiết về chất liệu và hướng dẫn bảo quản. Người dùng có thể tương tác chọn màu sắc và kích thước (S, M, L, XL, XXL) để hệ thống tự động cập nhật số lượng tồn kho thực tế và mã SKU tương ứng.")

add_screenshot_placeholder(doc, "ẢNH CHỤP TRANG CHI TIẾT SẢN PHẨM & BỘ CHỌN BIẾN THỂ", "Bấm vào 1 sản phẩm bất kỳ chụp trang chi tiết kèm bảng chọn Size và Màu", "Hình 3.6: Giao diện Chi tiết sản phẩm thời trang, Thư viện ảnh gallery và Bộ chọn biến thể SKU")

# 3.4
add_heading_2(doc, "3.4. GIỎ HÀNG VÀ NGĂN KÉO GIỎ HÀNG (MINI CART DRAWER)")
add_body_p(doc, "Khi bấm thêm vào giỏ, ngăn kéo Mini Cart sẽ trượt ra mượt mà từ cạnh phải màn hình mà không cần tải lại trang. Khách hàng có thể tăng/giảm số lượng sản phẩm, xóa sản phẩm, nhập mã giảm giá (Coupon như WELCOME10, GIAM50K) và quan sát thanh tiến trình đạt ngưỡng miễn phí ship (Freeship từ 500.000đ).")

add_screenshot_placeholder(doc, "ẢNH CHỤP NGĂN KÉO MINI CART TRƯỢT TỪ BÊN PHẢI", "Bấm nút 'Thêm vào giỏ hàng' chụp ngăn kéo giỏ hàng trượt ra và thanh Freeship", "Hình 3.7: Ngăn kéo giỏ hàng (Mini Cart Drawer) phản ứng tức thì với thanh tiến trình Freeship")

add_screenshot_placeholder(doc, "ẢNH CHỤP TRANG GIỎ HÀNG CHÍNH THỨC (/cart/)", "Truy cập https://urbanthreads-vn.onrender.com/cart/ chụp giỏ hàng đầy đủ", "Hình 3.8: Giao diện Trang Giỏ hàng chính thức, điều chỉnh số lượng và áp dụng mã giảm giá")

# 3.5
add_heading_2(doc, "3.5. TRANG THANH TOÁN VÀ CỔNG QUÉT MÃ VIETQR TỰ ĐỘNG")
add_body_p(doc, "Tại trang thanh toán (Checkout), hệ thống hỗ trợ chọn địa chỉ từ sổ địa chỉ đã lưu và chọn phương thức vận chuyển. Đặc biệt, hệ thống sinh ra mã QR Code VietQR động chứa chính xác số tài khoản ngân hàng, tên thụ hưởng, số tiền thanh toán và cú pháp nội dung chuyển khoản DHxxxxxxxx. Khách hàng quét mã qua ứng dụng ngân hàng và tải lên ảnh chụp biên lai giao dịch thành công.")

add_screenshot_placeholder(doc, "ẢNH CHỤP TRANG ĐẶT HÀNG & NHẬP ĐỊA CHỈ (CHECKOUT)", "Bấm 'Tiến hành thanh toán' chụp trang nhập địa chỉ nhận hàng và chọn cách ship", "Hình 3.9: Giao diện Trang Thanh toán (Checkout) và lựa chọn phương thức vận chuyển")

add_screenshot_placeholder(doc, "ẢNH CHỤP TRANG THANH TOÁN QUÉT MÃ VIETQR & UPLOAD BILL", "Sau khi xác nhận đặt hàng, chụp trang hiển thị mã QR VietQR động và nút tải biên lai", "Hình 3.10: Cổng thanh toán VietQR động chuẩn Napas247 và khu vực tải ảnh biên lai giao dịch")

# 3.6
add_heading_2(doc, "3.6. TRANG QUẢN TRỊ ADMIN DASHBOARD")
add_body_p(doc, "Trang quản trị Django Admin tùy biến cao cấp (https://urbanthreads-vn.onrender.com/admin/) cung cấp đầy đủ công cụ kiểm soát: xem danh sách đơn hàng có gắn huy hiệu màu sắc trực quan (Status Badges), xem trước hình thu nhỏ ảnh biên lai của khách, bấm phóng to ảnh biên lai và thao tác 1-click để duyệt thanh toán, tự động chuyển đơn sang trạng thái Đang đóng gói.")

add_screenshot_placeholder(doc, "ẢNH CHỤP BẢNG QUẢN LÝ ĐƠN HÀNG TRONG DJANGO ADMIN", "Đăng nhập admin, vào mục Quản lý Đơn hàng chụp danh sách đơn với huy hiệu màu sắc", "Hình 3.11: Giao diện Quản trị đơn hàng trong Django Admin với huy hiệu trạng thái trực quan")

add_screenshot_placeholder(doc, "ẢNH CHỤP TÍNH NĂNG ĐỐI SOÁT & DUYỆT BIÊN LAI 1-CLICK", "Chụp chi tiết 1 đơn hàng có ảnh biên lai chuyển khoản và nút xem QR Code", "Hình 3.12: Tính năng kiểm tra ảnh biên lai đối soát chuyển khoản và duyệt thanh toán 1-click")

# 3.7
add_heading_2(doc, "3.7. KẾ HOẠCH TRIỂN KHAI DỰ ÁN (GANTT CHART)")
add_body_p(doc, "Dự án được thực hiện nghiêm túc theo quy trình phát triển phần mềm gồm các giai đoạn qua 6 tuần:")

gantt_data = [
    ("Giai đoạn / Công việc", "Tuần 1", "Tuần 2", "Tuần 3", "Tuần 4", "Tuần 5", "Tuần 6"),
    ("1. Khảo sát yêu cầu & Lập kế hoạch", "X", "X", "", "", "", ""),
    ("2. Thiết kế CSDL & Luồng người dùng (User Flow)", "", "X", "X", "", "", ""),
    ("3. Lập trình Backend Django & Models", "", "", "X", "X", "", ""),
    ("4. Thiết kế Frontend Tailwind & Alpine.js", "", "", "", "X", "X", ""),
    ("5. Tích hợp cổng VietQR & Kiểm thử", "", "", "", "", "X", "X"),
    ("6. Triển khai Cloud Render & Viết báo cáo", "", "", "", "", "", "X"),
]
t_gantt = doc.add_table(rows=len(gantt_data), cols=7)
t_gantt.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_idx, row in enumerate(t_gantt.rows):
    is_head = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        cell.text = gantt_data[r_idx][c_idx]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (is_head or c_idx > 0) else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.runs[0]
        r.font.name = "Times New Roman"
        r.font.size = Pt(10 if not is_head else 10.5)
        if is_head or (c_idx > 0 and gantt_data[r_idx][c_idx] == "X"):
            r.font.bold = True
        if is_head:
            set_cell_background(cell, "E2E8F0")
        elif c_idx > 0 and gantt_data[r_idx][c_idx] == "X":
            set_cell_background(cell, "DCFCE7") # Xanh la nhat
        set_cell_borders(cell, color="CBD5E1", sz="4", val="single")

p_space = doc.add_paragraph()
p_space.paragraph_format.space_after = Pt(8)

doc.add_page_break()

# =========================================================================
# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
# =========================================================================
add_heading_1(doc, "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

add_heading_2(doc, "1. Tóm tắt kết quả đạt được:")
add_body_p(doc, "Sau quá trình nghiên cứu và thực hiện đề tài, em đã hoàn thành việc xây dựng website thương mại điện tử Urban Threads đáp ứng đầy đủ các yêu cầu đã đặt ra:")
add_bullet_p(doc, "Hệ thống hoạt động ổn định trên nền tảng Django 5.x với cấu trúc module hóa rõ ràng (9 ứng dụng chuyên biệt).")
add_bullet_p(doc, "Giao diện người dùng hiện đại, tinh tế theo phong cách streetwear, tương thích tốt trên cả thiết bị di động và máy tính.")
add_bullet_p(doc, "Đầy đủ các tính năng thương mại điện tử cốt lõi: Quản lý tài khoản, duyệt danh mục, bộ lọc, tìm kiếm tiếng Việt thông minh, giỏ hàng phản ứng nhanh Mini Cart, mã giảm giá, tính phí ship linh hoạt.")
add_bullet_p(doc, "Triển khai thành công giải pháp thanh toán quét mã VietQR tự động và cơ chế duyệt thanh toán 1-click đối soát biên lai trong Admin.")
add_bullet_p(doc, "Triển khai thành công website lên nền tảng đám mây Cloud (Render) với tên miền công khai hoạt động 24/7 có chứng chỉ bảo mật HTTPS (https://urbanthreads-vn.onrender.com).")

add_heading_2(doc, "2. Đánh giá ưu điểm và hạn chế:")
add_bullet_p(doc, "Mã nguồn sạch, dễ bảo trì và mở rộng; cơ chế bảo mật cao nhờ các tính năng tích hợp sẵn của Django; trải nghiệm người dùng mượt mà, tiện lợi; hệ thống quản trị trực quan giúp người bán dễ dàng kiểm soát kinh doanh.", "• Ưu điểm: ")
add_bullet_p(doc, "Cơ chế đối soát thanh toán hiện vẫn cần bước nhân viên xác nhận hình ảnh biên lai (chưa tích hợp Webhook biến động số dư tự động của ngân hàng); chưa tích hợp tính năng trò chuyện trực tuyến (Live Chat) chăm sóc khách hàng tức thời.", "• Hạn chế: ")

add_heading_2(doc, "3. Hướng phát triển trong tương lai:")
add_bullet_p(doc, "Tích hợp API ngân hàng hoặc Open Banking Webhook để tự động gạch nợ đơn hàng ngay khi khách hàng quét mã VietQR thành công.")
add_bullet_p(doc, "Phát triển ứng dụng di động (Mobile App) trên Flutter hoặc React Native kết nối đồng bộ qua Django REST Framework.")
add_bullet_p(doc, "Ứng dụng trí tuệ nhân tạo (AI Recommendation) để gợi ý các sản phẩm trang phục phối đồ (Mix & Match) cá nhân hóa cho từng khách hàng.")

doc.add_page_break()

# =========================================================================
# LỜI CẢM ƠN
# =========================================================================
p_cm = add_heading_1(doc, "LỜI CẢM ƠN")
p_cm.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_body_p(doc, "Em xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất tới cô Phạm Thị Dung — giảng viên phụ trách học phần Công nghệ phần mềm. Trong suốt quá trình học tập và thực hiện đề tài, cô đã luôn tận tình hướng dẫn, chỉ bảo những kiến thức chuyên môn quý báu và định hướng phương pháp tư duy kỹ thuật phần mềm chuẩn mực.")

add_body_p(doc, "Những lời góp ý chi tiết, sự động viên kịp thời và phương pháp giảng dạy tâm huyết của cô đã giúp em vượt qua những bỡ ngỡ trong giai đoạn khảo sát yêu cầu, thiết kế kiến trúc, mô hình hóa luồng người dùng và giải quyết các bài toán kỹ thuật phức tạp trong đề tài. Đây không chỉ là hành trang quan trọng để em hoàn thành tốt học phần mà còn là nền tảng vững chắc cho con đường phát triển nghề nghiệp sau này.")

add_body_p(doc, "Dù em đã rất nỗ lực cố gắng, song do kiến thức và kinh nghiệm thực tế của bản thân còn hạn chế, báo cáo khó tránh khỏi những thiếu sót nhất định. Em rất kính mong tiếp tục nhận được sự nhận xét, chỉ dẫn của cô để bài làm được hoàn thiện hơn nữa.")

add_body_p(doc, "Em xin kính chúc cô luôn dồi dào sức khỏe, ngập tràn niềm vui, hạnh phúc và gặt hái được nhiều thành công hơn nữa trong sự nghiệp trồng người cao quý!")

p_sign = doc.add_paragraph()
format_paragraph(p_sign, space_before=20, space_after=0, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.RIGHT)
p_sign.paragraph_format.right_indent = Inches(1.0)
r_s1 = p_sign.add_run("Sinh viên thực hiện\n\n\n\n")
r_s1.font.name = "Times New Roman"
r_s1.font.size = Pt(13)
r_s1.font.bold = True

r_s2 = p_sign.add_run("Lê Hải Nam")
r_s2.font.name = "Times New Roman"
r_s2.font.size = Pt(14)
r_s2.font.bold = True

# LƯU FILE BÁO CÁO HOÀN CHỈNH
out_path = 'D:/urban-threads/Bao_Cao_Cong_Nghe_Phan_Mem_Le_Hai_Nam.docx'
doc.save(out_path)
print(f"BÁO CÁO ĐÃ XUẤT THÀNH CÔNG TẠI: {out_path}")
