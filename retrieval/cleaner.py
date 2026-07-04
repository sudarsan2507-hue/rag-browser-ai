from bs4 import BeautifulSoup
from readability import Document


def extract_readability(html):
    summary_html = Document(html).summary()
    return BeautifulSoup(summary_html, "html.parser").get_text(separator=" ", strip=True)


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
