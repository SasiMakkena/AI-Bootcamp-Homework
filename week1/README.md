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

week1/
├── main.py # 🧠 Orchestrates the pipeline
├── github_reader.py # ⬇️ Downloads & filters GitHub files
├── parser_podcast.py # 🧾 Parses YAML + markdown
├── chunker.py # ✂️ Creates overlapping text chunks
├── indexer.py # 🔍 Builds & queries the MinSearch index
├── utils.py # 🪶 Helper tools like step logger
└── README.md # 📘 Project documentation

yaml
Copy code

---

## 🧩 Technologies Used

| Tool | What it is | What it does here |
|------|-------------|------------------|
| **Python** | Programming language | Runs the entire pipeline |
| **Markdown (.md)** | Lightweight text format | Used for docs & podcast files |
| **YAML (.yml / .yaml)** | Data format (key-value pairs) | Stores podcast metadata |
| **Bash (Terminal commands)** | Command-line language | Runs and installs your project |
| **minsearch** | Python search engine | Builds a simple text index |
| **requests** | HTTP library | Downloads GitHub repos |
| **PyYAML** | YAML parser | Reads metadata sections |

---

## 💡 Quick Primer: Markdown, YAML & Bash

### 📝 Markdown
Markdown = *formatted plain text*.  
Used for `README.md` and `.md` podcast files.

```markdown
# Title
**bold text**
*italic text*
- bullet point
1. numbered list
`inline code`
💬 On GitHub this becomes formatted text with headings, bold, etc.

⚙️ YAML
YAML = structured data (used at the top of podcast files):

yaml
Copy code
title: "Standing out as a Data Scientist"
season: 1
episode: 4
guests: [lukewhipps]
links:
  youtube: https://www.youtube.com/watch?v=Sb4CJlonB3c
  spotify: https://open.spotify.com/episode/2Yxay9HJmd6dvk34MHJ0K2
Your Python code converts this into a dictionary like:

python
Copy code
{
  "title": "Standing out as a Data Scientist",
  "season": 1,
  "episode": 4,
  "guests": ["lukewhipps"]
}
💻 Bash
Bash = terminal command language.
You run commands like this in PowerShell or Terminal:

bash
Copy code
pip install requests pyyaml minsearch
python week1/main.py
These tell your system to install dependencies and run the main Python file.

⚙️ Setup Instructions
1️⃣ Install Python Libraries
Open a terminal in the project folder and run:

bash
Copy code
pip install requests pyyaml minsearch scikit-learn
2️⃣ Run the Project
bash
Copy code
python week1/main.py
3️⃣ Sample Output
less
Copy code
[1] Reading GitHub repository
  Retrieved 183 podcast files
[2] Parsing example podcast
  Title: Data Team Roles Explained
[3] Chunking all files (size=30, overlap=15)
  Total chunks created: 253
[4] Building MinSearch index
[5] Query: how do I make money with AI?
  Top Results:
   1. Entrepreneurship Journey
   2. Building Machine Learning Products
   3. AI in Industry
🧱 Pipeline Stages
Step	Description	Output
1️⃣ GitHub Fetch	Downloads podcast markdowns	183 files
2️⃣ Parse Metadata	Extracts YAML fields	title, guests, etc.
3️⃣ Chunk Text	Paragraph-based slicing	~250 chunks
4️⃣ Build Index	Create search index	TF-IDF index
5️⃣ Query	Find relevant episodes	Ranked list of results

🔮 Next Steps
Goal	Example
💾 Export chunks	pandas.DataFrame(all_chunks).to_csv("chunks.csv")
🧮 Add embeddings	Use OpenAI or Hugging Face
🧠 Build RAG pipeline	Feed top-k chunks to an LLM
🌐 Host search UI	Streamlit or FastAPI app

🧑‍💻 Author
Mak S.
📍 Sunshine Daycare LLC / AI Bootcamp Homework
💬 “Every bright mind deserves a bright start — and a clean codebase.”

<p align="center"> <i>✨ Run <code>main.py</code> to start building your own AI-powered podcast search!</i> </p> ```