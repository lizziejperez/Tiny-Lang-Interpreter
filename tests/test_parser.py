from tinylang.lexer import Lexer
from tinylang.parser import Parser, ParseError
from tinylang.token import TokenKind
from tinylang.ast import IntLiteral, Name, GroupingExpr


def test_parser_advance_and_peek():
    p = Parser(Lexer("+"))

    # Ensure peek() returns the current token without consuming it
    assert p.peek().kind == TokenKind.PLUS

    tok = p.advance()

    # Ensure advance() returns the consumed token
    assert tok.kind == TokenKind.PLUS

    # After consuming '+', the parser should now be positioned at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parser_match():
    p = Parser(Lexer("+"))

    # match() should return True and consume the token when it matches
    assert p.match(TokenKind.PLUS) is True

    # After consuming '+', the current token should now be EOF
    assert p.peek().kind == TokenKind.EOF

    # match() should return False when the current token does not match
    assert p.match(TokenKind.MINUS) is False


def test_parser_expect_success():
    p = Parser(Lexer(";"))

    # expect() should consume the token when the correct kind is found
    p.expect(TokenKind.SEMICOLON, "Expected ';'")

    # After consuming ';', the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parser_expect_error_includes_position():
    p = Parser(Lexer("+"))

    try:
        # expect() should raise ParseError when the token kind does not match
        p.expect(TokenKind.SEMICOLON, "Expected ';'")

        # If no error was raised, the test should fail
        assert False, "Expected ParseError"

    except ParseError as e:
        # Ensure the error message contains position information
        assert "line" in str(e) and "col" in str(e)

def test_parse_primary_int_literal():
    p = Parser(Lexer("123"))

    expr = p.parse_primary()

    # Integer literals should parse into IntLiteral nodes
    assert expr == IntLiteral(123)

    # After consuming the integer, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_primary_name():
    p = Parser(Lexer("mana"))

    expr = p.parse_primary()

    # Identifiers should parse into Name nodes
    assert expr == Name("mana")

    # After consuming the identifier, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_primary_grouping():
    p = Parser(Lexer("(123)"))

    expr = p.parse_primary()

    # Parenthesized expressions should parse into GroupingExpr nodes
    assert expr == GroupingExpr(IntLiteral(123))

    # After consuming the grouped expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_primary_missing_right_paren():
    p = Parser(Lexer("(123"))

    try:
        # Missing ')' should raise ParseError
        p.parse_primary()

        # If no error was raised, the test should fail
        assert False, "Expected ParseError"

    except ParseError as e:
        # Ensure the error mentions the missing closing parenthesis
        assert ")" in str(e)


def test_parse_primary_error_on_non_expression_token():
    p = Parser(Lexer(";"))

    try:
        # A semicolon by itself is not a valid primary expression
        p.parse_primary()

        # If no error was raised, the test should fail
        assert False, "Expected ParseError"

    except ParseError as e:
        # Ensure the error message says an expression was expected
        assert "Expected expression" in str(e)