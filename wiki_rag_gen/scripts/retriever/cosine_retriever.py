from pathlib import Path
import argparse
import json
import math
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "chunking_embedding"))

from dense_embed_chunks import (
    CHUNKS_PATH,
    EMBEDDINGS_PATH,
    DEFAULT_OLLAMA_URL,
    DEFAULT_MODEL,
    DEFAULT_TIMEOUT,
    load_chunks,
    embed_text,
    check_ollama,
    build_or_load_embeddings,
)

# 1. 캐시된 chunk 임베딩 로드 (없으면 embed_chunks.py 로직으로 생성)
# 2. query도 같은 모델로 임베딩
# 3. query 벡터와 각 chunk 벡터의 cosine similarity 계산
# 4. 점수 높은 순 top-k 반환


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def search(
    query: str,
    chunks: list[dict],
    embeddings: list[dict],
    model: str,
    ollama_url: str,
    timeout: int,
    top_k: int,
) -> list[dict]:
    query_embedding = embed_text(query, model, ollama_url, timeout)
    scores = [cosine_similarity(query_embedding, item["embedding"]) for item in embeddings]
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

    results = []
    for index in ranked_indices[:top_k]:
        chunk = chunks[index]
        results.append({
            "score": float(scores[index]),
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "section": chunk["section"],
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
        })
    return results


def print_results(query: str, results: list[dict]) -> None:
    print(f"Query: {query}\n")
    for rank, result in enumerate(results, start=1):
        preview = result["text"].replace("\n", " ")
        if len(preview) > 300:
            preview = preview[:300].rstrip() + "..."
        print(f"[{rank}] score={result['score']:.4f}")
        print(f"    chunk_id={result['chunk_id']} section={result['section']}")
        print(f"    {preview}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Cosine similarity dense retriever")
    parser.add_argument("query", nargs="?")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH)
    parser.add_argument("--cache", type=Path, default=EMBEDDINGS_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    check_ollama(args.ollama_url, args.timeout)
    chunks = load_chunks(args.chunks)
    embeddings = build_or_load_embeddings(
        chunks=chunks,
        model=args.model,
        ollama_url=args.ollama_url,
        cache_path=args.cache,
        rebuild_cache=False,
        timeout=args.timeout,
    )

    if args.query:
        results = search(args.query, chunks, embeddings, args.model, args.ollama_url, args.timeout, args.top_k)
        print_results(args.query, results)
        return

    print("Cosine retriever ready. Type a query, or 'exit' to quit.")
    while True:
        query = input("\nQuery> ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        if not query:
            continue
        results = search(query, chunks, embeddings, args.model, args.ollama_url, args.timeout, args.top_k)
        print_results(query, results)


if __name__ == "__main__":
    main()