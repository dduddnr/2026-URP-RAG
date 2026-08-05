from pathlib import Path
import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parents[1] / "chunking_embedding"))
sys.path.append(str(Path(__file__).resolve().parents[1] / "retriever"))

ENV_PATH = Path(__file__).resolve().parents[3] / "data_KG_ver_1" / ".env"
load_dotenv(dotenv_path=ENV_PATH)

from dense_embed_chunks import (
    CHUNKS_PATH,
    EMBEDDINGS_PATH,
    FOLDER_ROOT,
    DEFAULT_OLLAMA_URL,
    DEFAULT_MODEL,
    DEFAULT_TIMEOUT,
    load_chunks,
    check_ollama,
    build_or_load_embeddings,
)
import hybrid_retriever
from generate import retrieve_chunks, build_prompt, generate_answer

REPORT_MD_PATH = FOLDER_ROOT / "data" / "compare_generation.md"
REPORT_JSON_PATH = FOLDER_ROOT / "data" / "compare_generation.json"

DEFAULT_GEN_MODEL = "gpt-4o-mini"
METHODS = ["cosine", "euclidean", "hybrid"]

DEFAULT_QUERIES = [
    "Dürer engravings",
    "1944 27 Martyrs shot by Nazis",
    "What is Albrecht Dürer known for?",
    "football club founded in Finland",
    "France government type",
]


def run_one(method, query, chunks, embeddings, bm25, client, gen_model,
            embed_model, ollama_url, timeout, top_k, alpha):
    retrieved = retrieve_chunks(
        method, query, chunks, embeddings, bm25,
        embed_model, ollama_url, timeout, top_k, alpha,
    )
    prompt = build_prompt(query, retrieved)
    answer = generate_answer(client, gen_model, prompt)
    return {
        "retrieved_chunk_ids": [item["chunk_id"] for item in retrieved],
        "answer": answer,
    }


def write_markdown_report(comparisons, path):
    lines = ["# Generation 비교 리포트 (cosine vs euclidean vs hybrid)\n"]
    for item in comparisons:
        lines.append(f"## Query: {item['query']}\n")
        for method in METHODS:
            result = item["results"][method]
            lines.append(f"**{method}** (검색된 chunk: {', '.join(result['retrieved_chunk_ids'])})\n")
            lines.append(f"> {result['answer']}\n")
        lines.append("---\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Compare generated answers across cosine/euclidean/hybrid retrieval")
    parser.add_argument("--queries", type=Path)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH)
    parser.add_argument("--cache", type=Path, default=EMBEDDINGS_PATH)
    parser.add_argument("--embed-model", default=DEFAULT_MODEL)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--gen-model", default=DEFAULT_GEN_MODEL)
    parser.add_argument("--output-md", type=Path, default=REPORT_MD_PATH)
    parser.add_argument("--output-json", type=Path, default=REPORT_JSON_PATH)
    args = parser.parse_args()

    queries = (
        [line.strip() for line in args.queries.read_text(encoding="utf-8").splitlines() if line.strip()]
        if args.queries else DEFAULT_QUERIES
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다 (.env 확인).")
    client = OpenAI(api_key=api_key)

    print(f"쿼리 {len(queries)}개 x 방식 3개 = OpenAI 호출 {len(queries) * 3}회 예정")

    check_ollama(args.ollama_url, args.timeout)
    chunks = load_chunks(args.chunks)
    embeddings = build_or_load_embeddings(
        chunks=chunks, model=args.embed_model, ollama_url=args.ollama_url,
        cache_path=args.cache, rebuild_cache=False, timeout=args.timeout,
    )
    bm25 = hybrid_retriever.build_bm25(chunks)

    comparisons = []
    for index, query in enumerate(queries, start=1):
        print(f"[{index}/{len(queries)}] {query}")
        results = {}
        for method in METHODS:
            print(f"  - {method} 검색 + 생성 중...")
            results[method] = run_one(
                method, query, chunks, embeddings, bm25, client, args.gen_model,
                args.embed_model, args.ollama_url, args.timeout, args.top_k, args.alpha,
            )
        comparisons.append({"query": query, "results": results})

    write_markdown_report(comparisons, args.output_md)
    args.output_json.write_text(json.dumps(comparisons, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n완료: {len(comparisons)}개 쿼리 비교")
    print(f"  markdown -> {args.output_md}")
    print(f"  json     -> {args.output_json}")


if __name__ == "__main__":
    main()