import ply.lex as lex
import ply.yacc as yacc

# --- Lexer ---
tokens = (
    'ID', 'NUMBER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'ASSIGN', 
    'PLUS', 'MINUS', 'MULT', 'DIV', 'TYPE', 'RETURN', 'IF', 'WHILE', 'FOR', 'ELSE', 'COMPARISON',
)

reserved = {
    'int': 'TYPE', 'float': 'TYPE', 'return': 'RETURN', 'if': 'IF', 
    'else': 'ELSE', 'while': 'WHILE', 'for': 'FOR',
}

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_COMPARISON = r'==|!=|<=|>=|<|>'
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# --- Semantic Analysis ---
symbol_table = {}
temp_counter = 0

def add_to_symbol_table(identifier, type_):
    if identifier in symbol_table:
        print(f"Error: Variable '{identifier}' already declared.")
    else:
        symbol_table[identifier] = type_

def check_variable_exists(identifier):
    if identifier not in symbol_table:
        print(f"Error: Variable '{identifier}' is not declared.")
        return False
    return True

def generate_temp_var():
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"

# --- Parser ---

# Precedence rules
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('left', 'COMPARISON'),
)

# Grammar rules
def p_program(p):
    '''program : statement_list'''
    print("Parsing successful!")
    print("Symbol Table: ", symbol_table)

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    pass

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | RETURN expression SEMICOLON
                 | if_statement
                 | while_statement
                 | for_statement'''
    pass

def p_declaration(p):
    '''declaration : TYPE ID SEMICOLON
                   | TYPE ID ASSIGN expression SEMICOLON'''
    # Add variable to symbol table
    add_to_symbol_table(p[2], p[1])

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    # Check if the variable exists
    if not check_variable_exists(p[1]):
        return
    # Generate code for assignment
    temp_var = generate_temp_var()
    print(f"{temp_var} = {p[3]}")  # Use the temporary variable for intermediate results

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block
                    | IF LPAREN expression RPAREN block ELSE block'''
    pass

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN block'''
    pass

def p_for_statement(p):
    '''for_statement : FOR LPAREN for_initializer SEMICOLON for_condition SEMICOLON for_increment RPAREN block'''
    pass

def p_for_initializer(p):
    '''for_initializer : declaration
                       | assignment
                       | ID ASSIGN expression
                       | empty'''
    pass

def p_for_condition(p):
    '''for_condition : expression
                     | empty'''
    pass

def p_for_increment(p):
    '''for_increment : assignment
                     | empty'''
    pass

def p_block(p):
    '''block : LBRACE statement_list RBRACE
             | LBRACE RBRACE'''
    pass

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | expression COMPARISON term'''
    if len(p) == 4:
        left = p[1]
        operator = p[2]
        right = p[3]
        temp_var = generate_temp_var()
        print(f"{temp_var} = {left} {operator} {right}")
        p[0] = temp_var
    else:
        p[0] = p[1]

def p_term(p):
    '''term : factor
            | term MULT factor
            | term DIV factor'''
    if len(p) == 4:
        left = p[1]
        operator = p[2]
        right = p[3]
        temp_var = generate_temp_var()
        print(f"{temp_var} = {left} {operator} {right}")
        p[0] = temp_var
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expression RPAREN'''
    if isinstance(p[1], int):
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# --- Code Generation ---

def generate_code(p):
    code = []
    if isinstance(p[1], int):
        code.append(f"LOAD {p[1]}")
    elif isinstance(p[1], str):
        code.append(f"LOAD {p[1]}")
    return code

# --- Main Program ---
if __name__ == "__main__":
    cpp_code = """
    int x = 5;
    int y = 10;
    x = x + 5;
    return x;
    """

    print("Tokens:")
    lexer.input(cpp_code)
    for token in lexer:
        print(token)

    print("\nParsing:")
    parser.parse(cpp_code)
    
    # Code Generation
    print("\nGenerated Code:")
    # Example of code generation for the assignment:
    generated_code = generate_code([None, 5])  # This is a simple simulation, would vary based on actual parsing
    for line in generated_code:
        print(line)
