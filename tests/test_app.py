
from pathlib import Path
import ast


def test_app_file_exists():
    assert Path("app.py").exists()


def test_app_code_is_valid():
    code = Path("app.py").read_text(encoding="utf-8")
    ast.parse(code)


def test_project_files_exist():
    assert Path("templates/index.html").exists()
    assert Path("static/style.css").exists()
    assert Path("requirements.txt").exists()

