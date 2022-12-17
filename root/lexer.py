import tag
import position
import tag_lists
import settings
import os

class Lexer:
    def __init__(self, markup, name = "", path = ""):
        self.markup = markup
        self.name = name
        self.path = path

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

            tags.append(tag.Tag(self, "str", self.markup, inline = False, formatting ="%content%", no_inner_tags = True))
            
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
                tag = self.generate_tag()

                if tag != None:
                    tags.append(tag)

            else:
                print(f"Invalid char detected: '{self.current_char}'")
                quit(-1)

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

        if id == 'css':
            return self.generate_css()

        forced_void = self.current_char == '*'

        # check if element is inline (doesn't need a closing tag)
        inline = id in tag_lists.INLINE_ELEMENTS

        if settings.DEBUG:
            print(f"{id} is {'inline' if inline else 'not inline'}")

        self.skip_whitespaces()

        # the content inside of the tag
        content = ''

        if settings.DEBUG:
            print(f'Generating attributes for {id}')

        # the tag's attributes (href, class, etc...)
        attributes = self.generate_attributes()

        if settings.DEBUG:
            print(f'{id}\'s attributes: {attributes}')

        # add content if it isn't inline.
        if not inline and not forced_void:
            if settings.DEBUG:
                print(f'Generating content for {id}')

            content = self.generate_content()

            self.advance()

            self.skip_whitespaces()

            if self.equals_symbol(settings.STYLE_SEPARATOR):
                self.skip_until(settings.STYLE_LEFT_BRACE)
                attributes.append(['style', f'"{self.generate_content_inside(settings.STYLE_LEFT_BRACE, settings.STYLE_RIGHT_BRACE).strip()}"'])

        if not inline or len(attributes) > 0:
            self.advance()

        # return tag object.
        return tag.Tag(self, id, content, attributes, inline=inline)

    def generate_string(self):
        """
        Generates a string. What would be plain text in normal HTML.
        :return: String tag.
        """
        string = ''

        escape_sequences = {
            '"': '"', # avoid cancelling string
            'n': '<br />', # add new line
            'r': '<br />', # return carriage, just for people who might be used to it?
            't': '    ' # tab
        }

        self.advance()

        quotation_marks = 1

        # we want to continue adding to the string
        while self.current_char != None and self.current_char != '"':
            # character wants to enable escape sequence
            if self.current_char == '\\':
                self.advance()

                string += escape_sequences[self.current_char]

            # just add
            else:
                string += self.current_char
                
            self.advance()

        if self.current_char == '"':
            quotation_marks -= 1

        if quotation_marks != 0:
            raise Exception(f"Missing quotation mark")

        self.advance()

        # return the string object
        # essentially just plain text
        return tag.Tag(self, "str", string, inline = False, formatting ="%content%", no_inner_tags = True)

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
            tags.append(
                tag.Tag(self, 'comment', content, inline = False, formatting ='<!--%content%-->', no_inner_tags = True))
            
    def generate_attributes(self) -> []:
        """
        Generates the attributes of a tag
        :return: A 2D array of attributes - name, and value.
        """
        # content inside of braces
        encapsulated_content = self.generate_content_inside(settings.ATTRIBUTE_LEFT_BRACE, settings.ATTRIBUTE_RIGHT_BRACE)

        # the components that we have retrieved from the encapsulated content
        split_components = []

        if encapsulated_content != "":
            split_components = encapsulated_content.split(settings.ATTRIBUTE_SEPARATOR)

            # track index to reassign components
            index = 0
            for component in split_components:
                # strip whitespaces from both ends
                split_components[index] = component.strip()

                index += 1

        attributes = []

        for component in split_components:
            # split by assigner
            split = component.split(settings.ATTRIBUTE_ASSIGNER)

            # if there is only one element in the array, then we add a blank element to serve as the value
            if len(split) == 1:
                split.append("")

            # add to attributes - name, value
            attributes.append([split[0], split[1]])

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
        while self.current_char != None and self.current_char != ' ' and (current + self.current_char) in symbol:
            current += self.current_char
            self.advance()

        return current == symbol

    def generate_content_inside(self, symbol_one: str, symbol_two: str) -> str:
        """
        Gets the content inside of two given symbols
        :param symbol_one: The opening symbol
        :param symbol_two: The closing symbol
        :return: The content inside of the two given symbols
        """
        encapsulated_content = ""

        if self.current_char == symbol_one:
            stack = 1

            self.advance()

            while stack != 0:
                if self.current_char == symbol_one:
                    stack += 1
                elif self.current_char == symbol_two:
                    stack -= 1

                encapsulated_content += self.current_char
                self.advance()

            self.advance()

        return encapsulated_content[:-1]

    def skip_whitespaces(self):
        """
        Skips characters until we meet a non-whitespace character
        """
        while self.current_char == ' ':
            self.advance()

    def skip_until(self, symbol: str):
        """
        Skips characters until we reach the given symbol
        :param symbol: The symbol to break at
        """
        while self.current_char != symbol:
            self.advance()

    def generate_css(self):
        if settings.DEBUG:
            print("Generating CSS")

        self.skip_whitespaces()
        attributes = self.generate_attributes()

        file_name = os.path.splitext(os.path.basename(self.path))[0]
        file_extension = os.path.splitext(os.path.basename(self.path))[1]

        has_name_attribute = len(list(filter(lambda array: array[0] == 'name', attributes))) > 0
        name_attribute = ''

        if has_name_attribute:
            name_attribute = list(filter(lambda array: array[0] == 'name', attributes))[0][1].replace('"', '') + '.css'

        name = name_attribute if has_name_attribute else f"{self.path.replace(os.path.dirname(self.path), '').replace(file_extension, '')}.style.css"

        content = self.generate_content()
        self.advance()

        with open(f"{os.path.dirname(self.path)}/{name}", 'w') as file:
            file.write(content)
            file.close()

        return tag.Tag(self, 'link', '', [['rel', '"stylesheet"'], ['href', f'"{name.removeprefix("/")}"']], inline=True)
