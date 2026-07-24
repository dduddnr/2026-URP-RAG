from pathlib import Path
import json
from pypdf import PdfReader

# 1. PDF 파일 로드
# 2. reader.pages를 이용해 페이지별 접근
# 3. extract_text()로 각 페이지의 텍스트 추출
# 4. source, page, text 구조로 저장
# 5. JSONL 형식으로 한 페이지씩 기록

PROJECT_ROOT = Path(__file__).resolve().parents[2]
pdf_path = PROJECT_ROOT / "data" / "raw" / "survey on RAG2.pdf"
output_path = PROJECT_ROOT / "data" / "interim" / "survey_on_rag2_pages_pypdf.jsonl"

reader = PdfReader(str(pdf_path))

with output_path.open("w", encoding="utf-8") as f:
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        record = {
            "source": pdf_path.name,
            "page": page_num,
            "text": text
        }

        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Saved to: {output_path}")
