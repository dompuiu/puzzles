from src.gangster import Gangster, GangsterStatus


class MafiaOrganization:
    def __init__(self, big_boss):
        if not isinstance(big_boss, Gangster):
            raise Exception("Only a gangster can become a mafia organization boss")

        big_boss.organization = self
        self.big_boss = big_boss


    def find_by_name(self, name):
        for gangster in self.__preorder_traversal(self.big_boss):
            if gangster.name == name:
                return gangster

        return None

    def add_under(self, boss, gangster):
        if not isinstance(boss, Gangster) or not isinstance(gangster, Gangster):
            raise Exception("Only gangsters can be added to the organization")

        if boss.organization != self:
            raise Exception("The boss gangster is not a member of this organization")

        gangster.organization = self
        boss.add_subordinate(gangster)

    def __preorder_traversal(self, gangster):
        yield gangster

        for subordinate in gangster.subordinates():
            for subordinate_gangster in self.__preorder_traversal(subordinate):
                yield subordinate_gangster