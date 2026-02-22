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

### Stage 3: Lexer (Ongoing)

- Character scanning utilities (`advance`, `peek`)
- Whitespace handling
- Token generation
- Support for:
    - Operators
    - Delimiters
    - Integers
    - Identifiers & keywords
- Error handling for illegal characters

### Stage 4: Parser (Planned)

- AST node definitions
- Expression parsing
-Statement parsing
- Function definitions and control flow

### Stage 5: Interpreter

- AST evaluation
- Environment/scope handling
- Function execution
- Control flow execution

### Stage 6: Error Handling & Polish

- Improved error messages
- Better diagnostics using line/column tracking
- Cleanup and refactoring

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