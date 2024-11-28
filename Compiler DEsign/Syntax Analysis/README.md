# C++ Syntax Analyzer (Parser) in Python

This project implements a **C++ Syntax Analyzer** (Parser) using **Python** and the **PLY** (Python Lex-Yacc) library. The parser is capable of analyzing C++ source code, recognizing key constructs such as **variables**, **expressions**, **conditionals**, **loops**, and **increment operators** (`++`).

## Features

- **Lexical Analysis**: Tokenizes C++ source code into distinct tokens like keywords, operators, and identifiers.
- **Syntax Analysis**: Supports parsing for:
  - Variable declarations (`int x = 0;`)
  - Assignment statements (`x = x + 1;`)
  - Conditional statements (`if`, `else`)
  - Loop constructs (`for`, `while`)
  - Increment operators (`++i`, `i++`)
- **Error Reporting**: The parser provides detailed feedback about syntax errors and their locations.

## Requirements

- Python 3.x
- **PLY** (Python Lex-Yacc) library

### Installing Dependencies

To get started, make sure you have Python 3 installed. Then, install the necessary library by running:

```bash
pip install ply
