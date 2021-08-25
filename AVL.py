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

class AVL(BinarySearchTree):

    def rebalance(self, node: TreeNode):
        if node.balanceFactor < 0:  # 右重需要左旋
            if node.rightChild.balanceFactor > 0:  # 右子节点左重先右旋
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:  # 单个左旋
                self.rotateLeft(node)
        elif node.balanceFactor > 0:  # 左重需要右旋
            if node.leftChild.balanceFactor < 0:  # 左子节点右重先左旋
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:  # 单个右旋
                self.rotateRight(node)

    def updateBalance(self, node: TreeNode):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1
            if node.parent.balanceFactor != 0:
                self.updateBalance((node.parent))

    def rotateRight(self, rotRoot: TreeNode):
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot

    def rotateLeft(self, rotRoot: TreeNode):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot

        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - \
                                min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + \
                                max(rotRoot.balanceFactor, 0)

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
                self.updateBalance(currentNode.leftChild)
        else:
            if currentNode.hasRightChild():  # 如果有右节点，递归调用_put方法，将右节点设置为当前节点，否则设置右节点
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.rightChild)
