class SyntaxNode:
    """Represents a node in abstract syntax tree."""
    def __init__(self, type, token=None):
        self.parent = None
        self.token = token
        self.left_child = None
        self.right_child = None
        self.type = type

    def is_epsilon(self):
        """
        Determines whether this syntax node is epsilon.

        Returns:
            True if determined epsilon
        """
        return self.token is None

    def __str__(self):
        result = ''
        if self.token is not None:
            result = str(self.token)
        return result


class SyntaxTree:
    """Represents an abstract syntax tree."""
    def __init__(self):
        self.root = None

    def pre_order(self, start_node, nodes=None):
        """
        Pre-order traversal of this abstract syntax tree.
        Args:
            start_node (SyntaxNode): starting point
            nodes (List[SyntaxNode]): result array of traversal

        Returns:
            nodes (List[SyntaxNode]): result array of traversal
        """
        if nodes is None:
            nodes = []

        # print(start_node.type + ':' + str(start_node))

        # it has to traverse right child first...strangely...
        nodes.append(start_node)
        if start_node.right_child is not None:
            nodes = self.pre_order(start_node.right_child, nodes)
        if start_node.left_child is not None:
            nodes = self.pre_order(start_node.left_child, nodes)

        return nodes

    def print_tree(self, option='pre_order'):
        """
        Prints the tree contents in string.
        Args:
            option (str): traversal option

        Returns:
            print_str (str): the string as a result of traversal
        """
        if option == 'preorder':
            nodes = self.pre_order(self.root)
        else:
            nodes = []  # not desired!

        print_str = ''
        for node in nodes:
            print_str += str(node)

        return print_str
