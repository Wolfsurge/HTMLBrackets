import tag_generator

class Tag:
    def __init__(self, name, content, properties = [], inline = False, formatting = None, no_inner_tags = False):
        self.name = name
        self.content = content
        self.properties = properties
        self.inline = inline
        self.formatting = formatting
        self.no_inner_tags = no_inner_tags

        # only generate tags if we want to have inner tags.
        # this is because comments and other elements also use this tag system,
        # but they obviously can't have inner elements.
        if not self.no_inner_tags:
            self.inner_tags = tag_generator.TagGenerator(name, content).make_tags()

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
            for property in self.properties:
                final += f" {property[0].strip()}={property[1].strip()}"

            # add closing arrow
            final += f'{ "/" if self.inline else "" }>'

            # generate inner html tags
            for t in self.inner_tags:
                final += t.generate_html()

            # add closing tag if it isn't an inline element
            if not self.inline:
                final += f'</{self.name}>'
        else:
            # add tag with our custom formatting
            final += self.formatting.replace('%name%', self.name).replace('%content%', self.content)

        # return with a new line
        return final + "\n"