class Position:
    def __init__(self, index, line_number, column, file_name, content):
        self.index = index
        self.line_number = line_number
        self.column = column
        self.file_name = file_name
        self.content = content

    def advance(self, current_char = None):
        self.index += 1
        self.column += 1
        if current_char == '\n':
            self.line_number += 1
            self.column = 0

        return self

    def copy(self):
        return Position(self.index, self.line_number, self.column, self.file_name, self.content)