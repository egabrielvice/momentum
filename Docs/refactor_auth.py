from pathlib import Path
import shutil
import py_compile

app_path = Path("app.py")
utils_dir = Path("utils")
auth_path = utils_dir / "auth.py"
backup_path = Path("app_before_auth_refactor.py")

text = app_path.read_text(encoding="utf-8")

start = text.find("def require_password():")
end = text.find("from styles.theme import apply_theme")

if end == -1:
    end = text.find("apply_theme()")

if start == -1 or end == -1 or end <= start:
    raise RuntimeError("Could not locate authentication block safely. No changes made.")

auth_block = text[start:end].strip() + "\n"

shutil.copy2(app_path, backup_path)

utils_dir.mkdir(exist_ok=True)
(utils_dir / "__init__.py").touch()

auth_path.write_text(
    "import streamlit as st\n\n\n" + auth_block,
    encoding="utf-8"
)

new_text = text[:start] + "from utils.auth import require_password\n\n" + text[end:]
app_path.write_text(new_text, encoding="utf-8")

py_compile.compile("app.py", doraise=True)
py_compile.compile(str(auth_path), doraise=True)

print("Auth refactor complete.")
print("Backup created: app_before_auth_refactor.py")
print("New file created: utils/auth.py")
