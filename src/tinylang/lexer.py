from __future__ import annotations

from tinylang.token import Token, TokenKind, KEYWORDS


class Lexer:
    """
    Converts source text into a stream of Token objects.

    This lexer is implemented incrementally and currently supports:
    - Arithmetic and comparison operators (single- and multi-character)
    - Delimiters (parentheses, braces, comma, semicolon)
    - Integer literals
    - Identifiers and keyword resolution (via KEYWORDS map)
    - Line and column tracking for error reporting
    """

    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0          # index into source string
        self.line = 1         # 1-based line number
        self.col = 1          # 1-based column number

    # Cursor Helper Functions

    def current_char(self) -> str | None:
        """Return the current character, or None if at end of input."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def advance(self) -> None:
        """
        If at end of input, do nothing.
        Otherwise, move forward by one character and update line and column tracking.
        """
        ch = self.current_char()
        if ch is None:
            return

        if ch == "\n":
            self.pos += 1
            self.line += 1
            self.col = 1
        else:
            self.pos += 1
            self.col += 1
    
    def peek_char(self) -> str | None:
        """Return the next character without advancing, or None if at end."""
        next_pos = self.pos + 1
        if next_pos >= len(self.source):
            return None
        return self.source[next_pos]
    
    def skip_whitespace(self) -> None:
        """
        Advance past any whitespace characters.

        Note: Whitespace includes spaces, tabs, carriage returns, and newlines.
        Newlines are handled in `advance()` so line/col tracking stays correct.
        """
        while True:
            ch = self.current_char()
            if ch is None:
                return
            if ch in (" ", "\t", "\r", "\n"):
                self.advance()
                continue
            return
    
    def read_number(self) -> str:
        """
        Read consecutive digits and return the full number lexeme.

        Leaves the cursor positioned at the first non-digit character.
        """
        start = self.pos

        while True:
            ch = self.current_char()
            if (ch is None) or (not ch.isdigit()):
                break
            self.advance()

        return self.source[start:self.pos]
    
    def read_name(self) -> str:
        """
        Read an identifier-like sequence:
        starts with a letter or underscore, then letters/digits/underscore.
        """
        start = self.pos

        while True:
            ch = self.current_char()
            if ch is None:
                break
            if ch.isalnum() or ch == "_":
                self.advance()
                continue
            break

        return self.source[start:self.pos]

    # Tokenization Function

    def next_token(self) -> Token:
        """
        Return the next token from the input stream.

        Currently supports:
        - Arithmetic and comparison operators
        - Delimiters
        - Integer literals
        - Identifiers (resolved to keywords if present in KEYWORDS)
        """
        self.skip_whitespace()

        ch = self.current_char()

        # Handle end of input, return EOF
        if ch is None:
            return Token(TokenKind.EOF, "", self.line, self.col)

        # Capture token start position before consuming characters
        tok_line = self.line
        tok_col = self.col

        # Multi-character operators (must be checked before single-character versions)
        
        nxt = self.peek_char()

        if ch == "=" and nxt == "=":
            self.advance()
            self.advance()
            return Token(TokenKind.EQEQ, "==", tok_line, tok_col)

        if ch == "!" and nxt == "=":
            self.advance()
            self.advance()
            return Token(TokenKind.NEQ, "!=", tok_line, tok_col)

        if ch == "<" and nxt == "=":
            self.advance()
            self.advance()
            return Token(TokenKind.LTE, "<=", tok_line, tok_col)

        if ch == ">" and nxt == "=":
            self.advance()
            self.advance()
            return Token(TokenKind.GTE, ">=", tok_line, tok_col)
        
        # Single-character operators

        if ch == "=":
            self.advance()
            return Token(TokenKind.EQUAL, "=", tok_line, tok_col)

        if ch == "!":
            self.advance()
            return Token(TokenKind.NOT, "!", tok_line, tok_col)

        if ch == "<":
            self.advance()
            return Token(TokenKind.LT, "<", tok_line, tok_col)

        if ch == ">":
            self.advance()
            return Token(TokenKind.GT, ">", tok_line, tok_col)
        
        if ch == "+":
            self.advance()
            return Token(TokenKind.PLUS, "+", tok_line, tok_col)

        if ch == "-":
            self.advance()
            return Token(TokenKind.MINUS, "-", tok_line, tok_col)

        if ch == "*":
            self.advance()
            return Token(TokenKind.STAR, "*", tok_line, tok_col)

        if ch == "/":
            self.advance()
            return Token(TokenKind.SLASH, "/", tok_line, tok_col)

        # Integer literals
        if ch.isdigit():
            lex = self.read_number()
            return Token(TokenKind.INT, lex, tok_line, tok_col, value=int(lex))
        
        # Identifiers and keywords:
        # - Must start with a letter or underscore
        # - May contain letters, digits, or underscores
        # - Resolved to keyword if present in KEYWORDS
        if ch.isalpha() or ch == "_":
            lex = self.read_name()
            kind = KEYWORDS.get(lex, TokenKind.NAME)
            return Token(kind, lex, tok_line, tok_col)

        # Delimiters

        if ch == "(":
            self.advance()
            return Token(TokenKind.LPAREN, "(", tok_line, tok_col)

        if ch == ")":
            self.advance()
            return Token(TokenKind.RPAREN, ")", tok_line, tok_col)

        if ch == "{":
            self.advance()
            return Token(TokenKind.LBRACE, "{", tok_line, tok_col)

        if ch == "}":
            self.advance()
            return Token(TokenKind.RBRACE, "}", tok_line, tok_col)
        
        if ch == ",":
            self.advance()
            return Token(TokenKind.COMMA, ",", tok_line, tok_col)

        if ch == ";":
            self.advance()
            return Token(TokenKind.SEMICOLON, ";", tok_line, tok_col)
            
        # Temporary fallback: unhandled characters currently return EOF
        return Token(TokenKind.EOF, "", tok_line, tok_col)