from __future__ import annotations

from typing import List

from tinylang.lexer import Lexer
from tinylang.token import Token, TokenKind

# Helpers

def collect_kinds(source: str) -> list[TokenKind]:
    """Return a list of TokenKind values until EOF."""
    lx = Lexer(source)
    kinds: list[TokenKind] = []
    while True:
        tok = lx.next_token()
        kinds.append(tok.kind)
        if tok.kind == TokenKind.EOF:
            break
    return kinds

def collect_tokens(source: str) -> list[Token]:
    """Return a list of Token objects until EOF."""
    lx = Lexer(source)
    toks: list[Token] = []
    while True:
        tok = lx.next_token()
        toks.append(tok)
        if tok.kind == TokenKind.EOF:
            break
    return toks

# Tests

def test_skip_whitespace_only():
    kinds = collect_kinds("   \n\t  ")
    assert kinds == [TokenKind.EOF]

def test_arithmetic_operators():
    assert collect_kinds("+ - * /") == [
        TokenKind.PLUS,
        TokenKind.MINUS,
        TokenKind.STAR,
        TokenKind.SLASH,
        TokenKind.EOF,
    ]

def test_parentheses_and_braces():
    assert collect_kinds("() {}") == [
        TokenKind.LPAREN,
        TokenKind.RPAREN,
        TokenKind.LBRACE,
        TokenKind.RBRACE,
        TokenKind.EOF,
    ]

def test_comma_and_semicolon():
    assert collect_kinds(", ;") == [
        TokenKind.COMMA,
        TokenKind.SEMICOLON,
        TokenKind.EOF,
    ]

def test_single_char_operators():
    assert collect_kinds("= ! < >") == [
        TokenKind.EQUAL,
        TokenKind.NOT,
        TokenKind.LT,
        TokenKind.GT,
        TokenKind.EOF,
    ]

def test_multi_char_operators():
    assert collect_kinds("== != <= >=") == [
        TokenKind.EQEQ,
        TokenKind.NEQ,
        TokenKind.LTE,
        TokenKind.GTE,
        TokenKind.EOF,
    ]

def test_integer_literals():
    toks = collect_tokens("10 0 420")

    assert toks[0].kind == TokenKind.INT and toks[0].src == "10" and toks[0].value == 10
    assert toks[1].kind == TokenKind.INT and toks[1].src == "0" and toks[1].value == 0
    assert toks[2].kind == TokenKind.INT and toks[2].src == "420" and toks[2].value == 420
    assert toks[3].kind == TokenKind.EOF

def test_names_and_keywords():
    kinds = collect_kinds("let x conjure y whilst z")

    assert kinds == [
        TokenKind.LET,
        TokenKind.NAME,
        TokenKind.LET,     # conjure alias
        TokenKind.NAME,
        TokenKind.WHILE,   # whilst alias
        TokenKind.NAME,
        TokenKind.EOF,
    ]

def test_unrecognized_characters():
    toks = collect_tokens("@ # $ ? : ' \" \\")

    assert toks[0].kind == TokenKind.ILLEGAL and toks[0].src == "@"
    assert toks[1].kind == TokenKind.ILLEGAL and toks[1].src == "#"
    assert toks[2].kind == TokenKind.ILLEGAL and toks[2].src == "$"
    assert toks[3].kind == TokenKind.ILLEGAL and toks[3].src == "?"
    assert toks[4].kind == TokenKind.ILLEGAL and toks[4].src == ":"
    assert toks[5].kind == TokenKind.ILLEGAL and toks[5].src == "'"
    assert toks[6].kind == TokenKind.ILLEGAL and toks[6].src == "\""
    assert toks[7].kind == TokenKind.ILLEGAL and toks[7].src == "\\"
    assert toks[8].kind == TokenKind.EOF