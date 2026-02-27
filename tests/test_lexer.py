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

def test_single_char_operators():
    tokens = collect_tokens("= ! < >")

    assert tokens == [
        TokenKind.EQUAL,
        TokenKind.NOT,
        TokenKind.LT,
        TokenKind.GT,
        TokenKind.EOF,
    ]

def test_multi_char_operators():
    tokens = collect_tokens("== != <= >=")

    assert tokens == [
        TokenKind.EQEQ,
        TokenKind.NEQ,
        TokenKind.LTE,
        TokenKind.GTE,
        TokenKind.EOF,
    ]

def test_integer_literals():
    lx = Lexer("10 0 420")
    tok1 = lx.next_token()
    tok2 = lx.next_token()
    tok3 = lx.next_token()
    tok4 = lx.next_token()

    assert tok1.kind == TokenKind.INT and tok1.src == "10" and tok1.value == 10
    assert tok2.kind == TokenKind.INT and tok2.src == "0" and tok2.value == 0
    assert tok3.kind == TokenKind.INT and tok3.src == "420" and tok3.value == 420
    assert tok4.kind == TokenKind.EOF