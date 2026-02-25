from __future__ import annotations

from tinylang.token import Token, TokenKind


class Lexer:
    """
    Converts source text into a stream of Token objects.

    Note: This initial version only implements cursor tracking and returns EOF.
    Tokenization logic will be added incrementally.
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

    # Tokenization Function

    def next_token(self) -> Token:
        """
        Return the next token.
        Note: Currently only returns EOF.
        """
        return Token(TokenKind.EOF, "", self.line, self.col)