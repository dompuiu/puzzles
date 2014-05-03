class Empty(Exception):
    pass

class LinkedList:

    class _Node:
        __slots__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

        def get_element(self):
            return self._element

        def get_next(self):
            return self._next

    def __init__(self):
        self.__head = None
        self.__size = 0

    def is_empty(self):
        return self.__size == 0

    def __len__(self):
        return self.__size

    def add_first(self, e):
        self.__head = self._Node(e, self.__head)
        self.__size += 1

        return self.__head

    def get_first(self):
        if self.is_empty():
            raise Empty("List is empty")

        return self.__head

    def find(self, v):
        if self.is_empty():
            raise Empty("List is empty")

        n, pn = self.__find_nodes_by_value(v)

        return n

    def contains(self, v):
        return self.find(v) is not None

    def remove(self, v):
        if self.is_empty():
            raise Empty("List is empty")

        n, pn = self.__find_nodes_by_value(v)

        if not n:
            return False

        if n == self.get_first():
            self.__head = n.get_next()

        if pn:
            pn._next = n.get_next()

        self.__size -= 1

        return True

    def get_elements(self):
        n = self.__head

        while n:
            yield n.get_element()
            n = n.get_next()


    def __find_nodes_by_value(self, v):
        n = self.__head
        pn = None

        while n:
            if n.get_element() == v:
                return n, pn

            pn = n
            n = n.get_next()

        return None, None