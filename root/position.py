class Position:
    def __init__(self, index, line_number, column, content):
        self.index = index
        self.line_number = line_number
        self.column = column
        self.content = content

    def advance(self, current_char = None):
        """
        Advances the current position
        :param current_char: The current character we are at. Used to reset the column and increase the line number if it is a new line character.
        :return: The current postition object.
        """
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line_number += 1
            self.column = 0

        return self

    def copy(self):
        """
        Copies the current position to a new, separate object.
        :return: The copied position.
        """
        return Position(self.index_number, self.column, self.content)