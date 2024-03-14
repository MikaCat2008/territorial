class Cell:
    def __init__(self, a: int) -> None:
        self.a = a


s = set()

c1 = Cell(1)
c2 = Cell(2)
c3 = Cell(2)

s.add(c1)
s.add(c2)
s.add(c3)

print(s)
