<!-- ─────────────────────────────────────────────── -->
<!-- 🔖 PROJECT HEADER -->
<!-- ─────────────────────────────────────────────── -->
<h1 align="center">🎧 Podcast RAG Pipeline</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python 3.12"/>
  <img src="https://img.shields.io/badge/RAG-Enabled-brightgreen?logo=openai" alt="RAG Enabled"/>
  <img src="https://img.shields.io/badge/Data-GitHub%20Repo-orange?logo=github" alt="GitHub Data"/>
  <img src="https://img.shields.io/badge/Search-MinSearch-yellow?logo=elastic" alt="MinSearch"/>
</p>

<p align="center">
  <b>📚 DataTalksClub – Podcast Knowledge Search & QA</b><br>
  <i>Download → Parse → Chunk → Index → Query</i>
</p>

---

## 🌟 Overview

This project builds a **searchable knowledge base** from the  
[`DataTalksClub/datatalksclub.github.io`](https://github.com/DataTalksClub/datatalksclub.github.io) repository using **Python**.

It:
- ⬇️ Downloads podcast markdown files (`_podcast/*.md`)
- 🧾 Parses their **YAML** metadata (title, episode, guests, links)
- ✂️ Breaks content into paragraph chunks
- 🔍 Builds a **search index** with `minsearch`
- 🧠 Lets you query podcasts (like “How do I make money with AI?”)

---

## 🧭 Directory Structure

```bash
week1/
├── main.py                # 🧠 Orchestrates the pipeline
├── github_reader.py       # ⬇️ Downloads & filters GitHub files
├── parser_podcast.py      # 🧾 Parses YAML + markdown
├── chunker.py             # ✂️ Creates overlapping text chunks
├── indexer.py             # 🔍 Builds & queries the MinSearch index
├── utils.py               # 🪶 Helper tools like step logger
└── README.md              # 📘 Project documentation
