class Vertex:
    '''
    图中的顶点
    '''
    def __init__(self, name):
        '''
        :param name: 顶点的名字
        '''
        self.name = name
        self.connectedto = {}  # k = Vertex,v = weight

        self.precursor = []  # 作为有权重的顶点使用
        self.successor = []  # 作为有权重的顶点使用

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return '{' + '{}:{}'.format('name', self.name) + '}'

    def hasPrecursor(self):
        '''
        :return: 有前驱返回True，否则False
        '''
        return self.precursor != []

    def hasSuccessor(self):
        '''
        :return: 有后继返回True，否则False
        '''
        return self.successor != []

    def setPreWeight(self, PreVertex, weight):
        '''
        :param PreVertex: 前驱顶点
        :param weight: 权重
        :return: None

        设置前驱的权重
        '''
        if isinstance(PreVertex, Vertex):
            for Pv in self.precursor:
                if Pv == PreVertex:
                    Pv.connectedto[self] = weight
        else:
            raise TypeError('PreVertex必须是类Vertex')

    def isPrecursor(self, vertex):
        '''
        :param vertex: 顶点
        :return: 如果vertex是self的前驱返回True，否则False

        vertex是否为self的前驱
        '''

        return vertex in self.precursor

    def isSuccessor(self, vertex):
        '''
        :param vertex: 顶点
        :return: 如果vertex是self的后继返回True，否则False

        vertex是否为self的后继
        '''

        return vertex in self.successor

    def addVertex(self, vertex, weight):
        '''
        :param vertex:
        :param weight:
        :return:

        添加相邻顶点
        '''
        if isinstance(vertex, Vertex):
            self.connectedto[vertex] = weight
        else:
            ver = Vertex(vertex)
            self.connectedto[ver] = weight


class Graph:
    def __init__(self):
        self.verDict = {}  # k = Vertex, v = 存放后继们的列表

    def addVertex(self, vertexname):
        '''
        :param vertexname: 顶点名字
        :return: Vertex
        '''
        if isinstance(vertexname, Vertex):
            self.verDict[vertexname] = [succ for succ in vertexname.connectedto]
            return vertexname
        else:
            vertex = Vertex(vertexname)
            self.verDict[vertex] = [succ for succ in vertex.connectedto]
            return vertex

    def addEdge(self, firstVer: Vertex, lastVer: Vertex, weight):
        '''
        :param firstVer: 顶点1
        :param lastVer: 顶点2
        :param weight: 权重
        :return: None

        添加边
        '''

        if isinstance(firstVer, Vertex) and isinstance(lastVer, Vertex) and (
                isinstance(weight, int) or isinstance(weight, float)):
            firstVer.connectedto[lastVer] = weight
            firstVer.successor.append(lastVer)
            lastVer.precursor.append(firstVer)

            for ver in self.verDict:
                if ver.name == firstVer.name:
                    self.verDict[ver].append(lastVer)
        else:
            raise TypeError('firstVer和lastVer必须为类Vertex,且权重为数字')

    def addDoubleEdge(self, firstVer: Vertex, lastVer: Vertex, weight=None):
        '''
        :param firstVer: 顶点1
        :param lastVer: 顶点2
        :param weight: 数字
        :return: None

        设置firstVer到lastVer和lastVer到firstVer的权重
        '''
        if isinstance(firstVer, Vertex) and isinstance(lastVer, Vertex) and weight == None:
            firstVer.connectedto[lastVer] = weight
            lastVer.connectedto[firstVer] = weight

            for ver in self.verDict:
                if ver.name == firstVer.name:
                    self.verDict[ver].append(lastVer)
                if ver.name == lastVer.name:
                    self.verDict[ver].append(firstVer)

        elif isinstance(firstVer, Vertex) and isinstance(lastVer, Vertex) and (
                isinstance(weight, int) or isinstance(weight, float)):
            firstVer.connectedto[lastVer] = weight
            firstVer.successor.append(lastVer)
            firstVer.precursor.append(lastVer)
            lastVer.connectedto[firstVer] = weight
            lastVer.precursor.append(firstVer)
            lastVer.successor.append(firstVer)

            for ver in self.verDict:
                if ver.name == firstVer.name:
                    self.verDict[ver].append(lastVer)
                if ver.name == lastVer.name:
                    self.verDict[ver].append(firstVer)
        else:
            raise TypeError('firstVer和lastVer必须为类Vertex')

    def removeEdge(self, vertex1: Vertex, vertex2: Vertex):
        '''
        :param vertex1: vertex2的前驱
        :param vertex2: vertex1的后继
        :return: None

        移除边
        '''
        if isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex):
            try:
                vertex1.successor.remove(vertex2)  # 删除vertex1的后继列表
                del vertex1.connectedto[vertex2]  # 删除vertex1的后继字典
                self.verDict[vertex1].remove(vertex2)  # 删除Graph中顶点列表
                vertex2.precursor.remove(vertex1)  # 删除vertex2的前驱
            except ValueError:
                raise ValueError("vertex2不是vertex1后继")
            except KeyError:
                raise KeyError("vertex2不是vertex1后继")

        else:
            raise TypeError('参数vertex1和vertex2必须是Vertex的实例')

    def getVertex(self, vertex) -> Vertex:
        if not isinstance(vertex, Vertex):
            for ver in self.verDict:
                if ver.name == vertex:
                    return ver

    def DFS(self, start: Vertex):
        '''
        :param start: 开始的顶点
        :return: 返回遍历顺序的顶点列表
        '''
        stack = []  # 栈
        seen = set()  # 作为一个清单，检查入队的顶点
        vers = []  # 返回的数据列表

        stack.append(start)
        seen.add(start)

        while stack:
            vertex = stack.pop()
            for ver in self.verDict[vertex]:
                if ver not in seen:
                    stack.append(ver)
                    seen.add(ver)
            vers.append(vertex)
        return vers

    def BFS(self, start: Vertex) -> list:
        '''
        :param start: 开始的顶点
        :return: 返回遍历顺序的顶点列表
        '''

        data = []  # 返回的数据列表
        queue = []  # 队列
        seen = set()  # 作为一个清单，检查入队的顶点
        vertexes = self.verDict  # 字典，key为顶点，value为key的后续顶点

        queue.append(start)
        seen.add(start)

        while queue:
            rmVer = queue.pop(0)
            data.append(rmVer)  # 将每次被弹出的顶点入队
            for ver in vertexes[rmVer]:  # 遍历被弹出的顶点的后续顶点
                if ver not in seen:  # 如果后继顶点不在清单中
                    queue.append(ver)  # 将这些元素入队并加入清单
                    seen.add(ver)
        return data

    def Topological(self):
        import copy
        data = []
        this = copy.deepcopy(self)
        verDict = this.verDict
        while verDict:
            for vertex in verDict:
                if not vertex.hasPrecursor():
                    data.append(this.removeVertex(vertex))
                    break
        return data

    def removeVertex(self, vertex: Vertex):
        if isinstance(vertex, Vertex):
            if vertex.hasSuccessor() and vertex.hasPrecursor():
                for pre in vertex.precursor:
                    pre.successor.remove(vertex)  # 1.删除前驱表中顶点关于vertex的信息
                    self.verDict[pre].remove(vertex)
                    del pre.connectedto[vertex]

                for suc in vertex.successor:  # 2.删除后继表中顶点关于vertex的信息
                    suc.precursor.remove(vertex)

                vertex.successor = []  # 3.清空后继表
                vertex.precursor = []  # 4.清空前驱表
                vertex.connectedto = {}  # 5.清空连接字典
                del self.verDict[vertex]


            elif vertex.hasPrecursor():  # 有前驱,无后继
                for pre in vertex.precursor:  # 删除前驱表中顶点关于vertex的信息
                    pre.successor.remove(vertex)  #
                    self.verDict[pre].remove(vertex)
                    del pre.connectedto[vertex]
                vertex.precursor = []
                del self.verDict[vertex]


            elif vertex.hasSuccessor():  # 无前驱,有后继
                for suc in vertex.successor:  # 2.删除后继表中顶点关于vertex的信息
                    suc.precursor.remove(vertex)
                vertex.successor = []
                vertex.connectedto = {}
                del self.verDict[vertex]

            else:
                del self.verDict[vertex]

            return vertex
        else:
            raise TypeError('参数vertex必须是Vertex的实例')

    def isPrecursor(self, vertex1: Vertex, vertex2: Vertex):
        '''
        :param vertex1:顶点1
        :param vertex2:顶点2
        :return:如果顶点1是顶点2的前驱，返回True，否则False

        vertex1是否为vertex2的前驱
        '''

        return vertex1 in vertex2.precursor

    def isSuccessor(self, vertex1: Vertex, vertex2: Vertex):
        '''
        :param vertex1:顶点1
        :param vertex2:顶点2
        :return:如果顶点1是顶点2的后继，返回True，否则False

        vertex1是否为vertex2的后继
        '''

        return vertex1 in vertex2.successor

    def getWeigt(self, vertex1: Vertex, vertex2: Vertex):
        '''
        :param vertex1: 顶点1
        :param vertex2: 顶点2
        :return: 权重

        返回vertex1到vertex2的权重
        '''
        if isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex):
            if self.hasWeight(vertex1, vertex2):
                return vertex1.connectedto[vertex2]
            else:
                return None
        else:
            raise TypeError('参数vertex1和vertex2必须是Vertex的实例')

    def hasWeight(self, vertex1: Vertex, vertex2: Vertex):
        '''
        :param vertex1: 顶点1
        :param vertex2: 顶点2
        :return: 如果有权重返回True，否则False
        '''
        flag = False
        try:
            weight = vertex1.connectedto[vertex2]
            if weight:
                flag = True
        except:
            flag = False
        return flag

    def modifyWeight(self, vertex1: Vertex, vertex2: Vertex, weight):
        if isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex):
            if self.hasWeight(vertex1, vertex2):
                if not weight:
                    vertex1.successor.remove(vertex2)  # 1
                    vertex2.precursor.remove(vertex1)  # 2
                    del vertex1.connectedto[vertex2]
                    self.verDict[vertex1].remove(vertex2)

                else:
                    vertex1.connectedto[vertex2] = weight  # 3
            else:
                if not weight:
                    if not (vertex2 in self.verDict[vertex1] and vertex1 in self.verDict[vertex2]):
                        raise ValueError('vertex1和vertex2间没有权重')
                else:
                    vertex1.connectedto[vertex2] = weight  # 3
                    vertex1.successor.append(vertex2)
                    vertex2.precursor.append(vertex1)
                    self.verDict[vertex2].remove(vertex1)
                    if vertex2.connectedto[vertex1] == None:
                        del vertex2.connectedto[vertex1]
        else:
            raise TypeError('参数vertex1和vertex2必须是Vertex的实例')
