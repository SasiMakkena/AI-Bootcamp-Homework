"""
Main orchestrator for the Podcast RAG pipeline.

Steps:
[1] Read GitHub repository (_podcast/*.md, ignoring underscored files)
[2] Parse podcast files (frontmatter + body)
[3] Chunk text (paragraph-based; size=30, overlap=15)
[4] Build MinSearch index and run a sample query
"""

from indexer import build_index, search_index
from github_reader import GithubRepositoryDataReader
from parser_podcast import parse_podcast_raw
from chunker import extract_text_blocks, format_chunks, process_podcast_file
from utils import StepLogger

QUERY = "how do I make money with AI?"


def read_github_data(repo_owner: str, repo_name: str):
    """
    Use GithubRepositoryDataReader to read only _podcast/*.md or .mdx,
    ignoring files that start with "_" (e.g., _template.md).
    """
    allowed_extensions = {"md", "mdx"}

    def only_podcast(filepath: str) -> bool:
        # Keep only _podcast/*.md or .mdx
        if not filepath.startswith("_podcast/"):
            return False
        filename = filepath.split("/")[-1]
        if filename.startswith("_"):
            return False
        return filename.endswith(".md") or filename.endswith(".mdx")

    reader = GithubRepositoryDataReader(
        repo_owner=repo_owner,
        repo_name=repo_name,
        allowed_extensions=allowed_extensions,
        filename_filter=only_podcast,
    )
    return reader.read()


def main() -> None:
    log = StepLogger()

    # [1] Read GitHub repo
    log.step("Reading GitHub repository")
    data_raw = read_github_data("DataTalksClub", "datatalksclub.github.io")
    log.note(f"Retrieved {len(data_raw)} podcast files")
    for i, f in enumerate(data_raw[:10], 1):
        log.note(f"{i:02d}. {f.filename}")

    # [2] Parse a sample file (show keys) — quick sanity check
    log.step("Parsing a sample podcast file (sanity check)")
    sample = parse_podcast_raw(data_raw[0])
    log.note(f"Keys: {list(sample.keys())}")
    log.note(f"Title: {sample['title']}")
    log.note(f"Guests: {sample['guests']}")
    log.note(f"YouTube: {sample['links'].get('youtube')}")
    log.note(f"Transcript lines: {len(sample['transcript'])}")
    log.note(f"Body length: {len(sample['body'])}")

    # [3] Chunking — process ALL files
    log.step("Chunking all podcast files (size=30, overlap=15)")
    all_chunks = []
    for rf in data_raw:
        try:
            chunks = process_podcast_file(rf, size=30, overlap=15)
            all_chunks.extend(chunks)
            if chunks:
                log.note(f"{rf.filename}: {len(chunks)} chunks")
            else:
                log.note(f"{rf.filename}: no text found")
        except Exception as e:
            log.note(f"{rf.filename}: ERROR {e}")

    log.note(f"Total chunks created across all episodes: {len(all_chunks)}")

    # [4] Index & query
    log.step("Building MinSearch index & querying")
    index = build_index(all_chunks, text_fields=["text", "episode_title"],
                        keyword_fields=["filename", "youtube"])
    results = search_index(index, QUERY, num_results=5)
    log.note(f"Top 5 results for: {QUERY}")
    for i, r in enumerate(results, 1):
        line = f"{i:02d}. {r['episode_title']} — {r['filename']}"
        if r.get("youtube"):
            line += f"\n      🎥 {r['youtube']}"
        log.note(line)


if __name__ == "__main__":
    main()
