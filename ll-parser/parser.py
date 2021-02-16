from lex import extract_tokens


def make_rules():
    return [
        Rule("sentences", nil_array) >> EPS,
        Rule("sentences", concat) >> ["sentence", "sentences"],
        Rule("sentence", make_sentence) >> ["NAME", "OP_HAS", "items", "END"],

        Rule("items", nil_array) >> ["OP_NOTHING"],
        Rule("items", concat) >> ["item", "and_items"],

        Rule("and_items", nil_array) >> EPS,
        Rule("and_items", lambda _, i: i) >> ["OP_AND", "items"],

        Rule("item", make_pet) >> ["OP_PET", "IDENTIFER"],
        Rule("item", make_lend) >> ["OP_ITEMS", "OP_FROM", "NAME"],
        Rule("item", make_int) >> ["INT", "int_type"],

        Rule("int_type", make_money) >> ["MONEY"],
        Rule("int_type", make_height) >> ["HEIGHT"],
    ]


class Rule:

    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.value = None

    def __rshift__(self, value):
        self.value = value
        return self

    def __repr__(self):
        return f"{self.name:8s} -> {self.value!r}"


class Eps:

    def __repr__(self):
        return "ε"


class End:

    def __repr__(self):
        return "$"

EPS = Eps()
END = End()


def concat(obj, array):
    return [obj] + array


def nil_array(*objs):
    return []


def make_sentence(name, _1, items, _2):
    return {
        "name": name,
        "items": items,
    }


def make_int(value, obj):
    return {
        "value": value,
        **obj,
    }


def make_pet(_, pet_name):
    return {
        "type": "pet",
        "name": pet_name,
    }


def make_pet(_, pet_name):
    return {
        "type": "pet",
        "name": pet_name,
    }


def make_lend(_1, _2, name):
    return {
        "type": "lend",
        "name": name,
    }


def make_money(kind):
    return {"type": "money", "kind": kind}


def make_height(unit):
    return {"type": "height", "unit": unit}


class Grama:

    def __init__(self, start, rules, debug=False):
        self.start = start
        self.rules = rules
        self.available_rules = set(rule.name for rule in rules)
        self.debug = debug
        self.pos = 0

    def run(self, lex):
        return self.eval(lex, self.start, END)

    def eval(self, lex, rule_name, end):
        current_token, token_value = self.find_current_token(lex)

        for rule in self.find_rule(rule_name):
            if rule.value == EPS:
                if current_token != end:
                    continue
                if self.debug:
                    print("SELECTED RULE", rule, "ON", repr(token_value))
                return rule.func()

            first_value = rule.value[0]
            if (first_value in self.available_rules
                    or first_value == current_token):
                if self.debug:
                    print("SELECTED RULE", rule, "ON", repr(token_value))
                return self.iterate_rule(lex, rule, end)

        raise ValueError("Syntax error, Not found any rule "
                         f"for token {current_token} for rule {rule_name}")

    def find_current_token(self, lex):
        try:
            return lex[self.pos]
        except IndexError:
            return END, None

    def find_rule(self, rule_name):
        for rule in self.rules:
            if rule.name == rule_name:
                yield rule

    def iterate_rule(self, lex, rule, end):
        data = []
        for next_i, symbol in enumerate(rule.value, start=1):
            end = self.find_end_symbol(rule, next_i, end)

            if symbol in self.available_rules:
                obj = self.eval(lex, symbol, end)
                data.append(obj)
                continue

            try:
                token_name, token_value = lex[self.pos]
            except IndexError:
                raise ValueError("Syntax Error")

            if symbol == token_name:
                if self.debug:
                    print("         RULE", rule.name, "SYMBOL", symbol, "ON", repr(token_value))
                data.append(token_value)
                self.pos += 1
                continue

            raise ValueError(f"Syntax Error, expect {symbol}, got {token_name}")
        return rule.func(*data)

    def find_end_symbol(self, rule, next_i, last_end):
        if next_i >= len(rule.value):
            return last_end

        end_symbol = rule.value[next_i]
        if end_symbol not in self.available_rules:
            return end_symbol
        else:
            return last_end

if __name__ == "__main__":
    import pprint
    from sys import argv

    rules = make_rules()
    print("RULES:")
    pprint.pp(rules)

    grama = Grama(
        start="sentences",
        rules=rules,
        debug=True,
    )

    filename = "data.txt" if len(argv) < 2 else argv[1]

    with open("data.txt") as file:
        data = file.read()

    lex = extract_tokens(data)
    result = grama.run(lex)

    pprint.pp(result)
