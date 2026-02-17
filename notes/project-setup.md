## Initialize Project Skeleton

### 1. Create the folder structure

Within your projects folder:
```
mkdir tiny-lang-interpreter
cd tiny-lang-interpreter
```

Now create folders:

```
mkdir -p src/tinylang
```

### 2. Create the required files

#### src/tinylang/__init__.py

Empty for now.

#### pyproject.toml

```toml
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
#### .gitignore

```
# Python bytecode / cache
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
env/

# Environment variables
.env

# Packaging / build artifacts
build/
dist/
*.egg-info/
pip-wheel-metadata/

# Testing / coverage
.coverage
htmlcov/
.pytest_cache/

# IDE / Editor settings
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
```
#### README.md

Give an overview of the project.

### 3. Set up the environment

From project root file:

```bash
python -m venv .venv
```

Activate it:

(Windows Command Promt)

```
.venv\Scripts\activate.bat
```

### 4. Install the Package locally

After activation, now run:

```
pip install -e ".[dev]"
```

Test it works in the activated env:

```
python -c "import tinylang; print('OK')"
```

If it prints OK → you’re correctly set up.

Deactivate env:

```
deactivate
```