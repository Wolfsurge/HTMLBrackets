import tag
import position
import tag_lists
import string
import settings

class TagGenerator:
    def __init__(self, markup, name = ""):
        self.markup = markup
        self.name = name

        self.position = position.Position(-1, 0, -1, markup)

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

        if self.name in tag_lists.TAG_EXCLUDED_ELEMENTS:
            if settings.DEBUG:
                print("Excluded element found, overriding tag generation...")

            tags.append(tag.Tag("str", self.markup, inline = False, formatting = "%content%", no_inner_tags = True))
            
            return tags
        
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()

            elif self.current_char == settings.COMMENT_INDICATOR[0] and self.equals_symbol(settings.COMMENT_INDICATOR):
                if settings.DEBUG:
                    print("Generating comment...")

                self.generate_comment(tags)

            elif self.current_char == '"':
                if settings.DEBUG:
                    print("Generating string...")

                tags.append(self.generate_string())

            elif self.current_char == '\n':
                self.advance()

            elif self.current_char in tag_lists.VALID_CHARACTERS:
                tags.append(self.generate_tag())

            else:
                return None

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

        if settings.DEBUG:
            print(f"{id} is {'inline' if inline else 'not inline'}")

        # skip whitespaces
        while self.current_char == ' ':
            self.advance()

        # the content inside of the tag
        content = ''

        if settings.DEBUG:
            print(f'Generating attributes for {id}')

        # the tag's attributes (href, class, etc...)
        attributes = self.generate_attributes()

        if settings.DEBUG:
            print(f'{id}\'s attributes: {attributes}')

        # add content if it isn't inline.
        if not inline:
            if settings.DEBUG:
                print(f'Generating content for {id}')

            content = self.generate_content()

        if not inline or len(attributes) > 0:
            self.advance()

        # return tag object.
        return tag.Tag(id, content, attributes, inline = inline)

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
        # essentially just plain text
        return tag.Tag("str", string, inline = False, formatting = "%content%", no_inner_tags = True)

    def generate_comment(self, tags):
        """
        Generates a comment tag
        :return: A comment tag object
        """
        content = ''

        self.advance()

        # not a new line, and not a null character
        while self.current_char != '\n' and self.current_char != None:
            content += self.current_char
            self.advance()

        self.advance()
        
        if not settings.IGNORE_COMMENTS:
            tags.append(tag.Tag('comment', content, inline = False, formatting = '<!--%content%-->', no_inner_tags = True))
            
    def generate_attributes(self) -> []:
        """
        Generates the attributes of a tag
        :return: A 2D array of attributes - name, and value.
        """
        attributes = []

        # we are adding attributes
        if self.current_char == settings.ATTRIBUTE_LEFT_BRACE:
            self.advance()

            # we haven't hit the end of our attributes
            while self.current_char != settings.ATTRIBUTE_RIGHT_BRACE:
                # whitespace or attribute separator
                if self.current_char in " ,":
                    self.advance()

                # attribute name
                attribute_id = ""
                while not self.current_char in "=":
                    attribute_id += self.current_char
                    self.advance()

                self.advance()

                # attribute value
                value = ""

                # we haven't reached a separator or an ending brace
                while not self.current_char in [',', settings.ATTRIBUTE_RIGHT_BRACE]:
                    value += self.current_char
                    self.advance()

                # add to list
                attributes.append([attribute_id, value])

        return attributes

    def generate_content(self) -> str:
        """
        Generates the content inside of braces.
        :return: The content inside of the braces, as a string.
        """
        content = ''

        # skip to opening brace
        while self.current_char != settings.INNER_LEFT_BRACE:
            if self.current_char == settings.SINGLE_LINE_TAG_INDICATOR[0] and self.equals_symbol(settings.SINGLE_LINE_TAG_INDICATOR):
                return self.generate_single_line_tag()

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
        content = content[1:len(content) - 1]

        return content

    def generate_single_line_tag(self) -> str:
        """
        Generates a single lined tag
        :return: The content
        """

        content = ''

        while self.current_char != None and self.current_char != '\n':
            # add char to content
            content += self.current_char
            self.advance()

        return content

    def equals_symbol(self, symbol: str) -> bool:
        """
        Checks if the forecoming text equals the given symbol
        :param symbol: The symbol to check against
        :return: Whether the forecoming text is equal to the symbol
        """
        current = ''

        # add char until we reach a whitespace
        while self.current_char != None and self.current_char != ' ':
            current += self.current_char
            self.advance()

        return current == symbol