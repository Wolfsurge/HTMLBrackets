import tag
import position
import tag_lists
import string

class TagGenerator:
    def __init__(self, file_name, markup):
        self.file_name = file_name
        self.markup = markup

        self.position = position.Position(-1, 0, -1, file_name, markup)

        self.current_char = None
        self.advance()

    def advance(self):
        self.position.advance(self.current_char)
        self.current_char = self.markup[self.position.index] if self.position.index < len(self.markup) else None

    def make_tags(self) -> []:
        tags = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in '~':
                tags.append(self.generate_comment())
            elif self.current_char == '"':
                tags.append(self.generate_string())
            elif self.current_char == '\n':
                self.advance()
            elif self.current_char in tag_lists.VALID_CHARACTERS:
                tags.append(self.generate_tag())
            else:
                print(self.current_char)

        return tags

    def generate_tag(self):
        id = ''
        start = self.position.copy()

        while self.current_char != None and self.current_char in tag_lists.VALID_CHARACTERS:
            id += self.current_char
            self.advance()

        inline = id in tag_lists.INLINE_ELEMENTS

        content = ''
        properties = []

        if not inline:
            while self.current_char == " ":
                self.advance()

            ############################
            #  BEGIN PROPERTY ADDITION #
            ############################
            if self.current_char == "[":
                self.advance()

                while self.current_char != "]":
                    if self.current_char in " ,":
                        self.advance()

                    property_id = ""
                    while self.current_char != "=":
                        property_id += self.current_char
                        self.advance()

                    self.advance()

                    value = ""
                    while not self.current_char in [',', ']']:
                        value += self.current_char
                        self.advance()

                    properties.append([property_id, value])

            while self.current_char != '{':
                self.advance()

            stack = 0
            while self.current_char != None:
                if self.current_char == '{':
                    stack += 1
                elif self.current_char == '}':
                    stack -= 1

                content += self.current_char

                if self.current_char == '}' and stack == 0:
                    break

                self.advance()

            self.advance()

            content = content[1:len(content)-1]

        return tag.Tag(id, content, properties, inline = inline)

    def generate_string(self):
        string = ''

        pos_start = self.position.copy()
        escape_character = False

        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char

            self.advance()

            escape_character = False

        self.advance()

        return tag.Tag("str", string, inline = False, formatting = "%content%", no_inner_tags = True)

    def generate_comment(self):
        content = ''

        self.advance()

        while self.current_char != '\n' and self.current_char != None:
            content += self.current_char
            self.advance()

        self.advance()

        return tag.Tag('comment', content, inline = False, formatting = '<!--%content%-->', no_inner_tags = True)