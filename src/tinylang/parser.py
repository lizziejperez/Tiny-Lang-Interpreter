from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tinylang.lexer import Lexer
from tinylang.token import Token, TokenKind
from tinylang.ast import (
    Program,
    Expr,
    Stmt,
    IntLiteral,
    Name,
    GroupingExpr,
    UnaryExpr,
    BinaryExpr,
    ExprStmt,
)


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

    This initial parser supports:
    - integer literals
    - identifier expressions
    - grouped expressions
    - expression statements
    """

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current: Token = self.lexer.next_token()
        self.previous: Optional[Token] = None

    # Token navigation utilities

    def peek(self) -> Token:
        """
        Return the current token without consuming it.
        """
        return self.current

    def at_end(self) -> bool:
        """
        True if the current token is EOF.
        """
        return self.current.kind == TokenKind.EOF

    def advance(self) -> Token:
        """
        Consume and return the current token, moving to the next token.
        """
        self.previous = self.current
        self.current = self.lexer.next_token()
        return self.previous

    def check_kind(self, kind: TokenKind) -> bool:
        """
        True if the current token matches kind (without consuming).
        """
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

    # Expression parsing

    def parse_primary(self) -> Expr:
        """
        Parse the most basic expressions:
        - integer literals
        - identifiers
        - parenthesized expressions
        """
        if self.match(TokenKind.INT):
            tok = self.previous
            assert tok is not None
            assert isinstance(tok.value, int)
            return IntLiteral(tok.value)

        if self.match(TokenKind.NAME):
            tok = self.previous
            assert tok is not None
            return Name(tok.src)

        if self.match(TokenKind.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenKind.RPAREN, "Expected ')' after expression")
            return GroupingExpr(expr)

        tok = self.current
        raise ParseError(
            message=f"Expected expression (found {tok.kind.name} {tok.src!r})",
            line=tok.line,
            col=tok.col,
        )

    def parse_unary(self) -> Expr:
        """
        Parse unary expressions.

        Supported unary operators:
        - !
        - -
        """
        if self.match(TokenKind.NOT, TokenKind.MINUS):
            tok = self.previous
            assert tok is not None
            right = self.parse_unary()
            return UnaryExpr(tok.src, right)

        return self.parse_primary()

    def parse_factor(self) -> Expr:
        """
        Parse multiplicative expressions.

        Supported operators:
        - *
        - /
        """
        expr = self.parse_unary()

        while self.match(TokenKind.STAR, TokenKind.SLASH):
            op_tok = self.previous
            assert op_tok is not None
            right = self.parse_unary()
            expr = BinaryExpr(expr, op_tok.src, right)

        return expr

    def parse_term(self) -> Expr:
        """
        Parse additive expressions.

        Supported operators:
        - +
        - -
        """
        expr = self.parse_factor()

        while self.match(TokenKind.PLUS, TokenKind.MINUS):
            op_tok = self.previous
            assert op_tok is not None
            right = self.parse_factor()
            expr = BinaryExpr(expr, op_tok.src, right)

        return expr

    def parse_comparison(self) -> Expr:
        """
        Parse comparison expressions.

        Supported operators:
        - <
        - <=
        - >
        - >=
        """
        expr = self.parse_term()

        while self.match(TokenKind.LT, TokenKind.LTE, TokenKind.GT, TokenKind.GTE):
            op_tok = self.previous
            assert op_tok is not None
            right = self.parse_term()
            expr = BinaryExpr(expr, op_tok.src, right)

        return expr

    def parse_equality(self) -> Expr:
        """
        Parse equality expressions.

        Supported operators:
        - ==
        - !=
        """
        expr = self.parse_comparison()

        while self.match(TokenKind.EQEQ, TokenKind.NEQ):
            op_tok = self.previous
            assert op_tok is not None
            right = self.parse_comparison()
            expr = BinaryExpr(expr, op_tok.src, right)

        return expr

    def parse_expression(self) -> Expr:
        """
        Parse a full expression using precedence rules.
        """
        return self.parse_equality()