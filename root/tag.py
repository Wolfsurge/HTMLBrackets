import settings
import lexer

class Tag:
    def __init__(self, name, content, line: int, attributes = [], inline = False, formatting = None, no_inner_tags = False):
        self.name = name
        self.content = content
        self.attributes = attributes
        self.inline = inline
        self.formatting = formatting
        self.no_inner_tags = no_inner_tags
        self.inner_tags = []
        
        # only generate tags if we want to have inner tags.
        # this is because comments and other elements also use this tag system,
        # but they obviously can't have inner elements.
        if not self.no_inner_tags:
            self.inner_tags = lexer.Lexer(content, name, line=line).make_tags()

            if self.inner_tags == None:
                self.inner_tags = []
            elif settings.DEBUG:
                tags = []

                for tag in self.inner_tags:
                    tags.append(tag.name)

                print(f'{name}\'s tags: {tags}')

    def generate_html(self) -> str:
        """
        Generates the required HTML tags for this element.
        :return: The HTML tags and a new line character
        """
        final = ''

        # we don't want to override formatting this
        if not self.formatting:
            # element name
            final = f'<{self.name}'

            # add properties (href, class, etc...)
            for property in self.attributes:
                final += f" {property[0].strip()}={property[1].strip()}"

            # add closing arrow
            final += f'{ "/" if self.inline else "" }>'

            # add optional new lines if the tag is NOT inline
            if settings.NEW_LINE_OUTPUT and not self.inline:
                final += '\n'

            # generate inner html tags
            for t in self.inner_tags:
                final += t.generate_html()

            # add closing tag if it isn't an inline element
            if not self.inline:
                final += f'</{self.name}>'
        else:
            # add tag with our custom formatting
            final += self.formatting.replace('%name%', self.name).replace('%content%', self.content)

        # add optional new lines
        return final + ('\n' if settings.NEW_LINE_OUTPUT else '')