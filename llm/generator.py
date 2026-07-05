import ollama

MODEL = "llama3.2:3b"


def ensure_ollama_ready():
    try:
        available = [m.model for m in ollama.list().models]
    except Exception as e:
        raise SystemExit(
            f"Can't reach Ollama ({e}). Make sure it's running before starting this pipeline."
        )

    if MODEL not in available:
        raise SystemExit(
            f"Model '{MODEL}' isn't pulled yet. Run: ollama pull {MODEL}"
        )


def build_prompt(query, retrieved):
    context_blocks = [
        f"[{i}] {meta['title']}\n{chunk}"
        for i, (chunk, meta, _distance) in enumerate(retrieved, 1)
    ]
    context = "\n\n".join(context_blocks)

    return f"""Answer the question using ONLY the context below. If the context doesn't contain enough information to answer, say so honestly instead of guessing. Cite sources inline using their [number].

Context:
{context}

Question: {query}

Answer:"""


def generate_answer(query, retrieved):
    prompt = build_prompt(query, retrieved)
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]
