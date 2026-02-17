# Tiny-Lang-Interpreter

A tiny programming language interpreter built from scratch in Python.

With:

- literals: numbers, strings, booleans, null
- `let` variables
- expressions: `+ - * /`, comparisons
- `if/else`

## Goal

Build this project incrementally:

- Lexer (tokenizer)
- Parser (AST generation)
- Interpreter (evaluation engine)

## Development Setup

### 1. Clone the Repository

```
git clone https://github.com/lizziejperez/tiny-lang-interpreter.git
cd tiny-lang-interpreter
```

### 2. Create a Virtual Environment

Within the local repo directory:

```
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows

(PowerShell)

```
.venv\Scripts\Activate.ps1
```

If PowerShell blocks scripts, use Command Prompt instead.

(Command Prompt)

```
.venv\Scripts\activate.bat
```

#### macOS / Linux

```
source .venv/bin/activate
```

#### Verify

When activated, your terminal should show:

```
(.venv)
```

### 4. Install the Package (Editable Mode)
```
pip install -e ".[dev]"
```

This installs:
- The tinylang package
- Development dependencies (e.g., pytest)

### 5. Verify Installation
```
python -c "import tinylang; print('TinyLang ready')"
```

If you see:
```
TinyLang ready
```

The environment is set up correctly.

### Deactivating the Virtual Environment

To exit the virtual environment:
```
deactivate
```

Your terminal will no longer show (.venv).