from __future__ import annotations

from dataclasses import dataclass
from typing import List

# Base AST node types
# These define the core node categories used by the parser and interpreter.
# They currently contain no fields or methods and exist primarily for type structure and classification.

class Node:
    """Base class for all AST nodes."""
    pass

class Stmt(Node):
    """Base class for all statement nodes."""
    pass

class Expr(Node):
    """Base class for all expression nodes."""
    pass

# Program root
@dataclass(frozen=True)
class Program(Node):
    """Top-level AST node representing an entire Tiny-Lang program."""
    statements: List[Stmt]

# Expressions
# These AST nodes represent values that can appear inside computations.

@dataclass(frozen=True)
class IntLiteral(Expr):
    """
    Integer literal expression.

    Represents a numeric constant from the source code.
    ex: 10
    """
    value: int


@dataclass(frozen=True)
class Name(Expr):
    """
    Identifier expression.

    Represents a variable reference.
    ex: x
    """
    name: str

@dataclass(frozen=True)
class GroupingExpr(Expr):
    """
    Grouped expression.

    Represents an expression wrapped in parentheses.
    ex:
        (1 + 2)
    """
    expr: Expr  # inner expression inside the parentheses

@dataclass(frozen=True)
class UnaryExpr(Expr):
    """
    Unary expression.

    Represents a unary operator applied to one operand.
    ex:
        -x
        !flag
    """
    op: str
    right: Expr


@dataclass(frozen=True)
class BinaryExpr(Expr):
    """
    Binary expression.

    Represents an infix operator with a left and right operand.
    ex:
        1 + 2
        x * y
    """
    left: Expr
    op: str
    right: Expr

# Statements
# Statement nodes represent executable instructions in the program.

@dataclass(frozen=True)
class ExprStmt(Stmt):
    """
    Expression statement.

    Wraps an expression so it can appear where a statement is required.
    This occurs when an expression is written as a standalone instruction.

    ex:
        1 + 2;
        x;
    """
    expr: Expr  # the expression being evaluated

@dataclass(frozen=True)
class PrintStmt(Stmt):
    """
    Print statement.

    Represents a print instruction that evaluates an expression
    and outputs its value later during interpretation.

    ex:
        print 1 + 2;
        print x;
    """
    expr: Expr