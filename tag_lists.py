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

VALID_CHARACTERS = string.ascii_letters + '0123456789'