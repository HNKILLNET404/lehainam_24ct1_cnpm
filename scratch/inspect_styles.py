import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r'C:\Users\ADMIN\.gemini\antigravity\brain\050a7b2d-e3c2-4b9c-85ea-9d7f7a1a4fd5\.user_uploaded\media_1793610009766_8dcaf68f.docx')
section = doc.sections[0]
print(f"Top margin: {section.top_margin.cm:.2f} cm")
print(f"Bottom margin: {section.bottom_margin.cm:.2f} cm")
print(f"Left margin: {section.left_margin.cm:.2f} cm")
print(f"Right margin: {section.right_margin.cm:.2f} cm")
print(f"Page width: {section.page_width.cm:.2f} cm")
print(f"Page height: {section.page_height.cm:.2f} cm")

# Check styles
normal_style = doc.styles['Normal']
print(f"Normal font: {normal_style.font.name}, size: {normal_style.font.size}")
if normal_style.paragraph_format.line_spacing is not None:
    print(f"Normal line spacing: {normal_style.paragraph_format.line_spacing}")
