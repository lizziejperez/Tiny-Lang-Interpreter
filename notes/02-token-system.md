# 02 - Token System (`token.py`)

## Goal

Create the token definitions for Tiny-Lang so the lexer can convert source code text into a stream of tokens that the parser can understand.

This file defines:
- `TokenKind` (an `Enum`) to represent token categories
- `KEYWORDS` mapping to convert specific words into keyword tokens (including aliases)
- `Token` class to store token data produced by the lexer

## What I Added

### 1. TokenKind Enum

I created a `TokenKind(Enum)` using `auto()` so each token type gets a unique value automatically.

Token categories included:
- Special: `END`, `ILLEGAL`
- Literals: `INT`, `NAME`
- Keywords: `LET`, `FUNC`, `RETURN`, `IF`, `ELSE`, `WHILE`, `PRINT`
- Operators: `PLUS`, `MINUS`, `STAR`, `SLASH`, `EQUAL`, `EQEQ`, `NOT`, `NEQ`, `LT`, `LTE`, `GT`, `GTE`
- Delimiters: `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`, `COMMA`, `SEMICOLON`

**Why `auto()`?**

The numeric values don’t matter—what matters is comparing types like:

```py
if token.kind == TokenKind.INT:
    ...
```

### 2. KEYWORDS Map (with aliases)

I added a KEYWORDS dictionary that maps strings to keyword token types.

The lexer will scan a name (like `mana`) as `NAME`, but if the text matches a keyword in this map, it becomes the matching keyword token type instead.

This also supports a “fantasy dialect” using aliases:

`conjure` → `LET`

`ritual` → `FUNC`

`bestow` → `RETURN`

`upon` → `IF`

`lest` → `ELSE`

`whilst` → `WHILE`

This means both standard and fantasy syntax can exist at the same time, without changing the parser.

### 3. Token Class

I implemented a `Token` class with a manual constructor so I fully understand what is stored per token.

Each token stores:

`kind`: the TokenKind

`src`: exact substring from source code (lexeme)

`line` / `col`: 1-based starting position (for error messages)

`value`: optional parsed value (ex: `int(src)` for integers)

**Example: What This Enables**

Given source:

```txt
conjure x = 10;
```

The lexer (later) should produce tokens like:

- `LET('conjure')`
- `NAME('x')`
- `EQUAL('=')`
- `INT('10') value=10`
- `SEMICOLON(';')`
- `EOF`

## Running Token Tests

This section describes how to run the token system tests (`test_token.py`).

From the project root:

```bash
pytest
```

You should see output similar to:

```
5 passed
```

If all tests pass, the token system is functioning as expected.