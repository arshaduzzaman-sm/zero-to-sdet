# Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/
"""The skills self-assessment and its scoring script work as the lesson says."""

import csv
import importlib.util
import sys
from pathlib import Path

import pytest

TOPIC = Path(__file__).resolve().parents[1]
TEMPLATE = TOPIC / "templates" / "skills_self_assessment.csv"
EXAMPLE = TOPIC / "examples" / "arshad_skills.csv"

SCRIPT = TOPIC / "templates" / "score_skills.py"
spec = importlib.util.spec_from_file_location("score_skills", SCRIPT)
score_skills = importlib.util.module_from_spec(spec)
sys.modules["score_skills"] = score_skills  # dataclasses need the module registered
spec.loader.exec_module(score_skills)


def write_csv(path: Path, rows: list[tuple[str, str, str]]) -> Path:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["area", "skill", "level"])
        writer.writerows(rows)
    return path


def test_template_starts_at_zero_for_every_skill():
    skills = score_skills.read_skills(TEMPLATE)
    assert len(skills) >= 10
    assert {skill.level for skill in skills} == {0}


def test_example_rates_the_same_skills_as_the_template():
    template = [(s.area, s.name) for s in score_skills.read_skills(TEMPLATE)]
    example = [(s.area, s.name) for s in score_skills.read_skills(EXAMPLE)]
    assert example == template


def test_area_score_is_a_percent_of_the_top_level(tmp_path):
    path = write_csv(tmp_path / "s.csv", [("API", "a", "3"), ("API", "b", "0"), ("UI", "c", "2")])
    scores = score_skills.area_scores(score_skills.read_skills(path))
    assert scores == pytest.approx({"API": 50.0, "UI": 66.67}, abs=0.01)


def test_learn_next_picks_the_three_lowest_in_file_order(tmp_path):
    rows = [("X", "a", "2"), ("X", "b", "0"), ("X", "c", "1"), ("X", "d", "0"), ("X", "e", "3")]
    skills = score_skills.read_skills(write_csv(tmp_path / "s.csv", rows))
    assert [skill.name for skill in score_skills.learn_next(skills)] == ["b", "d", "c"]


@pytest.mark.parametrize("bad_level", ["4", "-1", "two", ""])
def test_a_bad_level_names_the_line(tmp_path, bad_level):
    path = write_csv(tmp_path / "s.csv", [("X", "a", "1"), ("X", "b", bad_level)])
    with pytest.raises(ValueError, match="Line 3"):
        score_skills.read_skills(path)


def test_main_prints_the_report_for_the_example(capsys):
    assert score_skills.main([str(EXAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "Overall: 33%" in out
    assert "- Use pytest to write and run tests (Python, now: never done it)" in out


def test_main_without_a_file_shows_how_to_use_it(capsys):
    assert score_skills.main([]) == 2
    assert "Usage:" in capsys.readouterr().err


def test_main_with_a_missing_file_fails_clearly(tmp_path, capsys):
    assert score_skills.main([str(tmp_path / "nope.csv")]) == 1
    assert "Could not read the file" in capsys.readouterr().err
