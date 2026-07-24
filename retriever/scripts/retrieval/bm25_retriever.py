from pathlib import Path
import argparse
import json
import re

from rank_bm25 import BM25Okapi


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNKS_PATH = PROJECT_ROOT / "data" / "processed" / "survey_on_rag2_chunks.jsonl"

#bm25 동작 과정
# 1. JSONL에서 chunk 로드
# 2. 각 chunk를 token으로 분리
# 3. BM25Okapi 인덱스 생성
# 4. query 입력
# 5. query도 token으로 분리
# 6. 각 chunk의 BM25 점수 계산
# 7. 점수가 높은 Top-k chunk 반환

def tokenize(text: str) -> list[str]: # query와 chunk를 토큰화하는 함수
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text.lower())
#대소문자 차이 없앰
#findall() 함수는 정규표현식에 매칭되는 모든 문자열을 찾아 리스트로 반환
#Dense Retrieval is useful -> ['dense', 'retrieval', 'is', 'useful']

#chunk jsonl파일 에서 chunk를 로드하는 함수
def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def build_bm25(chunks: list[dict]) -> BM25Okapi:
    tokenized_corpus = [tokenize(chunk["text"]) for chunk in chunks] #chunk 텍스트를 token리스트로 변환
    return BM25Okapi(tokenized_corpus) #토큰화된 chunk들을 BM25Okapi 인스턴스로 변환하여 BM25 인덱스를 생성
# 1. 각 chunk의 길이
# 2. 전체 chunk의 평균 길이
# 3. 각 단어가 각 chunk에 몇 번 나오는지
# 4. 각 단어가 전체 chunk 중 몇 개의 chunk에 등장하는지
# 5. 각 단어의 IDF 값

#query를 입력받아 BM25 점수를 계산하고, 점수가 높은 Top-k chunk를 반환하는 함수
def search(query: str, chunks: list[dict], bm25: BM25Okapi, top_k: int) -> list[dict]:
    tokenized_query = tokenize(query) #쿼리를 토큰화
    scores = bm25.get_scores(tokenized_query) #BM25 점수 계산
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True) #점수가 높은 순서대로 정렬

    results = []
    for index in ranked_indices[:top_k]:
        chunk = chunks[index]
        results.append(
            {
                "score": float(scores[index]),
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "page": chunk["page"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
            }
        )

    return results


def print_results(query: str, results: list[dict]) -> None:
    print(f"Query: {query}")
    print()

    for rank, result in enumerate(results, start=1):
        preview = result["text"].replace("\n", " ")
        if len(preview) > 450:
            preview = preview[:450].rstrip() + "..."

        print(f"[{rank}] score={result['score']:.4f}")
        print(
            f"    chunk_id={result['chunk_id']} "
            f"page={result['page']} chunk_index={result['chunk_index']}"
        )
        print(f"    {preview}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Search RAG survey chunks with BM25.")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to show")
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH, help="Path to chunks JSONL")
    args = parser.parse_args()

    chunks = load_chunks(args.chunks)
    bm25 = build_bm25(chunks)

    if args.query:
        results = search(args.query, chunks, bm25, args.top_k)
        print_results(args.query, results)
        return

    print("BM25 retriever is ready. Type a query, or type 'exit' to quit.")
    while True:
        query = input("\nQuery> ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        if not query:
            continue

        results = search(query, chunks, bm25, args.top_k)
        print_results(query, results)


if __name__ == "__main__":
    main()
