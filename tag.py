import tag_generator

class Tag:
    def __init__(self, name, content, properties = [], inline = False, formatting = None, no_inner_tags = False):
        self.name = name
        self.content = content
        self.properties = properties
        self.inline = inline
        self.formatting = formatting
        self.no_inner_tags = no_inner_tags

        if not self.no_inner_tags:
            self.inner_tags = tag_generator.TagGenerator(name, content).make_tags()

    def generate_html(self):
        final = ''

        if not self.formatting:
            final = f'<{self.name}'

            for property in self.properties:
                final += f"{ ' ' if not property[0].startswith(' ') else '' }{property[0]}={property[1]}"

            final += f'{ "/" if self.inline else "" }>'

            for t in self.inner_tags:
                final += t.generate_html()

            if not self.inline:
                final += f'</{self.name}>'
        else:
            final += self.formatting.replace('%name%', self.name).replace('%content%', self.content)

        return final + "\n"