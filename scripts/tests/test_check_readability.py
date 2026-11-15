"""Tests for scripts/check_readability.py: it must measure only what readers read."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_readability.py"
spec = importlib.util.spec_from_file_location("check_readability", SCRIPT)
check_readability = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_readability)

prose = check_readability.prose
grade = check_readability.grade
longest_sentences = check_readability.longest_sentences


def test_front_matter_is_skipped():
    page = '---\ntitle: "Secret words"\n---\n\nThe cat sat.\n'
    assert "Secret" not in prose(page)
    assert "The cat sat." in prose(page)


def test_code_blocks_are_skipped():
    page = "Run this.\n\n```python\nimport extraordinarily_complicated_module\n```\n"
    assert "extraordinarily" not in prose(page)


def test_indented_code_inside_tabs_is_skipped():
    page = '=== "Python"\n\n    ```python\n    print("hidden words")\n    ```\n\nShown.\n'
    assert "hidden" not in prose(page)


def test_headings_tables_html_and_comments_are_skipped():
    page = (
        "# Heading words\n\n| Table | Words |\n| --- | --- |\n\n"
        '<div class="card">HTML words</div>\n\n<!-- comment words -->\n\nKept.\n'
    )
    text = prose(page)
    for skipped in ("Heading", "Table", "HTML", "comment"):
        assert skipped not in text
    assert "Kept." in text


def test_links_keep_their_text_not_the_address():
    text = prose("Read [the glossary](../glossary.md#api-and-more) first.\n")
    assert "the glossary" in text
    assert "glossary.md" not in text


def test_wrapped_lines_are_one_sentence():
    text = prose("This sentence is wrapped\nover two lines.\n")
    assert len(check_readability.SENTENCE_END.findall(text)) == 1


def test_each_list_item_is_its_own_sentence():
    text = prose("- First item\n- Second item\n")
    assert len(check_readability.SENTENCE_END.findall(text)) == 2


def test_box_title_is_its_own_sentence():
    text = prose('!!! tip "A short title"\n    The body of the box.\n')
    assert "A short title." in text


def test_simple_text_scores_low():
    score, words = grade("The cat sat on the mat. The dog ran to the park. We had fun.")
    assert words == 15
    assert score < 3


def test_long_hard_text_scores_high():
    hard = (
        "Comprehensive infrastructure considerations necessitate sophisticated "
        "organizational coordination, particularly regarding interdependent "
        "architectural responsibilities and operational accountability."
    )
    score, _ = grade(hard)
    assert score > check_readability.MAX_GRADE


def test_longest_sentences_lists_only_long_ones_longest_first():
    short = "This is short."
    long_one = " ".join(["word"] * 30) + "."
    longer = " ".join(["word"] * 40) + "."
    found = longest_sentences(f"{short} {long_one} {longer}")
    assert [size for size, _ in found] == [40, 30]
