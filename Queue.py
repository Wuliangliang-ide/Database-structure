class Queue:
    def __init__(self, l=[]):
        self.l = l

    def __iter__(self):
        return iter(self.l)

    def __repr__(self):
        return str(self.l)

    def enqueue(self, item):
        self.l.insert(0, item)

    def dequeue(self):
        return self.l.pop()

    def isEmpty(self):
        return self.l == []

    def size(self):
        return len(self.l)
