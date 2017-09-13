class PredictiveParser:
    """
    Simple predictive parser (recursive-descent parser) for CS420 HW#1

    It parses a sample expression grammar:

    <expr> ::= <term> <expr'>
    <expr'> ::= + <term> <expr'>
              | - <term> <expr'>
              | ε
    <term> ::= <factor> <term'>
    <term'> ::= / <term'>
              | * <term'>
              | ε
    <factor> ::= <number>
               | <id>
    <number> ::= positive integer
    <id> ::= [a-z]
    """

if __name__ == '__main__':
    parser = PredictiveParser()
    expression_str = input().strip()
    abstract_syntax_tree = parser.parse()

    print(abstract_syntax_tree)

