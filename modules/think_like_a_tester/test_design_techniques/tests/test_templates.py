# Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/
"""The templates of "Test design techniques" work, and the lessons' claims stay true."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

TOPIC = Path(__file__).resolve().parents[1]
TEMPLATES = TOPIC / "templates"
EXAMPLES = TOPIC / "examples"
CREDIT = "Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/"


def run(*args, cwd=EXAMPLES):
    return subprocess.run(
        [sys.executable, *args], cwd=cwd, capture_output=True, text=True, check=False
    )


def pytest_in(folder, *args):
    return run("-m", "pytest", "-q", "-p", "no:cacheprovider", *args, cwd=folder)


@pytest.mark.parametrize(
    "path",
    sorted(p for p in [*TEMPLATES.iterdir(), *EXAMPLES.rglob("*")] if p.suffix in {".py", ".md"}),
    ids=lambda p: p.name,
)
def test_every_file_starts_with_the_credit_line(path):
    assert CREDIT in path.read_text(encoding="utf-8").splitlines()[0]


def test_the_example_uses_the_boundaries_template_unchanged():
    assert (EXAMPLES / "boundaries.py").read_text() == (TEMPLATES / "boundaries.py").read_text()


def test_the_example_suite_passes():
    result = pytest_in(EXAMPLES)
    assert result.returncode == 0, result.stdout
    assert "49 passed" in result.stdout


def test_boundaries_lists_both_sides_of_each_edge():
    result = run(str(TEMPLATES / "boundaries.py"), "18", "120")
    assert result.returncode == 0
    lines = [line.split() for line in result.stdout.splitlines()[1:]]
    assert lines == [["17", "outside"], ["18", "inside"], ["120", "inside"], ["121", "outside"]]


def test_boundaries_three_adds_the_values_just_inside():
    sys.path.insert(0, str(TEMPLATES))
    try:
        from boundaries import boundary_values
    finally:
        sys.path.pop(0)
    assert [v for v, _ in boundary_values(3, 20, three=True)] == [2, 3, 4, 19, 20, 21]
    assert [v for v, _ in boundary_values(5, 6, three=True)] == [4, 5, 6, 7]
    with pytest.raises(ValueError, match="must not be bigger"):
        boundary_values(10, 1)


def test_boundaries_without_numbers_shows_usage():
    result = run(str(TEMPLATES / "boundaries.py"))
    assert result.returncode == 2
    assert "Usage" in result.stdout


def test_decision_table_prints_every_combination():
    result = run(str(TEMPLATES / "decision_table.py"), "Member", "Order $50 or more", "Express")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert lines[0] == "| # | Member | Order $50 or more | Express | Result |"
    assert len(lines) == 2 + 8
    assert lines[2] == "| 1 | Yes | Yes | Yes |  |"
    assert lines[-1] == "| 8 | No | No | No |  |"


def test_decision_table_warns_when_it_gets_too_big():
    result = run(str(TEMPLATES / "decision_table.py"), *[f"C{n}" for n in range(7)])
    assert "Warning: 128 rows" in result.stdout


@pytest.mark.parametrize(
    ("file", "old", "new", "caught_by", "missed_by"),
    [
        # Boundary values catch an off-by-one that equivalence partitioning misses.
        (
            "shop/signup.py",
            "if not MIN_AGE <= age <= MAX_AGE:",
            "if not MIN_AGE < age <= MAX_AGE:",
            "tests/test_signup_edges.py",
            "tests/test_signup_groups.py",
        ),
        # The decision table catches a forgotten condition.
        (
            "shop/delivery.py",
            "if member or subtotal_cents >= FREE_FROM:",
            "if subtotal_cents >= FREE_FROM:",
            "tests/test_delivery_table.py",
            None,
        ),
        # The state tests catch a move the rules don't allow.
        (
            "shop/order_status.py",
            '    ("shipped", "deliver"): "delivered",\n',
            '    ("shipped", "deliver"): "delivered",\n    ("shipped", "cancel"): "refunded",\n',
            "tests/test_order_states.py",
            None,
        ),
    ],
    ids=["off-by-one age", "forgotten member rule", "cancel after shipping"],
)
def test_the_tests_catch_the_bugs_shown_in_the_lessons(
    tmp_path, file, old, new, caught_by, missed_by
):
    copy = tmp_path / "examples"
    shutil.copytree(EXAMPLES, copy, ignore=shutil.ignore_patterns("__pycache__"))
    code = (copy / file).read_text()
    assert old in code
    (copy / file).write_text(code.replace(old, new))
    caught = pytest_in(copy, caught_by)
    assert caught.returncode == 1, caught.stdout
    assert "1 failed" in caught.stdout
    if missed_by:
        assert pytest_in(copy, missed_by).returncode == 0


@pytest.mark.parametrize(
    ("name", "sections"),
    [
        ("partitions_and_boundaries_worksheet.md", ["## Groups", "## Edges", "## Questions"]),
        ("decision_table_worksheet.md", ["## The table", "## Check the table"]),
        ("state_transition_worksheet.md", ["## The state table", "## Tests to write"]),
    ],
)
def test_worksheets_have_their_sections(name, sections):
    text = (TEMPLATES / name).read_text(encoding="utf-8")
    for section in sections:
        assert section in text
