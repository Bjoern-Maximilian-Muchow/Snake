from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_level_two_scaffold_is_separate_from_reference_bot():
    scaffold = ROOT / "learning" / "level2" / "student_bot.py"
    reference = ROOT / "simulator" / "python" / "example_bots.py"

    assert scaffold.exists()
    assert reference.exists()
    assert scaffold.read_text(encoding="utf-8") != reference.read_text(encoding="utf-8")
    assert "def is_blocked" in scaffold.read_text(encoding="utf-8")
    assert "def safe_moves" in scaffold.read_text(encoding="utf-8")


def test_level_three_scaffold_exposes_student_entry_point():
    scaffold = (ROOT / "learning" / "level3" / "student_bot.h").read_text(encoding="utf-8")

    assert "chooseStudentMove" in scaffold
    assert "new " not in scaffold
    assert "malloc" not in scaffold


def test_web_simulator_contains_block_editor_and_learning_modes():
    html = (ROOT / "simulator" / "web" / "index.html").read_text(encoding="utf-8")

    assert 'data-mode="demo"' in html
    assert 'data-mode="assignment"' in html
    assert 'data-mode="challenge"' in html
    assert 'id="rule-list"' in html
    assert 'src="block_editor.js"' in html


def test_edrys_contains_python_and_cpp_editors():
    laboratory = (ROOT / "edrys" / "laboratory.yaml").read_text(encoding="utf-8")

    assert laboratory.count("module-monaco-editor") == 2
    assert "runCommand: autosnake-python" in laboratory
    assert "runCommand: autosnake-cpp" in laboratory
    assert laboratory.count("module-pyxtermjs") == 2
    assert "execute: autosnake-python" in laboratory
    assert "execute: autosnake-cpp" in laboratory
    assert "autosnake-run python $CODE" in laboratory
    assert "autosnake-run cpp $CODE --upload --port COM3" in laboratory


def test_edrys_separates_lobby_and_three_level_rooms():
    laboratory = (ROOT / "edrys" / "laboratory.yaml").read_text(encoding="utf-8")

    assert "?mode=demo&level=1" in laboratory
    assert "  defaultNumberOfRooms: 3" in laboratory
    assert "showInCustom: Lobby" in laboratory
    assert "showInCustom: Room 1" in laboratory
    assert "showInCustom: Room 2" in laboratory
    assert "showInCustom: Room 3" in laboratory
    assert "Das kannst du danach" in laboratory
