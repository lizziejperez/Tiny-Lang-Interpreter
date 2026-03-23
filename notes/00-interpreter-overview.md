# 00 - Interpereter Overview

Most interpereters follow this pipeline:

```
Source Code (text)
        ↓
Lexer
        ↓
Parser
        ↓
AST
        ↓
Interpreter
        ↓
Program Result
```

## 1. Lexer (Tokenizer)

### What it does:
Turns raw text into tokens.

It answers:
“What are the words of this language?”

### Example input:
```
1 + 2 * 3
```

### Lexer output:
```
NUMBER(1)
PLUS
NUMBER(2)
STAR
NUMBER(3)
```

So instead of characters:
```
'1', ' ', '+', ' ', '2', ...
```

You now have meaningful units.

### Lexer’s job:

Skip whitespace

- Recognize numbers
- Recognize operators (+ - * /)
- Recognize parentheses
- Maybe recognize keywords later

It does no math.

It does no grammar validation.

It just groups characters.

## 2. Parser

### What it does:
Turns tokens into structure.

It answers:
“How do these tokens fit together according to grammar rules?”

From my CFG notes:
A grammar defines valid sentence structure

The parser enforces that structure.

### Example tokens:

```
1 + 2 * 3
```

Parser builds structure respecting precedence:

```
        (+)
       /   \
     1     (*)
          /   \
         2     3
```

It understands:

- `*` binds tighter than `+`
- Parentheses override precedence
- Expressions must follow grammar rules

If the input is:

```
1 + * 2
```

Parser says: `Syntax Error`

## 3. AST (Abstract Syntax Tree)

This is the **data structure representation** of the parsed program.

It’s what the parser builds.

Example Python classes:
```
class Number:
    def __init__(self, value):
        self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
```

Your AST for:
```
1 + 2 * 3
```

Would be something like:
```
BinOp(
    Number(1),
    '+',
    BinOp(
        Number(2),
        '*',
        Number(3)
    )
)
```

### Why “Abstract”?

Because it removes unnecessary syntax details.

No whitespace. No parentheses tokens. Just structure.

## 4. Interpreter

### What it does:

Walks the AST and evaluates it.

It answers:
“What does this program mean?”

From my OpSem notes:
Operational semantics gives meaning by describing execution 

That’s exactly what the interpreter is implementing.

### Example evaluation:

Interpreter sees:
```
BinOp(Number(1), '+', BinOp(Number(2), '*', Number(3)))
```

It:

1. Evaluates left → 1
2. Evaluates right → evaluates (2 * 3)
3. Returns 6
4. Returns 1 + 6 = 7

Final result: `7`

## Big Picture
| Stage       | Concerned With | Does Math? | Knows Grammar? |
| ----------- | -------------- | ---------- | -------------- |
| Lexer       | Characters     | ❌ No       | ❌ No           |
| Parser      | Structure      | ❌ No       | ✅ Yes          |
| AST         | Representation | ❌ No       | ✅ Yes          |
| Interpreter | Meaning        | ✅ Yes      | ❌ No           |

## Why This Is Powerful

Once you have this structure, you can later:

- Add variables
- Add functions
- Add conditionals
- Add lambda calculus (👀 from your notes)
- Add type checking
- Add bytecode compilation

This is how real languages work.