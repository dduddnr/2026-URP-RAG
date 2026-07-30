from pathlib import Path
import argparse
import json
import re
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "chunking_embedding"))

from rank_bm25 import BM25Okapi

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
from cosine_retriever import cosine_similarity

# Hybrid = dense(cosine) score와 sparse(BM25) score를 정규화 후 가중합
# score = alpha * dense_norm + (1 - alpha) * sparse_norm
# alpha=1.0 -> 순수 dense, alpha=0.0 -> 순수 BM25


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text.lower())


def build_bm25(chunks: list[dict]) -> BM25Okapi:
    tokenized_corpus = [tokenize(chunk["text"]) for chunk in chunks]
    return BM25Okapi(tokenized_corpus)


def min_max_normalize(scores: list[float]) -> list[float]:
    lo, hi = min(scores), max(scores)
    if hi - lo < 1e-9:
        return [0.0 for _ in scores]
    return [(s - lo) / (hi - lo) for s in scores]


def search(
    query: str,
    chunks: list[dict],
    embeddings: list[dict],
    bm25: BM25Okapi,
    model: str,
    ollama_url: str,
    timeout: int,
    top_k: int,
    alpha: float,
) -> list[dict]:
    # dense score (cosine)
    query_embedding = embed_text(query, model, ollama_url, timeout)
    dense_scores = [cosine_similarity(query_embedding, item["embedding"]) for item in embeddings]
    dense_norm = min_max_normalize(dense_scores)

    # sparse score (BM25)
    tokenized_query = tokenize(query)
    sparse_scores = list(bm25.get_scores(tokenized_query))
    sparse_norm = min_max_normalize(sparse_scores)

    final_scores = [alpha * d + (1 - alpha) * s for d, s in zip(dense_norm, sparse_norm)]
    ranked_indices = sorted(range(len(final_scores)), key=lambda i: final_scores[i], reverse=True)

    results = []
    for index in ranked_indices[:top_k]:
        chunk = chunks[index]
        results.append({
            "score": float(final_scores[index]),
            "dense_score": float(dense_norm[index]),
            "sparse_score": float(sparse_norm[index]),
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "section": chunk["section"],
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
        })
    return results


def print_results(query: str, results: list[dict], alpha: float) -> None:
    print(f"Query: {query}  (alpha={alpha})\n")
    for rank, result in enumerate(results, start=1):
        preview = result["text"].replace("\n", " ")
        if len(preview) > 300:
            preview = preview[:300].rstrip() + "..."
        print(
            f"[{rank}] hybrid={result['score']:.4f} "
            f"(dense={result['dense_score']:.4f}, sparse={result['sparse_score']:.4f})"
        )
        print(f"    chunk_id={result['chunk_id']} section={result['section']}")
        print(f"    {preview}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hybrid retriever (dense cosine + sparse BM25)")
    parser.add_argument("query", nargs="?")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.5, help="dense 비중 (0~1). 1=순수dense, 0=순수BM25")
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
    bm25 = build_bm25(chunks)

    if args.query:
        results = search(
            args.query, chunks, embeddings, bm25,
            args.model, args.ollama_url, args.timeout, args.top_k, args.alpha,
        )
        print_results(args.query, results, args.alpha)
        return

    print("Hybrid retriever ready. Type a query, or 'exit' to quit.")
    while True:
        query = input("\nQuery> ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        if not query:
            continue
        results = search(
            query, chunks, embeddings, bm25,
            args.model, args.ollama_url, args.timeout, args.top_k, args.alpha,
        )
        print_results(query, results, args.alpha)


if __name__ == "__main__":
    main()