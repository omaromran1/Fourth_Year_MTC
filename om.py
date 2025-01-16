import ast
from collections import Counter
import math

def halstead_metrics(source_code):
    # Parse the source code into an abstract syntax tree
    tree = ast.parse(source_code)
    
    # Initialize counters for operators and operands
    operators = set()
    operands = set()
    operator_count = 0
    operand_count = 0
    
    # Function to identify operators and operands
    def visit_node(node):
        nonlocal operator_count, operand_count
        if isinstance(node, ast.AST):
            # Detect operators
            if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.LShift, ast.RShift,
                                 ast.BitOr, ast.BitXor, ast.BitAnd, ast.FloorDiv, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
                                 ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.And, ast.Or)):
                operators.add(type(node).__name__)
                operator_count += 1
            
            # Detect operands (variable names, literals, etc.)
            if isinstance(node, (ast.Name, ast.Constant)):
                operands.add(getattr(node, 'id', getattr(node, 'value', None)))
                operand_count += 1

        # Visit child nodes
        for child in ast.iter_child_nodes(node):
            visit_node(child)
    
    # Start visiting the AST
    visit_node(tree)
    
    N1 = len(operators)
    N2 = operator_count
    n1 = len(operands)
    n2 = operand_count

    # Halstead metrics
    V = N1 + n1
    L = N2 + n2
    Volume = L * math.log2(V) if V > 0 else 0
    Difficulty = (N1 / 2) * (n2 / n1) if n1 > 0 else 0
    Effort = Difficulty * Volume
    Time = Effort / 18
    Bugs = (Effort ** 2) / 3000

    # Return the metrics
    return {
        'N1 (distinct operators)': N1,
        'N2 (total operators)': N2,
        'n1 (distinct operands)': n1,
        'n2 (total operands)': n2,
        'Vocabulary (V)': V,
        'Length (L)': L,
        'Volume (V)': Volume,
        'Difficulty (D)': Difficulty,
        'Effort (E)': Effort,
        'Time (T)': Time,
        'Bugs (B)': Bugs
    }

# Example usage:
source_code = """
def add(a, b):
    return a + b

result = add(3, 4)
"""
metrics = halstead_metrics(source_code)
for metric, value in metrics.items():
    print(f"{metric}: {value:.2f}")
