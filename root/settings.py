INNER_LEFT_BRACE = '{'
INNER_RIGHT_BRACE = '}'

ATTRIBUTE_LEFT_BRACE = '('
ATTRIBUTE_RIGHT_BRACE = ')'
ATTRIBUTE_SEPARATOR = ','
ATTRIBUTE_ASSIGNER = '='

STYLE_SEPARATOR = '->'
STYLE_LEFT_BRACE = '{'
STYLE_RIGHT_BRACE = '}'

COMMENT_INDICATOR = '~'

# Completely disregards comments - does not add them to the HTML output
IGNORE_COMMENTS = True

# The indicator for a single line tag
# E.G.
# a [href="link"] -> "Anchor text"
SINGLE_LINE_TAG_INDICATOR = '->'

# Whether to output messages about what the parser is currently doing
DEBUG = False

# Add new lines on the final output
NEW_LINE_OUTPUT = True

# Forces the given tag to not have any inner tags
# E.G.
# p*
FORCE_NO_INNER_TAGS = '*'