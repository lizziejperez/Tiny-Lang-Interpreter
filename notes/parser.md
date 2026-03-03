# 04 - Parser (`parser.py`)

## Goal

Implement a parser that consumes a stream of `Token` objects and produces an Abstract Syntax Tree (AST).

At this stage, the parser will **not** execute code — it will only build structure.

Status: **Planning / Not implemented yet**

## Responsibilities

The parser will be responsible for:

- Enforcing Tiny-Lang grammar rules
- Building structured AST nodes from tokens
- Respecting operator precedence and associativity
- Producing meaningful syntax errors (using token `line` and `col`)

## Design Approach

The parser will be implemented incrementally in increasing levels of language complexity:

1. Build parser skeleton and token navigation utilities (*ongoing*)
2. Define minimal AST node structure (*planned*)
3. Parse primary expressions
4. Implement operator precedence parsing
5. Parse statements (print, expression statements)
6. Parse variable declarations (let)
7. Parse control flow (if, while)
8. Parse functions (fn, return, calls`)
9. Add syntax error reporting and recovery

Each step expands the grammar while keeping previous behavior stable.

## AST Overview

The parser will output an Abstract Syntax Tree (AST).

### High-level structure:

Program  
└── List[Stmt]

Node categories:

- `Expr` (expressions)
- `Stmt` (statements)

Example node types (planned):

- `IntLiteral`
- `Name`
- `Binary`
- `Unary`
- `ExprStmt`
- `LetStmt`
- `PrintStmt`
- `BlockStmt`

### What it means:

A full program is a list of statements.

Example:
```
let x = 10;
print x;
```

Would become something like:
```
Program(
    [
        LetStmt(name="x", value=IntLiteral(10)),
        PrintStmt(Name("x"))
    ]
)
```

## Expression Parsing Strategy

Tiny-Lang expressions require operator precedence handling.

Planned precedence order (lowest to highest):

1. Equality (`==`, `!=`)
2. Comparison (`<`, `<=`, `>`, `>=`)
3. Term (`+`, `-`)
4. Factor (`*`, `/`)
5. Unary (`!`, `-`)
6. Primary (literals, identifiers, grouping)

This will be implemented using a precedence ladder so expressions bind correctly.

Example:

`1 + 2 * 3` parses as `1 + (2 * 3)`.

## Notes

Implementation details (specific methods, fields, and exact node definitions) will be added once Stage 4 development begins.
