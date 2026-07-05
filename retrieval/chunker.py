def split_oversized(paragraph, max_chars, overlap):
    if overlap >= max_chars:
        raise ValueError("overlap must be smaller than max_chars")

    chunks = []
    start = 0

    while start < len(paragraph):
        end = start + max_chars
        chunks.append(paragraph[start:end])
        start = end - overlap

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
