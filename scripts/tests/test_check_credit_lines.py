"""Tests for scripts/check_credit_lines.py: the right comment style for each file type."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_credit_lines.py"
spec = importlib.util.spec_from_file_location("check_credit_lines", SCRIPT)
check_credit_lines = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_credit_lines)

TEXT = check_credit_lines.TEXT
credit_line = check_credit_lines.credit_line
has_credit = check_credit_lines.has_credit
add_credit = check_credit_lines.add_credit


def test_each_file_type_gets_its_own_comment_style():
    assert credit_line(Path("a.py")) == f"# {TEXT}"
    assert credit_line(Path("steps.feature")) == f"# {TEXT}"
    assert credit_line(Path("Dockerfile")) == f"# {TEXT}"
    assert credit_line(Path("load.js")) == f"// {TEXT}"
    assert credit_line(Path("check.sql")) == f"-- {TEXT}"
    assert credit_line(Path("plan.jmx")) == f"<!-- {TEXT} -->"


def test_file_types_without_comments_are_not_guessed():
    assert credit_line(Path("data.unknownext")) is None


def test_credit_on_the_first_line_passes():
    line = credit_line(Path("a.py"))
    assert has_credit(f"{line}\nimport os\n", line)


def test_credit_after_a_shebang_passes():
    line = credit_line(Path("run.sh"))
    assert has_credit(f"#!/usr/bin/env bash\n{line}\necho hi\n", line)


def test_missing_or_misplaced_credit_fails():
    line = credit_line(Path("a.py"))
    assert not has_credit("import os\n", line)
    assert not has_credit(f"import os\n{line}\n", line)
    assert not has_credit("", line)


def test_fix_adds_the_line_on_top():
    line = credit_line(Path("a.py"))
    fixed = add_credit("import os\n", line)
    assert fixed == f"{line}\nimport os\n"
    assert has_credit(fixed, line)


def test_fix_keeps_the_shebang_first():
    line = credit_line(Path("run.sh"))
    fixed = add_credit("#!/usr/bin/env bash\necho hi\n", line)
    assert fixed.splitlines()[0] == "#!/usr/bin/env bash"
    assert has_credit(fixed, line)
