from pathlib import Path
import argparse
import json
import socket
import urllib.error
import urllib.request

# Ollama embedding model로 vector 변환
# embedding  저장

FOLDER_ROOT = Path(__file__).resolve().parents[2]   # wiki_rag_gen
CHUNKS_PATH = FOLDER_ROOT / "data" / "wikipedia_chunks.jsonl"
EMBEDDINGS_PATH = FOLDER_ROOT / "data" / "wikipedia_embeddings.json"

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434" # 로컬 Ollama 서버 주소
DEFAULT_MODEL = "nomic-embed-text"
DEFAULT_TIMEOUT = 60


def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


#ollama 서버에 POST 요청을 보내고 JSON 응답을 반환하는 함수
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

# Ollama 서버가 실행 중인지 확인하는 함수
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

# Ollama 모델을 사용하여 텍스트를 임베딩하는 함수
# openaiembedding은 품질 좋지만, 유료이므로 ollama embedding 모델을 사용
#입력된 text를 Ollama embedding 모델에 보내고, 결과로 숫자 리스트 형태의 embedding vector를 받음
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

    # Fallback for older Ollama versions.
    endpoint = f"{ollama_url.rstrip('/')}/api/embeddings"
    payload = {"model": model, "prompt": text}
    response = post_json(endpoint, payload, timeout)
    embedding = response.get("embedding")
    if not embedding:
        raise RuntimeError(
            f"Ollama did not return an embedding. Check that model '{model}' is available."
        )
    return embedding


# 캐시된 임베딩이 현재 모델과 일치하는지 확인하는 함수
def cache_matches(cache: dict, chunks: list[dict], model: str) -> bool:
    if cache.get("model") != model:
        return False

    cached_embeddings = cache.get("embeddings", [])
    if len(cached_embeddings) != len(chunks):
        return False

    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    cached_ids = [item.get("chunk_id") for item in cached_embeddings]
    return chunk_ids == cached_ids


def build_or_load_embeddings(
    chunks: list[dict],
    model: str,
    ollama_url: str,
    cache_path: Path,
    rebuild_cache: bool,
    timeout: int,
) -> list[dict]:
    if cache_path.exists() and not rebuild_cache:
        try:
            with cache_path.open("r", encoding="utf-8") as f:
                cache = json.load(f)
            if cache_matches(cache, chunks, model):
                return cache["embeddings"]
        except json.JSONDecodeError:
            print(f"경고: 캐시 파일이 손상되어 새로 계산합니다 ({cache_path})")

    embeddings = []
    for index, chunk in enumerate(chunks, start=1):
        print(f"Embedding chunk {index}/{len(chunks)}: {chunk['chunk_id']}")
        embedding = embed_text(chunk["text"], model, ollama_url, timeout)
        embeddings.append({"chunk_id": chunk["chunk_id"], "embedding": embedding})

    cache = {
        "model": model,
        "source_chunks": str(CHUNKS_PATH),
        "embeddings": embeddings,
    }
    with cache_path.open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)

    return embeddings


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and cache Ollama embeddings for chunks.")
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH, help="Path to chunks JSONL")
    parser.add_argument("--cache", type=Path, default=EMBEDDINGS_PATH, help="Embedding cache path")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama embedding model")
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL, help="Ollama base URL")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Ollama request timeout in seconds")
    parser.add_argument("--rebuild-cache", action="store_true", help="Recompute all embeddings")
    args = parser.parse_args()

    check_ollama(args.ollama_url, args.timeout)
    chunks = load_chunks(args.chunks)
    embeddings = build_or_load_embeddings(
        chunks=chunks,
        model=args.model,
        ollama_url=args.ollama_url,
        cache_path=args.cache,
        rebuild_cache=args.rebuild_cache,
        timeout=args.timeout,
    )

    print(f"완료: {len(embeddings)}개 chunk 임베딩 -> {args.cache}")


if __name__ == "__main__":
    main()