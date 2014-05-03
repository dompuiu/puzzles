from src.linked_list import LinkedList
from enum import Enum

GangsterLocation = Enum('GangsterLocation', 'UNKNOWN')
GangsterStatus = Enum('GangsterStatus', 'FREE INJAIL')


class Gangster:
    def __init__(self, name, age, location=None):
        if not isinstance(age, int):
            raise Exception("Age can be only a integer")

        self.name = name
        self.age = age

        self.status = GangsterStatus.FREE
        self.location = location or GangsterLocation.UNKNOWN

        self.__boss = None
        self.__subordinates = LinkedList()

    def subordinates_count(self):
        return len(self.__subordinates)

    def add_subordinate(self, gangster):
        if not isinstance(gangster, Gangster):
            raise Exception("You can add only Gangsters as subordinates")

        gangster.set_boss(self)
        return self.__subordinates.add_first(gangster)

    def subordinates(self):
        return self.__subordinates.get_elements()

    def set_boss(self, gangster):
        if not isinstance(gangster, Gangster):
            raise Exception("You can add only Gangsters as bosses")

        self.__boss = gangster

        return True

    def get_boss(self):
        return self.__boss

    def has_boss(self):
        return self.__boss is not None
