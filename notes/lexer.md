# 03 - Lexer (`lexer.py`)

## Goal

Implement a lexer that converts raw source code text into a stream of `Token` objects.

The lexer is responsible for:

- Scanning characters left-to-right
- Grouping characters into lexemes
- Producing `Token` objects with:
  - `TokenKind`
  - `src` (exact source substring)
  - `line` and `col`
  - Optional parsed `value`
- Handling whitespace
- Detecting illegal characters

## Design Approach

The lexer was implemented incrementally:

1. Track line and column positions
2. Build cursor utilities (`current_char`, `peek_char`, `advance`)
3. Implement whitespace skipping
4. Handle operators and delimiters
5. Add multi-character operator handling
6. Implement number scanning
7. Implement identifier/keyword scanning
8. Add illegal character handling

## 1. Cursor Tracking

The lexer maintains:

```python
self.source  # full source string
self.pos     # current index in source
self.line    # 1-based line number
self.col     # 1-based column number
```

`advance()`

Moves the cursor forward by one character.

- If the character is `\n`, increment line and reset `col` to `1`
- Otherwise increment `col`

This ensures precise error reporting later.

## 2. Skipping Whitespace

Implemented `skip_whitespace()` to ignore:

- Spaces
- Tabs
- Carriage returns (`\r`)
- Newlines (`\n`)

Including `\r` ensures compatibility with Windows-style line endings (`\r\n`).

Whitespace does not produce tokens.

## 3. Single-Character Tokens

Handled directly inside `next_token()`:

Examples:

- `+` → `TokenKind.PLUS`
- `-` → `TokenKind.MINUS`
- `(` → `TokenKind.LPAREN`
- `{` → `TokenKind.LBRACE`
- `;` → `TokenKind.SEMICOLON`

Each consumes one character and returns a token immediately.

## 4. Multi-Character Operators

Handled before single-character operators to avoid premature matching.

Examples:

- `==`
- `!=`
- `<=`
- `>=`

These use `peek_char()` to inspect the next character before deciding.

Order matters:

- Check `==` before `=`
- Check `!=` before `!`

## 5. Integer Literals

When a digit is encountered:

```python
if ch.isdigit():
    lex = self.read_number()
```
`read_number()`:

- Advances while characters are digits
- Returns the full digit sequence

Example:

Input: `10`

Produces:
```
TokenKind.INT
src="10"
value=10
```
The lexer groups multiple digits into a single token.

## 6. Identifiers and Keywords

When encountering a letter or `_`:

```python
if ch.isalpha() or ch == "_":
```

The lexer calls `read_name()`:

- Consumes letters, digits, and underscores
- Returns the full identifier string

Then:

```python
kind = KEYWORDS.get(lex, TokenKind.NAME)
```

If the lexeme matches a reserved word (including fantasy aliases), it becomes that keyword token.

Otherwise it remains TokenKind.NAME.

Example:`conjure` becomes `TokenKind.LET`

## 7. Illegal Characters

If a character does not match any known token pattern:

```python
self.advance()
return Token(TokenKind.ILLEGAL, ch, line, col)
```

The lexer:

- Produces an ILLEGAL token
- Advances the cursor to avoid infinite loops

This allows the parser to report meaningful syntax errors later.

## Example

Source:

```
conjure x = 10;
```

Produces tokens:

- `LET("conjure")`
- `NAME("x")`
- `EQUAL("=")`
- `INT("10") with value=10`
- `SEMICOLON(";")`
- `EOF`

## Result of Lexer Stage

At the end of Stage 3, Tiny-Lang can:

- Tokenize single- and multi-character operators
- Tokenize delimiters
- Tokenize integer literals
- Tokenize identifiers and keywords
- Support fantasy keyword aliases
- Track line and column positions
- Detect illegal characters
- Produce a complete token stream suitable for parsing

The lexer is now structurally complete for parsing expressions and statements.