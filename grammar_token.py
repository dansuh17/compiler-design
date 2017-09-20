import re


class Token:
    """
    Represents a syntax token.
    """
    def __init__(self, token_string: str):
        self.type = self.find_type(token_string=token_string)
        self._str = token_string

    @staticmethod
    def find_type(token_string: str):
        """
        Finds the token's type as following the syntax tree.

        Args:
            token_string (str): token string

        Returns:
            type (str): the type defined in BNF form
        """
        if re.compile('\d+').match(token_string):
            return 'number'
        elif re.compile('[a-zA-Z]').match(token_string):
            return 'id'
        elif re.compile('\*|\+|-|/').match(token_string):
            return 'op'
        else:
            return 'undefined'

    def is_terminal(self):
        """
        Determines whether it is a terminal or non terminal
        Returns:
            True if terminal
        """
        return self.type == 'number' or self.type == 'op'

    def __str__(self):
        return self._str

    def __eq__(self, other):
        if type(other) == str:
            return other == str(self)
        elif type(other) == Token:
            return str(self) == str(other)
