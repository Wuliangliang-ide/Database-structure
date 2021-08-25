class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.balanceFactor = None

    def __repr__(self):
        return str(self.key) + "的" + str(self.payload)

    def hasLeftChild(self):
        '''
        判断是否有左节点
        :return: 返回左节点，为TreeNode类
        '''
        return self.leftChild

    def hasRightChild(self):
        '''
        判断是否有右节点
        :return: 返回右节点，为TreeNode类
        '''
        return self.rightChild

    def isLeftChild(self) -> bool:
        '''
        判断是否是左节点，依据是：是否有父节点和父节点的左节点是否等于本身
        :return: bool. True if 是左节点 else False
        '''
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        '''
        :return: 有父节点为False，否则为True
        '''
        return not self.parent

    def isLeaf(self):
        '''
        :return: 如果有左节点或者右节点，返回False，否则为True
        '''
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def __iter__(self):
        if self:
            if self.hasLeftChild():
                for elem in self.leftChild:
                    yield elem

            yield self.key

            if self.hasRightChild():
                for elem in self.rightChild:
                    yield elem

    def findSuccessor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            # --------------------------------------------------
            
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.finSuccessor()
                    self.parent.rightChild = self
        # --------------------------------------------------
        return succ

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                # --------------------------------------------------
                
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            # --------------------------------------------------
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent


class BinarySearchTree:
    def __init__(self):

        self.root = None  # 根节点
        self.size = 0  # 节点数量

    def length(self) -> int:
        '''
        返回节点数量
        :return: 节点数量
        '''
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        '''
        枢纽函数 间接调用跟节点的__iter__
        :return: __iter__()
        '''
        return self.root.__iter__()

    def put(self, key: any, val: str):
        '''
        设置节点
        :param key:
        :param val:
        '''
        if self.root:  # 如果有跟节点，则调用_put方法设置节点
            self._put(key, val, self.root)
        else:  # 否则就设置根节点
            self.root = TreeNode(key, val)
        self.size += 1

    def _put(self, key, val, currentNode):
        '''
        设置左右节点
        :param key:
        :param val:
        :param currentNode:
        :return: None
        '''
        if key < currentNode.key:  # 如果比当前节点的键小，则设置左节点，否则设置右节点
            if currentNode.hasLeftChild():  # 如果有左节点，递归调用_put方法，将左节点设置为当前节点，否则设置左节点
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
        else:
            if currentNode.hasRightChild():  # 如果有右节点，递归调用_put方法，将右节点设置为当前节点，否则设置右节点
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)

    def __setitem__(self, key, value):
        return self.put(key, value)

    def get(self, key):
        '''

        :param key:
        :return:
        '''
        if self.root:  # 如果有根节点，则调用_get方法寻找key，否则返回None
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode: TreeNode) -> TreeNode:
        '''
        1.如果当前节点为空，返回None
        2.如果当前节点的键等于查找的键，则返回当前节点的值
        3.如果当前节点的键小于查找键，递归调用_get方法,第二个参数为当前节点的右节点
        4.如果当前节点的键大于于查找键，递归调用_get方法，第二个参数为当前节点的左节点
        :param key:查找键
        :param currentNode: 类型为TreeNode类
        :return: TreeNode
        '''
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, item):
        '''
        利用__getitem__间接调用get方法
        :param item: key
        :return: self.get()
        '''
        return self.get(item)

    def __contains__(self, item):
        if self._get(item, self.root):
            return True
        else:
            return False

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size -= 1
            else:
                raise KeyError('没有该键')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('没有此键')

    def __delitem__(self, key):
        self.delete(key)

    def remove(self, currentNode: TreeNode):

        if currentNode.isLeaf():  # 无左右节点
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():
            succ = currentNode.findSuccessor()

            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload

        elif currentNode.hasLeftChild():  # if有左节点
            if currentNode.isLeftChild():  # 如果currentNode是左节点
                currentNode.leftChild.parent = currentNode.parent
                currentNode.parent.leftChild = currentNode.leftChild
            elif currentNode.isRightChild():  # 如果currentNode是右节点
                currentNode.leftChild.parent = currentNode.parent
                currentNode.parent.rightChild = currentNode.leftChild
            else:  # currentNode为根节点
                currentNode.replaceNodeData(currentNode.leftChild.key,
                                            currentNode.leftChild.payload,
                                            currentNode.leftChild.leftChild,
                                            currentNode.leftChild.rightChild)
        else:  # 否则为currentNode有右节点
            if currentNode.isLeftChild():  # currentNode是左节点
                currentNode.rightChild.parent = currentNode.parent
                currentNode.parent.leftChild = currentNode.rightChild
            elif currentNode.isRightChild():  # currentNode是右节点
                currentNode.rightChild.parent = currentNode.parent
                currentNode.parent.rightChild = currentNode.rightChild
            else:  # currentNode为根节点
                currentNode.replaceNodeData(currentNode.rightChild.key,
                                            currentNode.rightChild.payload,
                                            currentNode.rightChild.leftChild,
                                            currentNode.rightChild.rightChild)

