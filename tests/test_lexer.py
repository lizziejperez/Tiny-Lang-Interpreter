from tinylang.lexer import Lexer
from tinylang.token import TokenKind

def test_skip_whitespace_only():
    lx = Lexer("   \n\t  ")
    tok = lx.next_token()

    assert tok.kind == TokenKind.EOF

def collect_tokens(source: str):
    lx = Lexer(source)
    tokens = []

    while True:
        tok = lx.next_token()
        tokens.append(tok.kind)
        if tok.kind == TokenKind.EOF:
            break

    return tokens

def test_arithmetic_operators():
    tokens = collect_tokens("+ - * /")

    assert tokens == [
        TokenKind.PLUS,
        TokenKind.MINUS,
        TokenKind.STAR,
        TokenKind.SLASH,
        TokenKind.EOF,
    ]

def test_parentheses_and_braces():
    tokens = collect_tokens("() {}")

    assert tokens == [
        TokenKind.LPAREN,
        TokenKind.RPAREN,
        TokenKind.LBRACE,
        TokenKind.RBRACE,
        TokenKind.EOF,
    ]

def test_comma_and_semicolon():
    tokens = collect_tokens(", ;")

    assert tokens == [
        TokenKind.COMMA,
        TokenKind.SEMICOLON,
        TokenKind.EOF,
    ]