from tinylang.token import Token, TokenKind, KEYWORDS

def test_token_initialization():
    token = Token(TokenKind.INT, "123", 1, 5, value=123)

    assert token.kind == TokenKind.INT
    assert token.src == "123"
    assert token.line == 1
    assert token.col == 5
    assert token.value == 123


def test_token_without_value():
    token = Token(TokenKind.NAME, "x", 2, 3)

    assert token.kind == TokenKind.NAME
    assert token.src == "x"
    assert token.line == 2
    assert token.col == 3
    assert token.value is None


def test_keywords_mapping_standard():
    assert KEYWORDS["let"] == TokenKind.LET
    assert KEYWORDS["fn"] == TokenKind.FUNC
    assert KEYWORDS["return"] == TokenKind.RETURN


def test_keywords_mapping_fantasy_aliases():
    assert KEYWORDS["conjure"] == TokenKind.LET
    assert KEYWORDS["ritual"] == TokenKind.FUNC
    assert KEYWORDS["bestow"] == TokenKind.RETURN
    assert KEYWORDS["upon"] == TokenKind.IF
    assert KEYWORDS["lest"] == TokenKind.ELSE
    assert KEYWORDS["whilst"] == TokenKind.WHILE


def test_non_keyword_not_in_keywords():
    assert "mana" not in KEYWORDS