import re
import matplotlib.pyplot as plt
from collections import Counter

def tokenize_cpp(code):
    # Define the token patterns
    token_specification = [
        ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),  # Single line and multi-line comments
        ('KEYWORD', r'\b(int|return|if|else|for|while|do|break|continue|void|float|double|char|bool)\b'),  # C++ keywords
        ('NUMBER',  r'\d+(\.\d*)?'),   # Integer or decimal number
        ('ID',      r'[A-Za-z_]\w*'),  # Identifiers
        ('OP',      r'[+\-*/%=]'),     # Arithmetic operators
        ('ASSIGN',  r'='),             # Assignment operator
        ('END',     r';'),             # Statement terminator
        ('BRACE',   r'[{}]'),          # Curly braces
        ('PARENTHESES', r'[()]'),      # Parentheses
        ('WHITESPACE', r'\s+'),        # Whitespace
        ('UNKNOWN', r'.'),             # Any other character
    ]

    # Compile the regular expression for tokenization
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match

    pos = 0
    match = get_token(code)
    tokens = []
    while match is not None:
        type = match.lastgroup
        if type not in ['WHITESPACE', 'COMMENT']:
            tokens.append(type)
        pos = match.end()
        match = get_token(code, pos)

    if pos != len(code):
        raise RuntimeError(f'Unexpected character {code[pos]} at position {pos}')

    return tokens

def plot_token_distribution(tokens):
    token_counts = Counter(tokens)
    token_types = list(token_counts.keys())
    counts = list(token_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(token_types, counts, color='skyblue')
    plt.xlabel('Token Types')
    plt.ylabel('Count')
    plt.title('Token Distribution in C++ Code')
    plt.show()

# Example usage
cpp_code = '''
int main() {
    // This is a comment
    int x = 10;
    float y = 20.5;
    x = x + y; /* another comment */
    return 0;
}
'''
tokens = tokenize_cpp(cpp_code)
plot_token_distribution(tokens)
