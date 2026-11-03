import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc_path = r'C:\Users\ADMIN\.gemini\antigravity\brain\050a7b2d-e3c2-4b9c-85ea-9d7f7a1a4fd5\.user_uploaded\media_1793610009766_8dcaf68f.docx'
doc = docx.Document(doc_path)

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if text.startswith("CHƯƠNG") or text.startswith("1.") or text.startswith("2.") or text.startswith("3.") or "BIỂU ĐỒ" in text or "LỜI" in text or "MỤC LỤC" in text:
        print(f"[{idx}] (style={p.style.name}): {text[:80]}")
