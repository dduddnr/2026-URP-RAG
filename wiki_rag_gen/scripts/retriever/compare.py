from pathlib import Path
import argparse
import json
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "chunking_embedding"))

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

# cosine / euclidean / hybrid 세 방식을 같은 쿼리셋으로 돌려서
# top-1이 서로 같은지(agreement), 점수는 어떻게 다른지 markdown 리포트로 정리한다.

REPORT_MD_PATH = Path(__file__).resolve().parents[2] / "data" / "compare_retrieval.md"
REPORT_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "compare_retrieval.json"

DEFAULT_QUERIES = [
    #키워드/고유명사형
    "Dürer engravings",
    
    #숫자/사실 특정형
    "1944 27 Martyrs shot by Nazis",

    #자연어
    "What is Albrecht Dürer known for?",
    
    #cross-entity 혼합
    "football club founded in Finland",
    
    #섹션 자체가 없는 경우(정답 없음/할루시네이션 방지 측정)
    "France government type",
]


def run_query(query: str, chunks, embeddings, bm25, model, ollama_url, timeout, top_k, alpha):
    cosine_results = cosine_retriever.search(query, chunks, embeddings, model, ollama_url, timeout, top_k)
    euclidean_results = euclidean_retriever.search(query, chunks, embeddings, model, ollama_url, timeout, top_k)
    hybrid_results = hybrid_retriever.search(query, chunks, embeddings, bm25, model, ollama_url, timeout, top_k, alpha)
    return {
        "cosine": cosine_results,
        "euclidean": euclidean_results,
        "hybrid": hybrid_results,
    }


def top1_agreement(results: dict) -> str:
    ids = {method: (r[0]["chunk_id"] if r else None) for method, r in results.items()}
    unique_ids = set(ids.values())
    if len(unique_ids) == 1:
        return "all_same"
    if len(unique_ids) == len(ids):
        return "all_different"
    return "partial"


def format_preview(text: str, limit: int = 150) -> str:
    preview = text.replace("\n", " ")
    if len(preview) > limit:
        preview = preview[:limit].rstrip() + "..."
    return preview


def write_markdown_report(comparisons: list[dict], path: Path) -> None:
    lines = ["# Cosine vs Euclidean vs Hybrid 비교 리포트\n"]

    lines.append("## Top-1 요약\n")
    lines.append("| Query | Cosine top-1 | Euclidean top-1 | Hybrid top-1 | Agreement |")
    lines.append("|---|---|---|---|---|")
    for item in comparisons:
        results = item["results"]
        cosine_id = results["cosine"][0]["chunk_id"] if results["cosine"] else "-"
        euclidean_id = results["euclidean"][0]["chunk_id"] if results["euclidean"] else "-"
        hybrid_id = results["hybrid"][0]["chunk_id"] if results["hybrid"] else "-"
        lines.append(
            f"| {item['query']} | {cosine_id} | {euclidean_id} | {hybrid_id} | {item['agreement']} |"
        )

    agreement_counts = {}
    for item in comparisons:
        agreement_counts[item["agreement"]] = agreement_counts.get(item["agreement"], 0) + 1
    lines.append("\n## Agreement 분포\n")
    for label, count in agreement_counts.items():
        lines.append(f"- {label}: {count}개")

    lines.append("\n## 상세 결과 (top-3까지)\n")
    for item in comparisons:
        lines.append(f"### Query: {item['query']}  (agreement={item['agreement']})\n")
        for method in ["cosine", "euclidean", "hybrid"]:
            lines.append(f"**{method}**")
            for rank, result in enumerate(item["results"][method][:3], start=1):
                score_label = "distance" if method == "euclidean" else "score"
                score_value = result.get("distance", result.get("score"))
                lines.append(
                    f"- [{rank}] {score_label}={score_value:.4f} "
                    f"`{result['chunk_id']}` ({result['section']}): {format_preview(result['text'])}"
                )
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare cosine / euclidean / hybrid retrieval")
    parser.add_argument("--queries", type=Path, help="한 줄에 쿼리 하나씩 있는 텍스트 파일 (없으면 기본 쿼리셋 사용)")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.5, help="hybrid의 dense 비중")
    parser.add_argument("--chunks", type=Path, default=CHUNKS_PATH)
    parser.add_argument("--cache", type=Path, default=EMBEDDINGS_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--output-md", type=Path, default=REPORT_MD_PATH)
    parser.add_argument("--output-json", type=Path, default=REPORT_JSON_PATH)
    args = parser.parse_args()

    if args.queries:
        queries = [line.strip() for line in args.queries.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        queries = DEFAULT_QUERIES

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
    bm25 = hybrid_retriever.build_bm25(chunks)

    comparisons = []
    for index, query in enumerate(queries, start=1):
        print(f"[{index}/{len(queries)}] {query}")
        results = run_query(
            query, chunks, embeddings, bm25,
            args.model, args.ollama_url, args.timeout, args.top_k, args.alpha,
        )
        comparisons.append({
            "query": query,
            "results": results,
            "agreement": top1_agreement(results),
        })

    write_markdown_report(comparisons, args.output_md)

    json_ready = [
        {
            "query": item["query"],
            "agreement": item["agreement"],
            "results": item["results"],
        }
        for item in comparisons
    ]
    args.output_json.write_text(json.dumps(json_ready, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n완료: {len(comparisons)}개 쿼리 비교")
    print(f"  markdown -> {args.output_md}")
    print(f"  json     -> {args.output_json}")


if __name__ == "__main__":
    main()