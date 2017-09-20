import re
from typing import List
from grammar_token import Token
from syntax_tree import SyntaxTree, SyntaxNode


class PredictiveParser:
    """
    Simple predictive parser (recursive-descent parser) for CS420 HW#1

    It parses a sample expression grammar (in BNF form):

    <expr> ::= <term> <expr'>
    <expr'> ::= + <term> <expr'>
              | - <term> <expr'>
              | ε
    <term> ::= <factor> <term'>
    <term'> ::= / <term>
              | * <term>
              | ε
    <factor> ::= <number>
               | <id>
    <number> ::= positive integer
    <id> ::= [a-z]
    """
    def __init__(self):
        self.expression = ''
        self.token_arr = []

    @staticmethod
    def tokenize(expression: str):
        """
        Tokenize the input expression represented as string.
        Args:
            expression (str): expression string to parse

        Returns:
            token_arr (List[Token]): list of tokens
        """
        regex = re.compile('[a-zA-Z]|\d+|\*|\+|-|/')  # split into tokens
        token_strings = regex.finditer(expression.strip().replace(' ', ''))

        token_arr = []
        for exp in token_strings:
            tok_str = exp.group(0)
            token_arr.append(Token(tok_str))

        if ''.join([str(tok) for tok in token_arr]) \
                != expression.strip().replace(' ', ''):
            raise InputError()

        return token_arr

    def parse(self, expression: str):
        """
        Parses the expression and turns into an abstract syntax tree.

        Args:
            expression (str): expression string to parse

        Returns:
            tree (SyntaxTree): abstract syntax tree
        """
        self.expression = expression
        self.token_arr = self.tokenize(expression=expression)

        token_arr, tree_stack = self.expr(token_arr=self.token_arr, tree_stack=[])

        tree = SyntaxTree()
        tree.root = tree_stack.pop()

        if len(token_arr) != 0:
            raise SyntaxError('Leftover tokens : {}'.format(
                [str(tok) for tok in token_arr]))

        return tree

    @staticmethod
    def match(token, lookahead):
        """
        Tests if the token matches the lookahead symbol.

        Args:
            token (Token|str): token to match
            lookahead (Token): lookahead symbol

        Returns:
            True if it matches
        """
        if not lookahead.is_terminal() or not token == lookahead:
            raise SyntaxError('Syntax Error: {}'.format(token))
        return True

    def expr(self, token_arr: List[Token], tree_stack):
        """
        Handles <expr>, given the remaining list of tokens
        and stack for tree nodes
        Args:
            token_arr (List[Token]): list of remaining tokens
            tree_stack (List[SyntaxNode]): list of syntax nodes

        Returns:
            (result_token_array, syntax_tree_stack):
                the resulting token array and tree stack
        """
        result_token_array, syntax_tree_stack = self.term(
            token_arr=token_arr, tree_stack=tree_stack)
        result_token_array, syntax_tree_stack = self.expr_prime(
            token_arr=result_token_array, tree_stack=syntax_tree_stack)

        # create the tree from stack contents
        # pop three and create a subtree. push it back in.
        if len(syntax_tree_stack) > 2:
            left_child = syntax_tree_stack.pop()
            head = syntax_tree_stack.pop()
            right_child = syntax_tree_stack.pop()

            head.left_child = left_child
            head.right_child = right_child
            left_child.parent = head
            right_child.parent = head

            # push subtree in
            syntax_tree_stack.append(head)
        return result_token_array, syntax_tree_stack

    def term(self, token_arr, tree_stack):
        """
        Handles <term>, given the remaining list of tokens
        and stack for tree nodes

        Args:
            token_arr (List[Token]): list of remaining tokens
            tree_stack (List[SyntaxNode]): list of syntax nodes

        Returns:
            (result_token_array, syntax_tree_stack):
                the resulting token array and tree stack
        """
        result_token_array, tree_stack = self.factor(token_arr, tree_stack=tree_stack)
        result_token_array, tree_stack = self.term_prime(result_token_array, tree_stack=tree_stack)

        # create the tree from stack contents
        if len(tree_stack) > 2:
            left_child = tree_stack.pop()
            head = tree_stack.pop()
            right_child = tree_stack.pop()

            head.left_child = left_child
            head.right_child = right_child
            left_child.parent = head
            right_child.parent = head

            tree_stack.append(head)

        return result_token_array, tree_stack

    def expr_prime(self, token_arr, tree_stack):
        """
        Handles <expr'>, given the remaining list of tokens
        and stack for tree nodes

        Args:
            token_arr (List[Token]): list of remaining tokens
            tree_stack (List[SyntaxNode]): list of syntax nodes

        Returns:
            (result_token_array, syntax_tree_stack):
                the resulting token array and tree stack
        """
        if len(token_arr) == 0:
            return [], tree_stack  # epsilon

        # match the lookahead symbol
        token_array = token_arr.copy()
        lookahead = token_array[0]

        if str(lookahead) == '+':
            self.match('+', lookahead)
        elif str(lookahead) == '-':
            self.match('-', lookahead)
        else:
            return token_arr, tree_stack  # epsilon

        syntax_node = SyntaxNode('expr_prime', lookahead)
        tree_stack.append(syntax_node)
        token_array = token_array[1:]

        token_array, tree_stack = self.term(token_array, tree_stack=tree_stack)
        token_array, tree_stack = self.expr_prime(token_array, tree_stack=tree_stack)
        return token_array, tree_stack

    def term_prime(self, token_arr, tree_stack):
        """
        Handles <term'>, given the remaining list of tokens
        and stack for tree nodes

        Args:
            token_arr (List[Token]): list of remaining tokens
            tree_stack (List[SyntaxNode]): list of syntax nodes

        Returns:
            (result_token_array, syntax_tree_stack):
                the resulting token array and tree stack
        """
        if len(token_arr) == 0:
            return [], tree_stack  # epsilon

        token_array = token_arr.copy()
        lookahead = token_arr[0]

        if str(lookahead) == '*':
            self.match('*', lookahead)
        elif str(lookahead) == '/':
            self.match('/', lookahead)
        else:
            return token_arr, tree_stack  # epsilon

        syntax_node = SyntaxNode('term_prime', lookahead)
        tree_stack.append(syntax_node)
        token_array = token_array[1:]
        return self.term(token_array, tree_stack=tree_stack)

    def factor(self, token_arr, tree_stack):
        """
        Handles <factor>, given the remaining list of tokens
        and stack for tree nodes

        Args:
            token_arr (List[Token]): list of remaining tokens
            tree_stack (List[SyntaxNode]): list of syntax nodes

        Returns:
            (result_token_array, syntax_tree_stack):
                the resulting token array and tree stack
        """
        token_array = token_arr.copy()
        try:
            lookahead = token_array[0]
        except IndexError:
            raise SyntaxError(
                'Syntax Error: token empty - expected <factor>')

        if lookahead.type == 'number':
            token_array = self.number(token_array)
        elif lookahead.type == 'id':
            token_array = self.id(token_array)
        else:
            raise SyntaxError('Syntax Error : {} at function factor()'
                              .format(lookahead))

        syntax_node = SyntaxNode('factor', lookahead)
        tree_stack.append(syntax_node)  # push the terminal into syntax node
        return token_array, tree_stack

    @staticmethod
    def number(token_arr):
        """
        Handles <number>, given the remaining list of tokens.

        Args:
            token_arr (List[Token]): list of remaining tokens

        Returns:
            result_token_array (List[Token]): token array after processing
        """
        try:
            lookahead = token_arr[0]
            if lookahead.type != 'number':
                raise SyntaxError(
                    'Syntax Error: {} is not a number; at function number()'
                    .format(lookahead))
            token_array = token_arr[1:]
            return token_array
        except IndexError:
            raise SyntaxError('Syntax Error : {} at function number()'
                              .format(token_arr))

    @staticmethod
    def id(token_arr):
        """
        Handles <id>, given the remaining list of tokens.

        Args:
            token_arr (List[Token]): list of remaining tokens

        Returns:
            result_token_array (List[Token]): token array after processing
        """
        try:
            lookahead = token_arr[0]
            if lookahead.type != 'id':
                raise SyntaxError(
                    'Syntax Error: {} is not an id; at function id()'
                    .format(lookahead))
            token_array = token_arr[1:]
            return token_array
        except IndexError:
            raise SyntaxError('Syntax Error: {} at function id()'
                              .format(token_arr))


class InputError(Exception):
    pass


if __name__ == '__main__':
    parser = PredictiveParser()
    with open('./res/hw1/input.txt', 'r') as in_f, open('./res/hw1/output.txt', 'w') as out_f:
        for input_line in in_f:
            print(input_line)
            try:
                tree = parser.parse(input_line)
                result = tree.print_tree('preorder')
            except:
                result = 'incorrect syntax'

            out_f.write('{}\n'.format(result))

    # tree = parser.parse('x-2*y')
    # tree.print_tree('preorder')
    #
    # tree = parser.parse('a + 35 - b')
    # tree.print_tree('preorder')
    #
    # tree = parser.parse('10+*5')
    # tree.print_tree('preorder')
