from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tinylang.lexer import Lexer
from tinylang.token import Token, TokenKind


@dataclass(frozen=True) # immutable error data (message + source position)
class ParseError(Exception):
    """
    Parser error that includes source position for meaningful messages.
    """
    message: str
    line: int
    col: int

    def __str__(self) -> str:
        return f"[line {self.line}, col {self.col}] {self.message}"


class Parser:
    """
    Consumes tokens and builds an AST (Abstract Syntax Tree).

    This initial version focuses on token navigation utilities.
    """

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current: Token = self.lexer.next_token()
        self.previous: Optional[Token] = None

    # Token navigation utilities

    def peek(self) -> Token:
        """Return the current token without consuming it."""
        return self.current

    def at_end(self) -> bool:
        """True if the current token is EOF."""
        return self.current.kind == TokenKind.EOF

    def advance(self) -> Token:
        """
        Consume and return the current token, moving to the next token.
        """
        self.previous = self.current
        self.current = self.lexer.next_token()
        return self.previous

    def check_kind(self, kind: TokenKind) -> bool:
        """True if the current token matches kind (without consuming)."""
        return self.current.kind == kind

    def match(self, *kinds: TokenKind) -> bool:
        """
        If current token is any of the provided kinds, consume it and return True.
        Otherwise return False.
        """
        for kind in kinds:
            if self.check_kind(kind):
                self.advance()
                return True
        return False

    def expect(self, kind: TokenKind, message: str) -> Token:
        """
        Consume the expected token kind or raise ParseError.
        """
        if self.check_kind(kind):
            return self.advance()

        tok = self.current
        raise ParseError(
            message=f"{message} (found {tok.kind.name} {tok.src!r})",
            line=tok.line,
            col=tok.col,
        )

    # Entry point (placeholder)
    def parse(self):
        """
        Parse a full program.

        Placeholder: returns an empty list for now.
        Next step will return a Program AST node.
        """
        return []