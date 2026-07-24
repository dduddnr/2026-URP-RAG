from pathlib import Path
import argparse
import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 문서(Chunk) 로드
# 2. Token으로 분리
# 3. TF-IDF 벡터 생성
# 4. Query 입력
# 5. Query도 Token으로 분리
# 6. Query와 각 문서의 TF-IDF 유사도 계산
# 7. 가장 높은 점수의 Top-k 문서 반환

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNKS_PATH = PROJECT_ROOT / "data" / "processed" / "survey_on_rag2_chunks.jsonl"


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text.lower())
#대소문자 차이 없앰
#findall() 함수는 정규표현식에 매칭되는 모든 문자열을 찾아 리스트로 반환


def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def build_tfidf(chunks: list[dict]) -> tuple[TfidfVectorizer, object]:
    documents = [chunk["text"] for chunk in chunks] #chunk 텍스트를 리스트로 변환
    vectorizer = TfidfVectorizer( # 전체 chunk를 보고 단어 사전을 만들고 각 단어의 IDF 값을 계산하고 각 chunk를 TF-IDF 벡터로 바꿔줌
        tokenizer=tokenize,
        lowercase=False,
        token_pattern=None,
    )
    matrix = vectorizer.fit_transform(documents) # TF-IDF 벡터를 학습하고, 각 chunk의 TF-IDF 벡터를 행렬로 변환
    return vectorizer, matrix
#전체 chunk를 읽어서 어떤 단어들이 있는지 단어 사전을 만들고, 각 단어가 얼마나 희귀한지 IDF 값을 계산

#query를 입력받아 TF-IDF 유사도를 계산하고, 점수가 높은 Top-k chunk를 반환하는 함수
def search(
    query: str,
    chunks: list[dict],
    vectorizer: TfidfVectorizer,
    matrix: object,
    top_k: int,
) -> list[dict]:
    query_vector = vectorizer.transform([query]) #query를 TF-IDF 벡터로 변환
    scores = cosine_similarity(query_vector, matrix).flatten()# query와 각 chunk의 TF-IDF 유사도 계산
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True) # 유사도 점수에 따라 chunk 인덱스를 내림차순으로 정렬

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
    parser = argparse.ArgumentParser(
        description="Search RAG survey chunks with TF-IDF cosine similarity."
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to show")
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH, help="Path to chunks JSONL")
    args = parser.parse_args()

    chunks = load_chunks(args.chunks)
    vectorizer, matrix = build_tfidf(chunks)

    if args.query:
        results = search(args.query, chunks, vectorizer, matrix, args.top_k)
        print_results(args.query, results)
        return

    print("TF-IDF retriever is ready. Type a query, or type 'exit' to quit.")
    while True:
        query = input("\nQuery> ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        if not query:
            continue

        results = search(query, chunks, vectorizer, matrix, args.top_k)
        print_results(query, results)


if __name__ == "__main__":
    main()
