import re

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def raw_windows(text, max_chars, overlap):
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def pack_sentences(sentences, max_chars):
    chunks = []
    buffer = ""

    for sentence in sentences:
        if not buffer:
            buffer = sentence
        elif len(buffer) + 1 + len(sentence) <= max_chars:
            buffer += " " + sentence
        else:
            chunks.append(buffer)
            buffer = sentence

    if buffer:
        chunks.append(buffer)

    return chunks


def split_oversized(paragraph, max_chars, overlap):
    if overlap >= max_chars:
        raise ValueError("overlap must be smaller than max_chars")

    sentences = SENTENCE_BOUNDARY.split(paragraph)

    if len(sentences) == 1:
        return raw_windows(paragraph, max_chars, overlap)

    chunks = []
    for chunk in pack_sentences(sentences, max_chars):
        if len(chunk) > max_chars:
            chunks.extend(raw_windows(chunk, max_chars, overlap))
        else:
            chunks.append(chunk)

    return chunks


def chunk_text(text, max_chars=800, overlap=100):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    buffer = ""

    for para in paragraphs:
        if len(para) > max_chars:
            if buffer:
                chunks.append(buffer)
                buffer = ""
            chunks.extend(split_oversized(para, max_chars, overlap))
            continue

        if not buffer:
            buffer = para
        elif len(buffer) + 2 + len(para) <= max_chars:
            buffer += "\n\n" + para
        else:
            chunks.append(buffer)
            buffer = para

    if buffer:
        chunks.append(buffer)

    return chunks
