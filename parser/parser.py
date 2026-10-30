"""
Simple Arithmetic Interpreter

Grammar (BNF, as designed):
    Expr   -> Expr '+' Term | Expr '-' Term | Term
    Term   -> Term '*' Factor | Factor
    Factor -> NUMBER | '(' Expr ')'
    NUMBER -> one or more digits

Grammar (EBNF, as implemented - left recursion replaced by repetition):
    Expr   -> Term   { ('+' | '-') Term }
    Term   -> Factor { '*' Factor }
    Factor -> NUMBER | '(' Expr ')'

Each parse_* method below implements one rule, so '*' binds tighter than
'+' and '-', all operators are left-associative, and parentheses override
the default precedence.
"""

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, expression):
        self.expr = expression.replace(' ', '')
        self.pos = 0
        self.current_char = self.expr[0] if self.expr else None

    def advance(self):
        self.pos += 1
        self.current_char = self.expr[self.pos] if self.pos < len(self.expr) else None

    def parse_number(self):
        # NUMBER -> one or more digits
        digits = ''
        while self.current_char is not None and self.current_char.isdigit():
            digits += self.current_char
            self.advance()
        if not digits:
            raise SyntaxError(f"Expected a number at position {self.pos}")
        return NumberNode(int(digits))

    def parse_factor(self):
        # Factor -> NUMBER | '(' Expr ')'
        if self.current_char == '(':
            self.advance()                      # consume '('
            node = self.parse_expression()
            if self.current_char != ')':
                raise SyntaxError(f"Expected ')' at position {self.pos}")
            self.advance()                      # consume ')'
            return node                         # parentheses leave no node behind
        return self.parse_number()

    def parse_term(self):
        # Term -> Factor { '*' Factor }
        node = self.parse_factor()
        while self.current_char == '*':
            op = self.current_char
            self.advance()
            node = BinaryOpNode(node, op, self.parse_factor())   # left-associative
        return node

    def parse_expression(self):
        # Expr -> Term { ('+' | '-') Term }
        node = self.parse_term()
        while self.current_char in ('+', '-'):
            op = self.current_char
            self.advance()
            node = BinaryOpNode(node, op, self.parse_term())     # left-associative
        return node

def evaluate(node):
    # Post-order traversal: evaluate both children, then apply the operator
    if isinstance(node, NumberNode):
        return node.value
    left = evaluate(node.left)
    right = evaluate(node.right)
    if node.op == '+':
        return left + right
    if node.op == '-':
        return left - right
    if node.op == '*':
        return left * right
    raise ValueError(f"Unknown operator: {node.op}")

def interpret(expression):
    parser = Parser(expression)
    ast = parser.parse_expression()
    return evaluate(ast)

def ast_to_string(node):
    # Helper for displaying the AST structure
    if isinstance(node, NumberNode):
        return str(node.value)
    return f"({ast_to_string(node.left)} {node.op} {ast_to_string(node.right)})"

# Test cases
if __name__ == "__main__":
    test_expressions = [
        "42",
        "2 + 3",
        "10 - 4",
        "3 * 7",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "1 + 2 + 3",
        "10 - 5 - 2",
        "((1 + 2) * 3) - 4"
    ]

    print("Dani Olaosebikan")
    print("Arithmetic Interpreter Test")
    for expr in test_expressions:
        try:
            result = interpret(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error interpreting '{expr}': {e}")

    # Show the AST grouping the parser builds for each expression
    print()
    print("AST structure (fully parenthesized)")
    for expr in test_expressions + ["2 + 3 * (4 - 1)"]:
        ast = Parser(expr).parse_expression()
        print(f"{expr}  ->  {ast_to_string(ast)}  =  {evaluate(ast)}")
