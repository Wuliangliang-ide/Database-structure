class Stack:
    def __init__(self):
        self.l = []
        self.counter = -1

    def __iter__(self):
        return iter(self.l)

    def __getitem__(self, item):
        if item >= len(self.l):
            raise StopIteration('Stop')
        return self.l[item]

    def __len__(self):
        return len(self.l)

    def __index__(self, ind):
        return self.l[ind]

    def __repr__(self):
        return str(self.l)

    def isEmpty(self):
        return self.l == []

    def len(self):
        return len(self.l)

    def append(self, a):
        self.l.append(a)

    def pop(self):
        return self.l.pop()

    def peek(self):
        return self.l[-1]
