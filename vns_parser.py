from parglare import Parser, Grammar
from pprint import pformat


with open("vns-grammar.glr", "rt") as f:
    grammar = Grammar.from_string(f.read())


def flat(a):
    r = []
    for i in a:
        if isinstance(i, list):
            r += flat(i)
        else:
            r.append(a)
    return r.copy()


def parse_color(n):
    return tuple(int(n[1:][i:i+2], 16) for i in (0, 2, 4))


def remove_nones(arr):
    while None in arr:
        arr.remove(None)
    return arr


class Node:
    type = "root"
    data = {}
    nods = ()

    def __init__(self, typ, data, *nods):
        self.type = str(typ)
        self.data = {}
        self.data.update(data)
        self.nods = list(nods).copy()

    def __str__(self):
        nods = "\n".join(tuple(str(i) for i in self.nods))
        nods = nods.replace("\n", "\n    ")
        return """Node <%s>
    %s
%s""" % (self.type, pformat(self.data), nods)

    __repr__ = __str__

    def __getitem__(self, k):
        return self.data[k]


def clear_root(n):
    r = flat(n)
    return r


actions = {
    "root": lambda _, n: remove_nones(clear_root(n))[0],
    "func": lambda _, n: Node("func", {"name": n[0], "body": remove_nones(n[2][0])}),
    "body": lambda _, n: list(n),
    "command": lambda _, n: n[0],
    "sload": lambda _, n: Node("load", {"type": n[1], "path": n[3], "name": n[5]}),
    "loadable": lambda _, n: n[0],
    "sourcable": lambda _, n: n[0],
    "sscene": lambda _, n: Node("scene", {"data": n[1], "effect": n[2]}),
    "scolor": lambda _, n: {"type": "color", "value": n[1] if n[1][0] != "#" else parse_color(n[1])},
    "simage": lambda _, n: {"type": "image", "value": n[1]},
    "effect": lambda _, n: {"type": "effect", "mode": n[1], "duration": n[2] if n[2] is not None else 1.0},
    "sshow": lambda _, n: Node("show", {"data": n[1], "color": n[2], "effect": n[3]}),
    "showable": lambda _, n: n[0],
    "stext": lambda _, n: {"type": "text", "value": n[1]},
    "swait": lambda _, n: Node("wait", {"duration": n[1]}),
    "shide": lambda _, n: Node("hide", {"effect": n[2]}),
    "sreplic": lambda _, n: Node("replic", {"author": None if n[0] is None else n[0][0], "text": ''.join(tuple(n[1]))}),
    "ssave": lambda _, n: Node("nop", {"raw": n.copy()}),
    "sexpr": [
        lambda _, n: n[1],
        lambda _, n: Node("op", {"act": "pow", "ops": (n[0], n[2])}),
        lambda _, n: Node("op", {"act": "mul", "ops": (n[0], n[2])}),
        lambda _, n: Node("op", {"act": "div", "ops": (n[0], n[2])}),
        lambda _, n: Node("op", {"act": "and", "ops": (n[0], n[2])}),
        lambda _, n: Node("op", {"act": "sor", "ops": (n[0], n[2])}),
        lambda _, n: Node("op", {"act": "not", "ops": (n[1],)}),
        lambda _, n: Node("op", {"act": "sub", "ops": (n[0], n[2])}),
        lambda _, n: Node("op", {"act": "add", "ops": (n[0], n[2])}),
        lambda _, n: Node("op", {"act": "neg", "ops": (n[1],)}),
        lambda _, n: n[0],
        lambda _, n: n[0],
        lambda _, n: n[0],
        lambda _, n: n[0],
        lambda _, n: n[0],
    ],
    "sif": lambda _, n: None, # Node("branch", {"type": "if", "expr": n[1], "body": n[3]}),
    "smenu": lambda _, n: None, # nto supported yet
    "tname": lambda _, n: n,
    "tpython": lambda _, n: n[1:][:-1], # Node("tpy", {"value": n[1:][:-1]}),
    "tnum": lambda _, n: eval(n),
    "tcomment": lambda *_: None,
    "tstring": lambda _, n: eval(n)
}

parser = Parser(grammar=grammar, actions=actions)
