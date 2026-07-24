from pathlib import Path
import json

# 1. 최대 1000자 기준으로 자름
# 2. 가능하면 문장 끝에서 자름
# 3. 문장 끝이 없으면 줄바꿈 기준
# 4. 그래도 어렵다면 공백 기준
# 5. 앞뒤 chunk는 150자 정도 겹치게 함

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "interim" / "survey_on_rag2_pages_pypdf.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "survey_on_rag2_chunks.jsonl"

CHUNK_SIZE = 1000 #한 chunk를 최대 약 1000자 정도로 만든다
CHUNK_OVERLAP = 150 #이전 chunk의 마지막 150자 정도를 다음 chunk와 겹치게 한다 
#overlap을 넣으면 chunk 2가 chunk 1의 끝부분을 조금 포함해서 문맥을 유지합니다.


def split_into_chunks(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap")

    chunks = []
    start = 0 #텍스트의 시작 위치를 0

    while start < len(text):
        end = min(start + chunk_size, len(text)) # 텍스트의 끝 위치를 chunk_size만큼 이동시키되, 텍스트 길이를 초과하지 않도록 한다

        if end < len(text): # 텍스트의 끝 위치가 텍스트 길이보다 작으면, 문장 경계를 찾아서 chunk를 나눈다
            boundary = max( # 문장 경계를 찾기 위해, 현재 chunk의 시작 위치와 끝 위치 사이에서 가장 마지막으로 나타나는 문장 구분자를 찾는다
                text.rfind(". ", start, end),
                text.rfind("? ", start, end),
                text.rfind("! ", start, end),
                text.rfind("\n\n", start, end),
                text.rfind("\n", start, end),
            )
            if boundary > start + chunk_size * 0.5: # 만약 문장 경계가 chunk_size의 절반 이상 떨어져 있으면, 그 위치를 chunk의 끝 위치로 설정한다
                end = boundary + 1
            else: # 만약 좋은 문장 경계를 못 찾으면 공백 기준으로 자릅니다.
                space = text.rfind(" ", start, end)
                if space > start:
                    end = space

        chunk = text[start:end].strip() # start부터 end까지 잘라서 앞뒤 공백을 제거하고, 비어 있지 않으면 chunk 리스트에 넣는다
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(0, end - overlap) # 다음 chunk는 방금 끝난 지점보다 150자 앞에서 다시 시작합니다.
        while start < len(text) and text[start] != " ": # chunk의 시작 위치를 공백 뒤로 맞추는 역할
            start += 1
        while start < len(text) and text[start] == " ":
            start += 1

    return chunks


def main() -> None:
    total_chunks = 0

    with INPUT_PATH.open("r", encoding="utf-8") as f_in, OUTPUT_PATH.open(
        "w", encoding="utf-8"
    ) as f_out:
        for line in f_in:
            page_record = json.loads(line)
            page = page_record["page"]
            text = page_record["text"].strip()
            chunks = split_into_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)

            for chunk_index, chunk_text in enumerate(chunks):
                chunk_record = {
                    "chunk_id": f"survey_on_rag2_p{page}_c{chunk_index}",
                    "source": page_record["source"],
                    "page": page,
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                }
                f_out.write(json.dumps(chunk_record, ensure_ascii=False) + "\n")
                total_chunks += 1

    print(f"Saved {total_chunks} chunks to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
