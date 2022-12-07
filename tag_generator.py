import tag
import position
import tag_lists
import string
import settings

class TagGenerator:
    def __init__(self, file_name, markup):
        self.file_name = file_name
        self.markup = markup

        self.position = position.Position(-1, 0, -1, file_name, markup)

        self.current_char = None
        self.advance()

    def advance(self):
        """
        Advances the current position by 1.
        """
        self.position.advance(self.current_char)
        self.current_char = self.markup[self.position.index] if self.position.index < len(self.markup) else None

    def make_tags(self) -> []:
        """
        Creates and returns a list of tag objects.
        :return: A list of HTML tag objects.
        """
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
                print(f'Invalid character at line {self.position.line_number}, column {self.position.column}')
                break

        return tags

    def generate_tag(self):
        """
        Generates a tag.
        :return: The tag object.
        """

        # name
        id = ''

        # Get name
        while self.current_char != None and self.current_char in tag_lists.VALID_CHARACTERS:
            id += self.current_char
            self.advance()

        # check if element is inline (doesn't need a closing tag)
        inline = id in tag_lists.INLINE_ELEMENTS

        # skip whitespaces
        while self.current_char == " ":
            self.advance()

        # the content inside of the tag
        content = ''

        # the tags properties (href, class, etc...)
        properties = self.generate_properties()

        # add inner tags if it isn't inline.
        if not inline:
            # skip to opening brace
            while self.current_char != settings.INNER_LEFT_BRACE:
                self.advance()

            # brace stack. should end on 0.
            stack = 0

            while self.current_char != None:
                # push one to stack
                if self.current_char == settings.INNER_LEFT_BRACE:
                    stack += 1

                # remove one from stack
                elif self.current_char == settings.INNER_RIGHT_BRACE:
                    stack -= 1

                content += self.current_char

                # break out of loop when we have reached the correct closing brace
                if self.current_char == settings.INNER_RIGHT_BRACE and stack == 0:
                    break

                # advance to next position.
                self.advance()

            # trim content by one character on either side.
            content = content[1:len(content)-1]

        self.advance()

        # return tag object.
        return tag.Tag(id, content, properties, inline = inline)

    def generate_string(self):
        """
        Generates a string. What would be plain text in normal HTML.
        :return: String tag.
        """
        string = ''

        self.advance()

        # temporarily exiting the string.
        escape_character = False
        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        # we want to continue adding to the string
        while self.current_char != None and (self.current_char != '"' or escape_character):
            # we want to exit the string
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)

            else:
                # \n, \t, etc...
                if self.current_char == '\\':
                    escape_character = True

                # just add to the string
                else:
                    string += self.current_char

            self.advance()

            escape_character = False

        self.advance()

        # return the string object
        return tag.Tag("str", string, inline = False, formatting = "%content%", no_inner_tags = True)

    def generate_comment(self):
        """
        Generates a comment tag
        :return: A comment tag object
        """
        content = ''

        self.advance()

        # Not a new line, and not a null character
        while self.current_char != '\n' and self.current_char != None:
            content += self.current_char
            self.advance()

        self.advance()

        return tag.Tag('comment', content, inline = False, formatting = '<!--%content%-->', no_inner_tags = True)

    def generate_properties(self) -> []:
        """
        Generates the properties of a tag
        :return: A 2D array of properties - name, and value.
        """
        properties = []

        # we are adding properties
        if self.current_char == settings.PROPERTY_LEFT_BRACE:
            self.advance()

            # we haven't hit the end of our properties
            while self.current_char != settings.PROPERTY_RIGHT_BRACE:
                # whitespace or property separator
                if self.current_char in " ,":
                    self.advance()

                # property name
                property_id = ""
                while not self.current_char in "=":
                    property_id += self.current_char
                    self.advance()

                self.advance()

                # property value
                value = ""

                # we haven't reached a separator or an ending brace
                while not self.current_char in [',', settings.PROPERTY_RIGHT_BRACE]:
                    value += self.current_char
                    self.advance()

                # add to list
                properties.append([property_id, value])

        return properties