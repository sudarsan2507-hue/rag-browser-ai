# rag-browser-ai

A RAG pipeline that acquires its own knowledge from the web: search -> fetch ->
extract -> chunk -> embed -> store -> retrieve -> generate.

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Playwright's browser binary (not covered by pip):
   ```
   playwright install chromium
   ```
4. Install [Ollama](https://ollama.com) and pull the model this project uses:
   ```
   ollama pull llama3.2:3b
   ```
   Ollama must be running (`ollama serve`, or the desktop app) before running the pipeline.

## Running

```
python main.py
```

You'll be prompted for a query. A visible Chromium window opens (slowed down
on purpose so each step is watchable), searches DuckDuckGo, visits the top
results, extracts and chunks their content, embeds and stores it in a
persistent local vector store (`chroma_data/`), retrieves the most relevant
chunks for your query, and asks the local LLM to answer using only that
retrieved context, with sources cited.

Knowledge accumulates across runs - `chroma_data/` isn't cleared between
invocations, so previously fetched pages remain searchable later.

### Environment variables

- `RAG_HEADLESS` - set to `true` to run the browser headless (default `false`)
- `RAG_SLOW_MO` - milliseconds of artificial delay per browser action (default `100`)

## Tests

```
pytest
```

Covers the pure-logic modules (`retrieval/chunker.py`, `retrieval/cleaner.py`).
Modules that depend on a live browser, the embedding model, or an LLM aren't
covered by automated tests - those are verified by running the pipeline directly.

## Project layout

- `browser/` - Playwright-driven search
- `interface/` - CLI query input
- `retrieval/` - fetch, clean, and chunk page content
- `rag/` - embedding, persistent vector storage, retrieval
- `llm/` - grounded answer generation via Ollama
- `main.py` - orchestrates the full pipeline
