from pathlib import Path
import argparse
import os
import sys

from openai import OpenAI

from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[3] / "data_KG_ver_1" / ".env"
load_dotenv(dotenv_path=ENV_PATH)

sys.path.append(str(Path(__file__).resolve().parents[1] / "chunking_embedding"))
sys.path.append(str(Path(__file__).resolve().parents[1] / "retriever"))

from dense_embed_chunks import (
    CHUNKS_PATH,
    EMBEDDINGS_PATH,
    DEFAULT_OLLAMA_URL,
    DEFAULT_MODEL,
    DEFAULT_TIMEOUT,
    load_chunks,
    check_ollama,
    build_or_load_embeddings,
)
import cosine_retriever
import euclidean_retriever
import hybrid_retriever

DEFAULT_GEN_MODEL = "gpt-4o-mini"


def retrieve_chunks(method, query, chunks, embeddings, bm25, embed_model, ollama_url, timeout, top_k, alpha):
    if method == "cosine":
        return cosine_retriever.search(query, chunks, embeddings, embed_model, ollama_url, timeout, top_k)
    if method == "euclidean":
        return euclidean_retriever.search(query, chunks, embeddings, embed_model, ollama_url, timeout, top_k)
    if method == "hybrid":
        return hybrid_retriever.search(query, chunks, embeddings, bm25, embed_model, ollama_url, timeout, top_k, alpha)
    raise ValueError(f"Unknown method: {method}")


def build_prompt(query, retrieved):
    context = "\n\n".join(f"[{item['chunk_id']}] {item['text']}" for item in retrieved)
    return f"""다음은 질문에 답하는 데 참고할 수 있는 Wikipedia 문서 조각들입니다.

{context}

위 문서만 참고해서 아래 질문에 답하세요.
- 문서에 있는 내용만 사용하고, 모르는 내용은 추측하지 마세요.
- 문서에서 답을 찾을 수 없으면 "제공된 문서에서 답을 찾을 수 없습니다"라고 답하세요.
- 답변에 어떤 chunk_id를 근거로 썼는지 마지막 줄에 표시하세요.

질문: {query}

답변:"""


def generate_answer(client, gen_model, prompt):
    response = client.chat.completions.create(
        model=gen_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.2,
    )
    return response.choices[0].message.content


def print_retrieved(retrieved, method):
    print("=== 검색된 chunk ===")
    for rank, item in enumerate(retrieved, start=1):
        preview = item["text"].replace("\n", " ")
        if len(preview) > 120:
            preview = preview[:120].rstrip() + "..."

        if method == "hybrid":
            score_str = f"score={item['score']:.4f} (dense={item['dense_score']:.4f}, sparse={item['sparse_score']:.4f})"
        elif method == "euclidean":
            score_str = f"distance={item['distance']:.4f}"
        else:
            score_str = f"score={item['score']:.4f}"

        print(f"[{rank}] {item['chunk_id']} ({item['section']}) {score_str}")
        print(f"    {preview}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Retrieve chunks then generate an answer with OpenAI GPT.")
    parser.add_argument("query")
    parser.add_argument("--method", choices=["cosine", "euclidean", "hybrid"], default="hybrid")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH)
    parser.add_argument("--cache", type=Path, default=EMBEDDINGS_PATH)
    parser.add_argument("--embed-model", default=DEFAULT_MODEL)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--gen-model", default=DEFAULT_GEN_MODEL)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다. "
            "PowerShell에서 $env:OPENAI_API_KEY = \"sk-...\" 로 설정해주세요."
        )
    client = OpenAI(api_key=api_key)

    check_ollama(args.ollama_url, args.timeout)
    chunks = load_chunks(args.chunks)
    embeddings = build_or_load_embeddings(
        chunks=chunks, model=args.embed_model, ollama_url=args.ollama_url,
        cache_path=args.cache, rebuild_cache=False, timeout=args.timeout,
    )
    bm25 = hybrid_retriever.build_bm25(chunks) if args.method == "hybrid" else None

    retrieved = retrieve_chunks(
        args.method, args.query, chunks, embeddings, bm25,
        args.embed_model, args.ollama_url, args.timeout, args.top_k, args.alpha,
    )

    print(f"Query: {args.query}  (method={args.method})\n")
    print_retrieved(retrieved, args.method)

    prompt = build_prompt(args.query, retrieved)
    answer = generate_answer(client, args.gen_model, prompt)

    print("=== 답변 ===")
    print(answer)


if __name__ == "__main__":
    main()