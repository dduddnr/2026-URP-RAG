from pathlib import Path
import argparse
import json
import math
import socket
import urllib.error
import urllib.request


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNKS_PATH = PROJECT_ROOT / "data" / "processed" / "survey_on_rag2_chunks.jsonl"

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "nomic-embed-text"
DEFAULT_TIMEOUT = 60


def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def post_json(url: str, payload: dict, timeout: int) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is installed and running "
            f"at {DEFAULT_OLLAMA_URL}."
        ) from exc


def check_ollama(ollama_url: str, timeout: int) -> None:
    url = f"{ollama_url.rstrip('/')}/api/tags"
    request = urllib.request.Request(url, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=timeout):
            return
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Install Ollama, start it, and pull an "
            "embedding model such as 'nomic-embed-text'."
        ) from exc


def embed_text(text: str, model: str, ollama_url: str, timeout: int) -> list[float]:
    endpoint = f"{ollama_url.rstrip('/')}/api/embed"
    payload = {"model": model, "input": text}

    try:
        response = post_json(endpoint, payload, timeout)
        embeddings = response.get("embeddings")
        if embeddings and isinstance(embeddings, list):
            return embeddings[0]
    except RuntimeError:
        raise
    except Exception:
        pass

    endpoint = f"{ollama_url.rstrip('/')}/api/embeddings"
    payload = {"model": model, "prompt": text}
    response = post_json(endpoint, payload, timeout)
    embedding = response.get("embedding")
    if not embedding:
        raise RuntimeError(
            f"Ollama did not return an embedding. Check that model '{model}' is available."
        )
    return embedding


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))

    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def build_embeddings(
    chunks: list[dict],
    model: str,
    ollama_url: str,
    timeout: int,
) -> list[list[float]]:
    embeddings = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Embedding chunk {index}/{len(chunks)}: {chunk['chunk_id']}")
        embeddings.append(embed_text(chunk["text"], model, ollama_url, timeout))

    return embeddings


def search(
    query: str,
    chunks: list[dict],
    chunk_embeddings: list[list[float]],
    model: str,
    ollama_url: str,
    timeout: int,
    top_k: int,
) -> list[dict]:
    query_embedding = embed_text(query, model, ollama_url, timeout)
    scores = [
        cosine_similarity(query_embedding, chunk_embedding)
        for chunk_embedding in chunk_embeddings
    ]
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

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
        description="Search RAG survey chunks with simple Ollama dense retrieval."
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to show")
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH, help="Path to chunks JSONL")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama embedding model")
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL, help="Ollama base URL")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Ollama request timeout in seconds")
    args = parser.parse_args()

    check_ollama(args.ollama_url, args.timeout)
    chunks = load_chunks(args.chunks)
    chunk_embeddings = build_embeddings(
        chunks=chunks,
        model=args.model,
        ollama_url=args.ollama_url,
        timeout=args.timeout,
    )

    if args.query:
        results = search(
            args.query,
            chunks,
            chunk_embeddings,
            args.model,
            args.ollama_url,
            args.timeout,
            args.top_k,
        )
        print_results(args.query, results)
        return

    print("Simple Ollama dense retriever is ready. Type a query, or type 'exit' to quit.")
    while True:
        query = input("\nQuery> ").strip()
        if query.lower() in {"exit", "quit", "q"}:
            break
        if not query:
            continue

        results = search(
            query,
            chunks,
            chunk_embeddings,
            args.model,
            args.ollama_url,
            args.timeout,
            args.top_k,
        )
        print_results(query, results)


if __name__ == "__main__":
    main()
