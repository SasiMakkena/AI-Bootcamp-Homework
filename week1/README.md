# Podcast RAG (DataTalksClub / _podcast)

This project downloads podcast markdown files from the
[DataTalksClub/datatalksclub.github.io](https://github.com/DataTalksClub/datatalksclub.github.io)
repository, parses their YAML frontmatter and content, chunks them into
paragraph-based windows, and builds a simple MinSearch index for Q&A.

## Pipeline

1. **Read GitHub repository**
   - Downloads `main` branch ZIP via codeload
   - Filters to `_podcast/*.md` and `_podcast/*.mdx`
   - Ignores filenames starting with `_` (e.g., `_template.md`)

2. **Parse podcasts**
   - Extracts YAML frontmatter if present (safe fallback)
   - Normalizes: `title`, `season`, `episode`, `guests`, `links`, `ids`
   - Keeps `transcript` if available; otherwise uses markdown body

3. **Chunk**
   - Paragraph-based chunking
   - Window size = 30 blocks, overlap = 15
   - Adds metadata: `episode_title`, `filename`, `chunk_id`, `youtube`

4. **Index & Query**
   - Builds a MinSearch index over chunks
   - Sample query: “how do I make money with AI?”

## Project Layout

