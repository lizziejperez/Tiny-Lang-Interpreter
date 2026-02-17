# Project Setup (Tiny-Lang)

## Goal

Initialize a clean, professional Python project structure for building a tiny interpreter.

The goal of this step was not to write language logic yet, but to:
- Create a proper package layout
- Set up an isolated Python environment
- Prepare for modular development (lexer, parser, interpreter)
- Ensure the project is installable and runnable

---

## 1. Repository Initialization

Created a new GitHub repository for Tiny-Lang.

Local project structure:

```
Tiny-Lang-Interpreter/
├── notes/
├── src/
│ └── tinylang/
│      └── __init__.py
├── pyproject.toml
├── README.md
├── .gitignore
```
### Why use `src/` layout?

Using a `src/` directory prevents accidental imports from the project root during development.

This ensures imports behave the same way they would after installation.

Example import:

```python
from tinylang.token import Token
```

This only works properly when the package is installed or run correctly, which is intentional.

## 2. Create the Folder Structure

From your projects directory:
```bash
mkdir Tiny-Lang-Interpreter
cd Tiny-Lang-Interpreter
mkdir -p src/tinylang
```

Created:
```bash
src/tinylang/__init__.py
```

The `__init__.py` file is empty for now and marks `tinylang` as a Python package.

## 3. Create `pyproject.toml`

Defined project metadata in `pyproject.toml` and prepared the project for editable installation:

```
[project]
name = "tinylang"
version = "0.1.0"
description = "A tiny programming language interpreter built in Python."
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]

[tool.pytest.ini_options]
pythonpath = ["src"]
```

## 4. Configure .gitignore

Used a minimal but sufficient configuration:

```
# Virtual environment
.venv/

# Python cache
__pycache__/
*.pyc

# Packaging artifacts
*.egg-info/
build/
dist/
```

This prevents committing:

- virtual environment files
- Python bytecode
- packaging/build artifacts

## 5. Set Up the Virtual Environment

Created a virtual environment to isolate dependencies.

From the project root:
```bash
python -m venv .venv
```

Activate (Windows Command Prompt):
```bash
.venv\Scripts\activate.bat
```

## 6. Install the Project Locally (Editable Mode)

After activating the environment:
```
pip install -e .
```

This allows changes in `src/tinylang` to be reflected immediately without reinstalling the package.

If using development dependencies:
```
pip install -e ".[dev]"
```

Test that installation works:
```
python -c "import tinylang; print('OK')"
```

If it prints `OK`, the package is correctly installed.

Deactivate when finished:
```
deactivate
```

## 7. README Setup

Documented:

- How to create the virtual environment
- How to activate it
- How to install the project
- How to deactivate the environment

This ensures anyone can clone and run the project easily.

## Result of Setup Phase

At the end of this step, Tiny-Lang had:

- Proper package structure
- Isolated Python environment
- Clean Git history
- Installation configuration
- Documentation for reproducibility

No interpreter logic yet — only infrastructure.