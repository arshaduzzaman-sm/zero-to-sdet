# Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/
"""Score your SDET skills self-assessment and see what to learn next.

Rate each skill in skills_self_assessment.csv from 0 to 3:
    0 = never done it    1 = done it with help
    2 = can do it alone  3 = can teach it

Then run:
    python score_skills.py skills_self_assessment.csv
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

LEVELS = {0: "never done it", 1: "with help", 2: "alone", 3: "can teach it"}
NEXT_COUNT = 3  # how many skills to suggest; more than three at once is too many


@dataclass(frozen=True)
class Skill:
    area: str
    name: str
    level: int


def read_skills(path: Path) -> list[Skill]:
    skills = []
    with path.open(newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                level = int(row["level"])
            except (TypeError, ValueError):
                raise ValueError(f"Line {line_number}: level must be 0, 1, 2 or 3") from None
            if level not in LEVELS:
                raise ValueError(f"Line {line_number}: level must be 0, 1, 2 or 3, not {level}")
            skills.append(Skill(row["area"].strip(), row["skill"].strip(), level))
    if not skills:
        raise ValueError("The file has no skills in it")
    return skills


def area_scores(skills: list[Skill]) -> dict[str, float]:
    """Each area's score from 0 to 100 percent, in the order the areas first appear."""
    levels: dict[str, list[int]] = defaultdict(list)
    for skill in skills:
        levels[skill.area].append(skill.level)
    return {area: 100 * sum(values) / (3 * len(values)) for area, values in levels.items()}


def learn_next(skills: list[Skill], count: int = NEXT_COUNT) -> list[Skill]:
    """The lowest-rated skills, keeping the file's order when levels are equal."""
    return sorted(skills, key=lambda skill: skill.level)[:count]


def report(skills: list[Skill]) -> str:
    lines = ["Your SDET skills", ""]
    for area, score in area_scores(skills).items():
        bar = "#" * round(score / 10)
        lines.append(f"{area:<16} {bar:<10} {score:3.0f}%")
    total = 100 * sum(skill.level for skill in skills) / (3 * len(skills))
    lines += ["", f"Overall: {total:.0f}%", "", "Learn next:"]
    for skill in learn_next(skills):
        lines.append(f"- {skill.name} ({skill.area}, now: {LEVELS[skill.level]})")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Usage: python score_skills.py skills_self_assessment.csv", file=sys.stderr)
        return 2
    try:
        print(report(read_skills(Path(argv[0]))))
    except (OSError, ValueError, KeyError) as error:
        print(f"Could not read the file: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
