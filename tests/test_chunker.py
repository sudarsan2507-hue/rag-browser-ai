import pytest
from retrieval.chunker import chunk_text, split_oversized, pack_sentences, raw_windows


def test_packs_small_paragraphs_together():
    text = "First para.\n\nSecond para.\n\nThird para."
    chunks = chunk_text(text, max_chars=100, overlap=10)
    assert chunks == ["First para.\n\nSecond para.\n\nThird para."]


def test_splits_when_paragraphs_exceed_max_chars():
    text = "A" * 40 + "\n\n" + "B" * 40
    chunks = chunk_text(text, max_chars=50, overlap=10)
    assert len(chunks) == 2
    assert chunks[0] == "A" * 40
    assert chunks[1] == "B" * 40


def test_oversized_paragraph_splits_on_sentence_boundaries():
    para = " ".join(f"Sentence {i} has some words." for i in range(10))
    chunks = chunk_text(para, max_chars=60, overlap=10)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c) <= 60
        assert c.rstrip().endswith(".")


def test_oversized_paragraph_with_no_punctuation_falls_back_to_raw_windows():
    para = "x" * 200
    chunks = split_oversized(para, max_chars=50, overlap=10)
    assert len(chunks) > 1
    assert all(len(c) <= 50 for c in chunks)
    # reconstructing without overlap should recover the original run of x's
    assert chunks[0][:40] == "x" * 40


def test_split_oversized_raises_when_overlap_not_smaller_than_max_chars():
    with pytest.raises(ValueError):
        split_oversized("some text", max_chars=10, overlap=10)

    with pytest.raises(ValueError):
        split_oversized("some text", max_chars=10, overlap=20)


def test_pack_sentences_respects_max_chars():
    sentences = ["Short one.", "Another short one.", "A third short sentence."]
    chunks = pack_sentences(sentences, max_chars=30)
    assert all(len(c) <= 30 or " " not in c for c in chunks)


def test_raw_windows_covers_full_text_with_overlap():
    text = "0123456789" * 3
    chunks = raw_windows(text, max_chars=10, overlap=3)
    assert chunks[0] == text[0:10]
    assert chunks[1] == text[7:17]


def test_chunk_text_empty_input_returns_empty_list():
    assert chunk_text("") == []
    assert chunk_text("   \n\n   ") == []
