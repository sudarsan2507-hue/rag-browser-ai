from bs4 import BeautifulSoup
from readability import Document


BLOCK_TAGS = ["p", "li", "h1", "h2", "h3", "h4"]
CONTAINER_TAGS = ["div", "section", "article"]


def extract_readability(html):
    summary_html = Document(html).summary()
    soup = BeautifulSoup(summary_html, "html.parser")

    texts = _block_texts(soup, BLOCK_TAGS)
    if texts:
        return "\n\n".join(texts)

    # No semantic block tags - fall back to leaf-level containers (div/section/
    # article with no block-level children), skipping ones that would just
    # duplicate a nested container's text.
    leaf_containers = [
        b for b in soup.find_all(CONTAINER_TAGS)
        if not b.find(CONTAINER_TAGS + BLOCK_TAGS)
    ]
    texts = _block_texts(soup, tags=None, elements=leaf_containers)
    if texts:
        return "\n\n".join(texts)

    print("Warning: extract_readability found no block structure, falling back to flat text (paragraph boundaries lost)")
    return soup.get_text(separator=" ", strip=True)


def _block_texts(soup, tags, elements=None):
    blocks = elements if elements is not None else soup.find_all(tags)
    texts = [b.get_text(separator=" ", strip=True) for b in blocks]
    return [t for t in texts if t]


def link_density(tag):
    text_length = len(tag.get_text(strip=True))
    if text_length == 0:
        return 1.0

    link_length = sum(len(a.get_text(strip=True)) for a in tag.find_all("a"))
    return link_length / text_length


def extract_paragraphs(html, max_link_density=None):
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")

    if max_link_density is not None:
        paragraphs = [p for p in paragraphs if link_density(p) <= max_link_density]

    return "\n".join(p.get_text(strip=True) for p in paragraphs)
