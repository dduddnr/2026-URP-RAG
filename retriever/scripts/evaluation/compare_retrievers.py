from pathlib import Path
import argparse
import json
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RETRIEVAL_DIR = PROJECT_ROOT / "scripts" / "retrieval"
CHUNKS_PATH = PROJECT_ROOT / "data" / "processed" / "survey_on_rag2_chunks.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "retriever_comparison.json"
REPORT_PATH = PROJECT_ROOT / "data" / "processed" / "retriever_comparison.md"

sys.path.append(str(RETRIEVAL_DIR))

import bm25_retriever
import dense_ollama_retriever
import tfidf_retriever


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


DEFAULT_QUERIES = [
    "BM25 sparse retrieval", #명확한 keyword query에서 세 retriever 비교
    "dense retrieval embedding",
    "retrieval granularity chunk entity",
    "query rewriting",
    "Self-RAG", 
    "How does RAG reduce hallucination?",
    "What are training-free RAG methods?",
    "What is the difference between sparse retrieval and dense retrieval?",
    "What is retrieval granularity in RAG?",
    "What are pre-retrieval and post-retrieval techniques?",
    "How is Wikipedia used as an external database in RAG?",
    "What is input-layer integration?", #가까운 section에 있는 query와 관련된 chunk를 top-k로 반환하는지 비교
    "What is output-layer integration?",
    "What is intermediate-layer integration?",
    "What are independent training, sequential training, and joint training?", # 
    "What are the future challenges of RA-LLMs?",
    "Why can irrelevant retrieved passages hurt generation?",
    "What applications use retrieval-augmented large language models?",
    "How can the model use outside knowledge to avoid wrong answers?",
    "How does the system decide whether to retrieve more information?",
    "What methods modify the user question before searching?",
    "How can external documents make generated answers more reliable?",
    "What happens when retrieved information is noisy or unrelated?",
    "How can a model answer questions about information not seen during training?",
    "How can retrieved passages be shortened before being given to the generator?",
]


def trim_result(result: dict, preview_chars: int) -> dict:
    preview = result["text"].replace("\n", " ")
    if len(preview) > preview_chars:
        preview = preview[:preview_chars].rstrip() + "..."

    return {
        "score": result["score"],
        "chunk_id": result["chunk_id"],
        "page": result["page"],
        "chunk_index": result["chunk_index"],
        "preview": preview,
    }


def build_bm25_runner(chunks: list[dict]):
    bm25 = bm25_retriever.build_bm25(chunks)

    def run(query: str, top_k: int) -> list[dict]:
        return bm25_retriever.search(query, chunks, bm25, top_k)

    return run


def build_tfidf_runner(chunks: list[dict]):
    vectorizer, matrix = tfidf_retriever.build_tfidf(chunks)

    def run(query: str, top_k: int) -> list[dict]:
        return tfidf_retriever.search(query, chunks, vectorizer, matrix, top_k)

    return run


def build_dense_runner(
    chunks: list[dict],
    model: str,
    ollama_url: str,
    timeout: int,
    rebuild_cache: bool,
):
    dense_ollama_retriever.check_ollama(ollama_url, timeout)
    embeddings = dense_ollama_retriever.build_or_load_embeddings(
        chunks=chunks,
        model=model,
        ollama_url=ollama_url,
        cache_path=dense_ollama_retriever.EMBEDDINGS_PATH,
        rebuild_cache=rebuild_cache,
        timeout=timeout,
    )

    def run(query: str, top_k: int) -> list[dict]:
        return dense_ollama_retriever.search(
            query=query,
            chunks=chunks,
            embeddings=embeddings,
            model=model,
            ollama_url=ollama_url,
            timeout=timeout,
            top_k=top_k,
        )

    return run


def print_comparison(comparison: list[dict], methods: list[str], preview_chars: int) -> None:
    for item in comparison:
        print("=" * 88)
        print(f"Query: {item['query']}")
        print("=" * 88)

        for method in methods:
            print(f"\n[{method.upper()}]")
            for rank, result in enumerate(item["results"][method], start=1):
                print(
                    f"{rank}. score={result['score']:.4f} "
                    f"{result['chunk_id']} page={result['page']} "
                    f"chunk={result['chunk_index']}"
                )
                print(f"   {result['preview'][:preview_chars]}")
        print()


def markdown_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def format_score(score: float) -> str:
    return f"{score:.4f}"


def top1_summary_row(item: dict, methods: list[str]) -> str:
    cells = [markdown_escape(item["query"])]
    top_ids = []

    for method in methods:
        result = item["results"][method][0]
        top_ids.append(result["chunk_id"])
        cells.append(
            f"{result['chunk_id']}<br>p.{result['page']} "
            f"c.{result['chunk_index']}<br>{format_score(result['score'])}"
        )

    agreement = "same" if len(set(top_ids)) == 1 else "different"
    cells.append(agreement)
    return "| " + " | ".join(cells) + " |"


def write_markdown_report(
    comparison: list[dict],
    methods: list[str],
    output_path: Path,
) -> None:
    lines = [
        "# Retriever Comparison",
        "",
        "BM25, TF-IDF, Dense Ollama retriever의 검색 결과를 같은 query 기준으로 비교한 리포트입니다.",
        "",
        "## Top-1 Summary",
        "",
        "| Query | " + " | ".join(method.upper() for method in methods) + " | Agreement |",
        "| --- | " + " | ".join("---" for _ in methods) + " | --- |",
    ]

    for item in comparison:
        lines.append(top1_summary_row(item, methods))

    lines.extend(["", "## Detailed Results", ""])

    for item in comparison:
        lines.extend([f"### {markdown_escape(item['query'])}", ""])

        for method in methods:
            lines.extend([f"#### {method.upper()}", ""])
            lines.append("| Rank | Score | Chunk | Page | Preview |")
            lines.append("| --- | ---: | --- | ---: | --- |")

            for rank, result in enumerate(item["results"][method], start=1):
                preview = markdown_escape(result["preview"])
                lines.append(
                    f"| {rank} | {format_score(result['score'])} | "
                    f"{result['chunk_id']} | {result['page']} | {preview} |"
                )

            lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare BM25, TF-IDF, and Ollama dense retrieval results."
    )
    parser.add_argument("--top-k", type=int, default=3, help="Number of results per method")
    parser.add_argument(
        "--query",
        action="append",
        dest="queries",
        help="Query to evaluate. Can be used multiple times.",
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        default=["bm25", "tfidf", "dense"],
        choices=["bm25", "tfidf", "dense"],
        help="Retrievers to compare",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH, help="JSON output path")
    parser.add_argument(
        "--report",
        type=Path,
        default=REPORT_PATH,
        help="Markdown report output path",
    )
    parser.add_argument("--preview-chars", type=int, default=280, help="Preview length")
    parser.add_argument("--model", default=dense_ollama_retriever.DEFAULT_MODEL)
    parser.add_argument("--ollama-url", default=dense_ollama_retriever.DEFAULT_OLLAMA_URL)
    parser.add_argument("--timeout", type=int, default=dense_ollama_retriever.DEFAULT_TIMEOUT)
    parser.add_argument("--rebuild-dense-cache", action="store_true")
    args = parser.parse_args()

    queries = args.queries or DEFAULT_QUERIES
    chunks = bm25_retriever.load_chunks(CHUNKS_PATH)

    runners = {}
    if "bm25" in args.methods:
        runners["bm25"] = build_bm25_runner(chunks)
    if "tfidf" in args.methods:
        runners["tfidf"] = build_tfidf_runner(chunks)
    if "dense" in args.methods:
        runners["dense"] = build_dense_runner(
            chunks=chunks,
            model=args.model,
            ollama_url=args.ollama_url,
            timeout=args.timeout,
            rebuild_cache=args.rebuild_dense_cache,
        )

    comparison = []
    for query in queries:
        method_results = {}
        for method in args.methods:
            results = runners[method](query, args.top_k)
            method_results[method] = [
                trim_result(result, args.preview_chars) for result in results
            ]

        comparison.append({"query": query, "results": method_results})

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(comparison, f, ensure_ascii=False, indent=2)

    write_markdown_report(comparison, args.methods, args.report)
    print_comparison(comparison, args.methods, args.preview_chars)
    print(f"Saved comparison to: {args.output}")
    print(f"Saved markdown report to: {args.report}")


if __name__ == "__main__":
    main()
