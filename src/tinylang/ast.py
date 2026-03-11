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
