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

# cosine_retriever.py와 유사도 계산식만 다름:
# cosine  = 벡터의 "방향"이 얼마나 비슷한가 (크기 무시)
# euclidean = 벡터 공간에서의 "직선 거리" (크기도 영향을 줌)
# 거리이므로 값이 작을수록 더 유사한 chunk


def euclidean_distance(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


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
    distances = [euclidean_distance(query_embedding, item["embedding"]) for item in embeddings]
    # 거리는 작을수록 유사하므로 오름차순 정렬
    ranked_indices = sorted(range(len(distances)), key=lambda i: distances[i])

    results = []
    for index in ranked_indices[:top_k]:
        chunk = chunks[index]
        results.append({
            "distance": float(distances[index]),
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
        print(f"[{rank}] distance={result['distance']:.4f}  (낮을수록 유사)")
        print(f"    chunk_id={result['chunk_id']} section={result['section']}")
        print(f"    {preview}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Euclidean distance dense retriever")
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

    print("Euclidean retriever ready. Type a query, or 'exit' to quit.")
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