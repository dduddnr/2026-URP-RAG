from pathlib import Path
import json
import re


base_dir = Path(__file__).parent

input_path = base_dir / "survey_on_rag2_pages_pypdf.jsonl"
output_path = base_dir / "survey_on_rag2_pages_cleaned.jsonl"


def clean_text(text: str) -> str:
    # 1. 깨진 특수문자 일부 치환
    text = text.replace("user?셲", "user's")
    text = text.replace("model?셲", "model's")
    text = text.replace("?뾅orresponding author", "Corresponding author")

    # 2. 줄 끝 하이픈 복원
    # 예: knowl-\nedge -> knowledge
    text = re.sub(r"([A-Za-z])-\n([a-z])", r"\1\2", text)

    # 3. 문장 중간 줄바꿈을 공백으로 변경
    # 단, 문단 구분은 어느 정도 유지
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # 4. 반복되는 공백 정리
    text = re.sub(r"[ \t]+", " ", text)

    # 5. 앞뒤 공백 제거
    text = text.strip()

    return text


with input_path.open("r", encoding="utf-8") as f_in, output_path.open(
    "w", encoding="utf-8"
) as f_out:
    for line in f_in:
        record = json.loads(line)

        raw_text = record["text"]
        cleaned_text = clean_text(raw_text)

        cleaned_record = {
            "source": record["source"],
            "page": record["page"],
            "text": cleaned_text,
        }

        f_out.write(json.dumps(cleaned_record, ensure_ascii=False) + "\n")


print(f"Saved cleaned file to: {output_path}")