from enum import Enum, auto

class TokenKind(Enum):
    """
    Enumeration of all token categories recognized by the Tiny-Lang lexer.

    A TokenKind represents the syntactic classification of a token
    (e.g., integer literal, identifier, operator, delimiter, keyword).

    The lexer assigns a TokenKind to each lexeme extracted from source code.
    The parser then uses this classification to determine grammatical structure.

    Categories:

    Special:
        EOF       - End of input marker.
        ILLEGAL   - Unrecognized or invalid character sequence.

    Literals:
        INT       - Integer literal.
        NAME      - Identifier (variable or function name).

    Keywords:
        LET, IF, ELSE, WHILE, PRINT, FUNC, RETURN

    Operators:
        PLUS      - +
        MINUS     - -
        STAR      - *
        SLASH     - /
        EQUAL     - =
        EQEQ      - ==
        NOT       - !
        NEQ       - !=
        LT        - <
        LTE       - <=
        GT        - >
        GTE       - >=

    Delimiters:
        LPAREN    - (
        RPAREN    - )
        LBRACE    - {
        RBRACE    - }
        COMMA     - ,
        SEMICOLON - ;
    """

    # Special
    EOF = auto()
    ILLEGAL = auto()

    # Literals
    INT = auto()
    NAME = auto()

    # Keywords (add as your language grows)
    LET = auto()
    FUNC = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    EQUAL = auto()
    EQEQ = auto()
    NOT = auto()
    NEQ = auto()

    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()

"""
Mapping of reserved keyword strings to their corresponding TokenKind.

When the lexer reads an identifier (NAME), it checks this table to
determine whether the identifier is actually a reserved keyword.

Example:
    "let"   -> TokenKind.LET
    "print" -> TokenKind.PRINT

If an identifier is not found in this table, it remains TokenKind.NAME.
"""
KEYWORDS: dict[str, TokenKind] = {
    # Standard
    "let": TokenKind.LET,
    "fn": TokenKind.FUNC,
    "return": TokenKind.RETURN,
    "if": TokenKind.IF,
    "else": TokenKind.ELSE,
    "while": TokenKind.WHILE,
    "print": TokenKind.PRINT,

    # Fantasy aliases
    "conjure": TokenKind.LET,
    "ritual": TokenKind.FUNC,
    "bestow": TokenKind.RETURN,
    "upon": TokenKind.IF,
    "lest": TokenKind.ELSE,
    "whilst": TokenKind.WHILE,
}
