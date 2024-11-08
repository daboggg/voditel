class Proba:
    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c

    def __str__(self) -> str:
        return f'{self.a}-{self.b}-{self.c}'



ll = [
    Proba(1, 2, 3),
    Proba(1, 20, 33),
    Proba(2, 50, 60),
    Proba(2, 96, 58),
    Proba(3, 200, 300),
    Proba(3, 159, 423),
]

a = None

aa = []
bb = []

for idx, l in enumerate(ll):
    if not a or a == l.a:
        a = l.a
        bb.append(l)
        if idx+1 == len(ll):
            aa.append(bb.copy())
    else:
        aa.append(bb.copy())
        bb.clear()
        bb.append(l)
        a = l.a

for a in aa:
    for x in a:
        print(x)

