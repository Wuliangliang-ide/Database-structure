class Node:
    """
    节点分为两部分，一部分为数据，另外一部分为指向下一个数据的地址，如果下一个数据为空，则为None
    """

    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return str(self.getData())

    def getData(self):
        """
        :return: 得到当前节点数据
        """
        return self.data

    def getNext(self):
        """
        :return: 得到下一个节点数据
        """
        return self.next

    def setData(self, data):
        """
        :param data: 你想要设置的数据
        """
        self.data = data

    def setNext(self, next):
        """
        :param next: 下一个节点的数据
        """
        self.next = next

class OrderList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def search(self, item):
        currend = self.head
        found = False
        stop = False
        while currend != None and not found and not stop:
            if currend.getData() == item:
                found = True
            elif currend.getData() > item:
                stop = True
            else:
                currend = currend.getNext()
        return found

    def add(self, item):
        current = self.head
        previous = None
        stop = False
        while current != None and not stop:
            if current.getData() > item:
                stop = True
            else:
                previous = current
                current = current.getNext()

        temp = Node(item)
        if previous == None:
            temp.setNext(self.head)
            self.head = temp
        else:
            temp.setNext(current)
            previous.setNext(temp)
