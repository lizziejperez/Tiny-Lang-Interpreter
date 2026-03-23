from tinylang.lexer import Lexer
from tinylang.parser import Parser, ParseError
from tinylang.token import TokenKind
from tinylang.ast import (
    Program,
    IntLiteral,
    Name,
    GroupingExpr,
    UnaryExpr,
    BinaryExpr,
    ExprStmt,
    PrintStmt
)

# ----------------------------------------
# Phase 1: Parser navigation utilities
# ----------------------------------------

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

# ----------------------------------------
# Phase 2: Primary expression parsing
# ----------------------------------------

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

# ----------------------------------------
# Phase 3: Operator precedence parsing
# ----------------------------------------

def test_parse_unary_minus():
    p = Parser(Lexer("-123"))

    expr = p.parse_expression()

    # Unary minus should parse into a UnaryExpr node
    assert expr == UnaryExpr("-", IntLiteral(123))

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_unary_not():
    p = Parser(Lexer("!mana"))

    expr = p.parse_expression()

    # Logical not should parse into a UnaryExpr node
    assert expr == UnaryExpr("!", Name("mana"))

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_factor_multiplication():
    p = Parser(Lexer("2 * 3"))

    expr = p.parse_expression()

    # Multiplication should parse into a BinaryExpr node
    assert expr == BinaryExpr(IntLiteral(2), "*", IntLiteral(3))

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_term_addition():
    p = Parser(Lexer("1 + 2"))

    expr = p.parse_expression()

    # Addition should parse into a BinaryExpr node
    assert expr == BinaryExpr(IntLiteral(1), "+", IntLiteral(2))

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_precedence_multiplication_before_addition():
    p = Parser(Lexer("1 + 2 * 3"))

    expr = p.parse_expression()

    # Multiplication should bind tighter than addition
    assert expr == BinaryExpr(
        IntLiteral(1),
        "+",
        BinaryExpr(IntLiteral(2), "*", IntLiteral(3)),
    )

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_precedence_grouping_overrides_default():
    p = Parser(Lexer("(1 + 2) * 3"))

    expr = p.parse_expression()

    # Parentheses should override normal precedence
    assert expr == BinaryExpr(
        GroupingExpr(
            BinaryExpr(IntLiteral(1), "+", IntLiteral(2))
        ),
        "*",
        IntLiteral(3),
    )

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_comparison():
    p = Parser(Lexer("1 < 2"))

    expr = p.parse_expression()

    # Comparison should parse into a BinaryExpr node
    assert expr == BinaryExpr(IntLiteral(1), "<", IntLiteral(2))

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_equality():
    p = Parser(Lexer("1 == 2"))

    expr = p.parse_expression()

    # Equality should parse into a BinaryExpr node
    assert expr == BinaryExpr(IntLiteral(1), "==", IntLiteral(2))

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_precedence_comparison_before_equality():
    p = Parser(Lexer("1 == 2 < 3"))

    expr = p.parse_expression()

    # Comparison should bind tighter than equality
    assert expr == BinaryExpr(
        IntLiteral(1),
        "==",
        BinaryExpr(IntLiteral(2), "<", IntLiteral(3)),
    )

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_left_associative_term():
    p = Parser(Lexer("10 - 3 - 1"))

    expr = p.parse_expression()

    # Term operators should associate left-to-right
    assert expr == BinaryExpr(
        BinaryExpr(IntLiteral(10), "-", IntLiteral(3)),
        "-",
        IntLiteral(1),
    )

    # After consuming the expression, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF

# ----------------------------------------
# Phase 4: Statement parsing
# ----------------------------------------

def test_parse_expr_stmt_int_literal():
    p = Parser(Lexer("123;"))

    stmt = p.parse_statement()

    # Integer expression statements should parse into ExprStmt nodes
    assert stmt == ExprStmt(IntLiteral(123))

    # After consuming the statement, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_expr_stmt_name():
    p = Parser(Lexer("mana;"))

    stmt = p.parse_statement()

    # Identifier expression statements should parse into ExprStmt nodes
    assert stmt == ExprStmt(Name("mana"))

    # After consuming the statement, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_expr_stmt_binary_expression():
    p = Parser(Lexer("1 + 2;"))

    stmt = p.parse_statement()

    # Full expressions should be allowed inside expression statements
    assert stmt == ExprStmt(
        BinaryExpr(IntLiteral(1), "+", IntLiteral(2))
    )

    # After consuming the statement, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_expr_stmt_missing_semicolon():
    p = Parser(Lexer("123"))

    try:
        # Missing ';' should raise ParseError
        p.parse_statement()

        # If no error was raised, the test should fail
        assert False, "Expected ParseError"

    except ParseError as e:
        # Ensure the error mentions the missing semicolon
        assert ";" in str(e)


def test_parse_print_stmt_int_literal():
    p = Parser(Lexer("print 123;"))

    stmt = p.parse_statement()

    # Print statements should parse into PrintStmt nodes
    assert stmt == PrintStmt(IntLiteral(123))

    # After consuming the statement, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_print_stmt_name():
    p = Parser(Lexer("print mana;"))

    stmt = p.parse_statement()

    # Print statements should allow identifier expressions
    assert stmt == PrintStmt(Name("mana"))

    # After consuming the statement, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_print_stmt_expression():
    p = Parser(Lexer("print 1 + 2;"))

    stmt = p.parse_statement()

    # Print statements should allow full expressions
    assert stmt == PrintStmt(
        BinaryExpr(IntLiteral(1), "+", IntLiteral(2))
    )

    # After consuming the statement, the parser should now be at EOF
    assert p.peek().kind == TokenKind.EOF


def test_parse_print_stmt_missing_semicolon():
    p = Parser(Lexer("print 123"))

    try:
        # Missing ';' should raise ParseError
        p.parse_statement()

        # If no error was raised, the test should fail
        assert False, "Expected ParseError"

    except ParseError as e:
        # Ensure the error mentions the missing semicolon
        assert ";" in str(e)

# ----------------------------------------
# Phase 5: Full program parsing
# ----------------------------------------

def test_parse_program_with_expr_and_print_statements():
    p = Parser(Lexer("123; print 4;"))

    program = p.parse()

    # The parser should build a full Program node from multiple statements
    assert program == Program([
        ExprStmt(IntLiteral(123)),
        PrintStmt(IntLiteral(4)),
    ])


def test_parse_program_with_multiple_statement_types():
    p = Parser(Lexer("print 1 + 2; mana;"))

    program = p.parse()

    # The parser should support mixing print and expression statements
    assert program == Program([
        PrintStmt(BinaryExpr(IntLiteral(1), "+", IntLiteral(2))),
        ExprStmt(Name("mana")),
    ])