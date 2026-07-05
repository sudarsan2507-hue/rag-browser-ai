from bs4 import BeautifulSoup
from retrieval.cleaner import extract_readability, link_density, extract_paragraphs


def test_extract_readability_uses_semantic_block_tags():
    html = "<html><body><article><h1>Title</h1><p>First paragraph.</p><p>Second paragraph.</p></article></body></html>"
    result = extract_readability(html)
    assert result == "Title\n\nFirst paragraph.\n\nSecond paragraph."


def test_extract_readability_falls_back_to_leaf_containers():
    html = """
    <html><body>
    <div><div>Some intro text about the topic.</div></div>
    <div>A second block of content here.</div>
    </body></html>
    """
    result = extract_readability(html)
    assert "Some intro text about the topic." in result
    assert "A second block of content here." in result
    # nested div shouldn't duplicate the inner text at both levels
    assert result.count("Some intro text about the topic.") == 1


def test_extract_readability_flat_fallback_warns(capsys):
    html = "<html><body><span>just a span</span> and <b>bold text</b> with no blocks</body></html>"
    result = extract_readability(html)
    captured = capsys.readouterr()
    assert "Warning" in captured.out
    assert "just a span" in result


def test_link_density_no_links():
    soup = BeautifulSoup("<p>Plain prose with no links at all.</p>", "html.parser")
    p = soup.find("p")
    assert link_density(p) == 0.0


def test_link_density_all_links():
    soup = BeautifulSoup("<p><a href='#'>Home</a><a href='#'>About</a></p>", "html.parser")
    p = soup.find("p")
    assert link_density(p) == 1.0


def test_link_density_empty_tag_is_treated_as_max_density():
    soup = BeautifulSoup("<p></p>", "html.parser")
    p = soup.find("p")
    assert link_density(p) == 1.0


def test_extract_paragraphs_filters_by_link_density():
    html = """
    <p>Real article prose about the subject matter here.</p>
    <p><a href='#'>Home</a><a href='#'>About</a><a href='#'>Contact</a></p>
    """
    filtered = extract_paragraphs(html, max_link_density=0.5)
    assert "Real article prose" in filtered
    assert "Home" not in filtered
