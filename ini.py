def load(fp: str) -> dict:
    with open(fp, "rt") as f:
        data = f.read()

    entries = data.splitlines()
    ret = {}

    for line in entries:
        k, v = line.split("=")
        ret[k] = v

    return ret
