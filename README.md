# Tiny-Lang-Interpreter

A tiny programming language interpreter built from scratch in Python.

With:

- literals: numbers, strings, booleans, null
- `let` variables
- expressions: `+ - * /`, comparisons
- `if/else`
- unique fantasy name aliases

## Goal

Build this project incrementally:

- Lexer (tokenizer)
- Parser (AST generation)
- Interpreter (evaluation engine)

## Development Stages

Tiny-Lang is being built incrementally in clearly defined phases:

### Stage 1: Project Setup

- Structured `src/`-based package layout
- Virtual environment configuration
- Editable installation via `pip install -e` .
- Clean `.gitignore`
- Setup documentation

### Stage 2: Token System

- `TokenKind` enum definition
- Keyword mapping (including fantasy aliases)
- `Token` data model
- Line/column tracking for error reporting

### Stage 3: Lexer

- Character scanning utilities (`advance`, `peek`)
- Whitespace handling
- Token generation
- Support for:
    - Operators
    - Delimiters
    - Integers
    - Identifiers & keywords
- Error handling for illegal characters

### Stage 4: Parser (Ongoing)

- AST node definitions
- Expression parsing
- Statement parsing
- Function definitions and control flow

### Stage 5: Interpreter (Planned)

- AST evaluation
- Environment/scope handling
- Function execution
- Control flow execution

### Stage 6: Error Handling & Polish

- Improved error messages
- Better diagnostics using line/column tracking
- Cleanup and refactoring

## Notes & Design Documentation

Detailed notes for each stage of development can be found in the `notes/` directory.

These documents explain design decisions, implementation steps, and how each component was built.

* [Project Setup](notes/project-setup.md)
* [Token System](notes/token-system.md)
* [Lexer](notes/lexer.md)
* [Parser](notes/parser.md)

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/lizziejperez/tiny-lang-interpreter.git
cd tiny-lang-interpreter
```

### 2. Create a Virtual Environment

Within the local repo directory:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows

(PowerShell)

```bash
.venv\Scripts\Activate.ps1
```

If PowerShell blocks scripts, use Command Prompt instead.

(Command Prompt)

```bash
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Verify

When activated, your terminal should show: `(.venv)`

### 4. Install the Package (Editable Mode)
```bash
pip install -e ".[dev]"
```

This installs:
- The tinylang package
- Development dependencies (e.g., pytest)

### 5. Verify Installation
```bash
python -c "import tinylang; print('TinyLang ready')"
```

If you see `TinyLang ready`, the environment is set up correctly.

### 6. Run the Test Suite

Tiny-Lang uses pytest for automated testing.

From the project root directory, run:
```bash
pytest
```
You should see output similar to:
```
============================= test session starts =============================
collected X items

tests/test_lexer.py ..... 
tests/test_parser.py ....

============================== X passed in 0.XXs ==============================
```
If all tests pass, the project is installed and working correctly.

#### Run a Specific Test File
```bash
pytest tests/test_lexer.py
```

#### Run a Specific Test Function
```bash
pytest tests/test_lexer.py::test_integer_literals
```

### Deactivating the Virtual Environment

To exit the virtual environment:
```bash
deactivate
```

Your terminal will no longer show `(.venv)`.