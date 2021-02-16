from dataclasses import dataclass, field
from typing import List, Optional

from parser import Grama, make_rules
from lex import extract_tokens


class Item:
    pass


@dataclass
class Person:
    name: str
    height: Optional[int] = None
    items: List[Item] = field(default_factory=list)


@dataclass
class Pet(Item):
    name: str


@dataclass
class Money(Item):
    kind: str
    value: int


def eval(data):
    people = {}
    for obj in data:
        name = obj["name"]
        person = Person(name=name)
        for raw_item in obj["items"]:
            eval_item(people, person, raw_item)
        people[name] = person
    return people


def eval_item(people, person, raw_item):
    type_item = raw_item["type"]
    if type_item == "height":
        height = float(raw_item["value"])
        if raw_item["unit"] == "cm":
            height /= 100.0
        person.height = height
    elif type_item == "money":
        person.items.append(
            Money(
                kind=raw_item["kind"],
                value=raw_item["value"],
            )
        )
    elif type_item == "pet":
        person.items.append(
            Pet(name=raw_item["name"])
        )
    elif type_item == "lend":
        guy_name = raw_item["name"]
        that_guy = people.get(guy_name, None)
        if that_guy is None:
            raise ValueError(f"guy {guy_name} doesnt exist")
        person.items += that_guy.items
    else:
        raise ValueError("wrong item type")


if __name__ == "__main__":
    import pprint
    from sys import argv

    grama = Grama(start="sentences", rules=make_rules())
    filename = "data.txt" if len(argv) < 2 else argv[1]

    with open("data.txt") as file:
        data = file.read()

    lex = extract_tokens(data)
    items = grama.run(lex)
    people = eval(items)

    for person in people.values():
        print(person.name, "height =", person.height, "items =", end=" ")
        pprint.pp(person.items)
