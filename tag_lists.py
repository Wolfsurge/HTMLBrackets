import string

# elements that cannot have inner tags
INLINE_ELEMENTS = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr"
]

# elements that have a body, but NOT tags
TAG_EXCLUDED_ELEMENTS = [
    "script"
]

VALID_CHARACTERS = string.ascii_letters + '0123456789'