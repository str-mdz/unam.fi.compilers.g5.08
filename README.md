# CompyFI LR(0) – Compilers Project

---

# Description

This project implements an educational compiler-like system developed in Python for the Compilers course at UNAM – Faculty of Engineering.

The system integrates the following compilation stages:

* Lexical Analysis (Lexer)
* LR(0) Syntactic Analysis (Shift-Reduce Parser)
* Syntax-Directed Translation (SDT)
* Basic Semantic Validation and Symbol Table
* Three Address Code (TAC) Generation

The implemented language is a reduced block-based grammar focused on demonstrating how each compilation phase works internally, including visual step-by-step output through a local web interface.

The program generates:

* Tokens produced by the lexer
* Original CFG and augmented grammar
* Canonical LR(0) item collection
* State transitions
* ACTION/GOTO table
* Parsing trace (step-by-step)
* Symbol table
* SDT rules explanation
* Generated TAC intermediate code

The system also reports:

* Lexical errors (unrecognized symbols)
* Syntactic errors (invalid token in current state)
* Semantic errors (validation failure)

---

# Theoretical Concepts

This implementation is based on concepts from:

* Formal Languages and Automata Theory
* Context-Free Grammars (CFG)
* Lexical Analysis
* Bottom-Up Parsing
* LR(0) Parsing and Canonical Collection
* Shift-Reduce Parsing
* Syntax-Directed Translation (SDT)
* Three Address Code (TAC) and Backpatching

---

# Grammar

```text
0. P' -> P
1. P  -> B
2. B  -> { W }
3. B  -> { }
4. W  -> W S
5. W  -> S
6. S  -> while ( C ) B
7. S  -> if ( C ) B
8. S  -> i ;
9. C  -> i < i
```

Where:

* `P` = Program
* `B` = Block
* `W` = Statement list
* `S` = Statement
* `C` = Condition
* `i` = Generic identifier
* `while`, `if` = Reserved words

---

# Project Structure

```text
unam.fi.compilers.g5.08
│
├── src
│   ├── main.py
│   ├── ui.py
│   ├── lexer.py
│   ├── parser_lr0.py
│   ├── sdt.py
│   ├── tac.py
│   ├── index.html
│   └── multimedia/
│
├── docs
│   ├── Proyecto_Final_Compiladores.pdf
│   └── Presentacion_final.pdf
│
├── README.md
└── .gitignore
```

---

# Module Responsibilities

| File            | Responsibility                                                                 |
| --------------- | ------------------------------------------------------------------------------ |
| `main.py`       | Entry point. Starts the local HTTP server and handles GET/POST routes          |
| `ui.py`         | Generates all HTML views and executes the complete compilation flow            |
| `lexer.py`      | Performs lexical analysis and produces ordered list of (type, lexeme) tuples   |
| `parser_lr0.py` | Builds the LR(0) canonical collection, ACTION/GOTO table, and runs the parser  |
| `sdt.py`        | Performs basic semantic validation and builds the symbol table                 |
| `tac.py`        | Generates elementary TAC intermediate code for recognized structures           |
| `index.html`    | Static HTML shell served as the visual entry point                             |
| `multimedia/`   | Visual interface resources (mascot, images)                                    |

---

# Documentation

The complete report and presentation are located in:

```text
docs/Proyecto_Final_Compiladores.pdf
docs/Presentacion_final.pdf
```

The documentation includes:

* Theoretical framework
* Grammar explanation and LR(0) item collection
* State transitions and ACTION/GOTO table
* Parsing trace analysis
* SDT rules and TAC generation
* Semantic validation and symbol table
* System architecture
* Test case analysis

---

# Test Cases

The application includes predefined examples built into the interface. No external test files are required.

| ID | Title | Expected Result |
|----|-------|----------------|
| valid | Block with while and if | Accept — generates full TAC |
| empty | Empty block | Accept — no TAC |
| missing_semicolon | Missing semicolon | Syntactic error |
| incomplete_condition | Incomplete condition | Syntactic error |
| missing_brace | Missing closing brace | Syntactic error |

These examples can be selected directly from the compiler view in the web interface.

---

# Features

* Lexical analysis with error reporting
* LR(0) automaton and canonical item collection generation
* ACTION/GOTO parsing table construction
* Step-by-step shift-reduce parsing trace
* Syntax-Directed Translation (SDT) concepts
* Symbol table generation
* TAC intermediate code generation
* Full web interface with tabbed result panels
* Three-level error handler (lexical, syntactic, semantic)

---

# How to Run

Requirements: **Python 3.10 or higher** with the `Add to PATH` option enabled.

Run the program from the project root:

```bash
python src/main.py
```

Then open your browser at:

```
http://127.0.0.1:8000/index.html
```

To stop the server press `Ctrl+C` in the terminal.

---

# Example Output

The web interface displays:

* Generated tokens
* Original CFG and augmented grammar
* Canonical LR(0) states and transitions
* ACTION/GOTO table
* Step-by-step parsing trace
* Final parsing result
* Symbol table
* SDT rules
* Generated TAC

---

# Authors

* 320198687
* 320301238
* 321132927
* 321132477
* 321332086

Group 5 – Team 8
Computer Engineering
UNAM – Faculty of Engineering
Compilers Course · Semester 2026-II
Computer Engineering
UNAM – Faculty of Engineering
Compilers Course · Semester 2026-II
