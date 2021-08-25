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


class UnorderList:

    def __init__(self):
        """
        初始化无序列表，空表表头数据为None
        """
        self.head = None  # 表头数据为None
        self.l = []

    def __repr__(self):
        return str(self.l)

    def isEmpty(self):
        """

        :return: 空为True，否则为False
        """
        return self.head == None

    def add(self, item):
        """
        add方法将链表(无序列表)当前节点设置为item，当前节点指针设置为None
        :param item: 所添加的数据
        """
        temp = Node(item)  # 创建一个节点实例
        temp.setNext(self.head)  # 当前节点指针的设置
        self.head = temp  # 设置当前节点
        self.l.append(self.head)

    def size(self):
        """
        遍历所有节点，累加count
        :return: 无序列表的大小
        """
        # count = 0
        # node = self.head
        # while node != None:
        #     count += 1
        #     node = node.getNext()
        return len(self.l)

    def search(self, item):
        """
        遍历链表所有节点，直到找到或下一个节点为None
        :param item: 需被查找的值
        :return: 找到返回True， 否则False
        """
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found

    def remove(self, item):
        current = self.head  # 当前节点,永远在第一位
        rear = None  # rear指向current后面的节点
        found = False

        while not found:
            if current.getData() == item:
                found = True
            else:
                rear = current
                current = current.getNext()
            if current == None:
                raise ValueError("未能找到该元素!")
        if rear == None:  # 如果要删除的元素在表头
            self.head = current.getNext()
        else:
            rear.setNext(current.getNext())

    def pop(self, index):
        size = self.size()
        if -1 < index < size:
            self.head = self.l[index - size]
            current_value = self.l.pop(index).getData()
        elif -size <= index < 0:
            self.head = self.l[size + index]
            current_value = self.l.pop(index).getData()
        else:
            raise IndexError("索引越界")
        return current_value

    def __getitem__(self, item):
        return self.l[item].getData()
