import re

IGNORE_TOKEN = "SPACE"
TOKENS = [
    ("SPACE", r"\s+", str),
    ("NAME", r"[A-Z][a-z]+", str),
    ("INT", r"[0-9]+", int),
    ("MONEY", r"PLN|USD|EUR", str),
    ("HEIGHT", r"(m|cm)\b", str),
    ("OP_HAS", r"has\b", str),
    ("OP_AND", r"and\b|&", str),
    ("OP_ITEMS", r"items\b", str),
    ("OP_PET", r"pet\b", str),
    ("OP_FROM", r"from\b", str),
    ("OP_NOTHING", r"nothing\b", str),
    ("IDENTIFER", r"[a-z]+", str),
    ("END", r"\.", str),
]

TOKENS = [
    (name, re.compile(regex), func)
    for name, regex, func in TOKENS
]

def extract_tokens(data):
    len_data = len(data) - 1
    pos = 0
    lex = []
    while pos < len_data:
        token, pos = find_token(data, pos)
        if token == "ERROR":
            raise ValueError("Syntax Error")
        elif token is not None:
            lex.append(token)
    return lex


def find_token(data, pos):
    for token_name, regex, func in TOKENS:
        match = regex.match(data, pos)
        if match is None:
            continue
        if token_name == IGNORE_TOKEN:
            return None, match.end()
        value = func(match.group(0))
        return (token_name, value), match.end()
    return "ERROR", None


if __name__ == "__main__":
    with open("data.txt") as file:
        data = file.read()
    lex = extract_tokens(data)
    for name, value in lex:
        print(f"{name:12s} {value!r}")
