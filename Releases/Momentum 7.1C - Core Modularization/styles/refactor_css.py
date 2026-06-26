from pathlib import Path
import shutil
import textwrap
import py_compile

app_path = Path("app.py")
styles_dir = Path("styles")
theme_path = styles_dir / "theme.py"
init_path = styles_dir / "__init__.py"
backup_path = Path("app_before_css_refactor.py")

text = app_path.read_text(encoding="utf-8")

start = text.find('st.markdown("""\n<style>')
if start == -1:
    start = text.find('st.markdown("""\r\n<style>')

end_marker = '# st.title("Momentum v2.1")'
end = text.find(end_marker)

if start == -1 or end == -1 or end <= start:
    raise RuntimeError("Could not locate CSS block safely. No changes made.")

css_block = text[start:end].rstrip() + "\n"

shutil.copy2(app_path, backup_path)

styles_dir.mkdir(exist_ok=True)
init_path.touch()

theme_code = (
    "import streamlit as st\n\n\n"
    "def apply_theme():\n"
    + textwrap.indent(css_block, "    ")
    + "\n"
)

theme_path.write_text(theme_code, encoding="utf-8")

replacement = "from styles.theme import apply_theme\n\napply_theme()\n\n"
new_text = text[:start] + replacement + text[end:]

app_path.write_text(new_text, encoding="utf-8")

py_compile.compile("app.py", doraise=True)
py_compile.compile(str(theme_path), doraise=True)

print("CSS refactor complete.")
print("Backup created: app_before_css_refactor.py")
print("New file created: styles/theme.py")
