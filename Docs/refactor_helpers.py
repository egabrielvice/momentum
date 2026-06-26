from pathlib import Path
import shutil
import py_compile

app_path = Path("app.py")
utils_dir = Path("utils")
helpers_path = utils_dir / "helpers.py"
backup_path = Path("app_before_helpers_refactor.py")

text = app_path.read_text(encoding="utf-8")

start = text.find("def total_reps(reps):")
end = text.find("week = current_week()")

if start == -1 or end == -1 or end <= start:
    raise RuntimeError("Could not locate helper functions safely. No changes made.")

helpers_block = text[start:end].strip() + "\n"

shutil.copy2(app_path, backup_path)

utils_dir.mkdir(exist_ok=True)
(utils_dir / "__init__.py").touch()

helpers_path.write_text(
    "import streamlit as st\n"
    "import streamlit.components.v1 as components\n"
    "from datetime import date, datetime\n"
    "from database import *\n\n\n"
    + helpers_block,
    encoding="utf-8"
)

new_text = text[:start] + "from utils.helpers import *\n\n" + text[end:]
app_path.write_text(new_text, encoding="utf-8")

py_compile.compile("app.py", doraise=True)
py_compile.compile(str(helpers_path), doraise=True)

print("Helpers refactor complete.")
print("Backup created: app_before_helpers_refactor.py")
print("New file created: utils/helpers.py")
