from pathlib import Path
import shutil
import textwrap
import py_compile

app_path = Path("app.py")
utils_dir = Path("utils")
auth_path = utils_dir / "auth.py"
init_path = utils_dir / "__init__.py"
backup_path = Path("app_before_auth_refactor.py")

text = app_path.read_text(encoding="utf-8")

start = text.find("def require_password():")
end = text.find("from styles.theme import apply_theme")

if start == -1 or end == -1 or end <= start:
    raise RuntimeError("Could not locate authentication block safely. No changes made.")

auth_block = text[start:end].rstrip() + "\n"

shutil.copy2(app_path, backup_path)

utils_dir.mkdir(exist_ok=True)
init_path.touch()

auth_code = (
    "import streamlit as st\n\n\n"
    + auth_block
)

auth_path.write_text(auth_code, encoding="utf-8")

replacement = "from utils.auth import require_password\n"
new_text = text[:start] + replacement + text[end:]

app_path.write_text(new_text, encoding="utf-8")

py_compile.compile("app.py", doraise=True)
py_compile.compile(str(auth_path), doraise=True)

print("Auth refactor complete.")
print("Backup created: app_before_auth_refactor.py")
print("New file created: utils/auth.py")
