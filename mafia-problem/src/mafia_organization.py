from src.gangster import Gangster, GangsterStatus, GangsterLocation, SameGangsterException


class MafiaOrganization:
    def __init__(self, big_boss):
        if not isinstance(big_boss, Gangster):
            raise Exception("Only a gangster can become a mafia organization boss")

        self.set_big_boss(big_boss)

    def set_big_boss(self, big_boss):
        big_boss.organization = self
        self.__big_boss = big_boss

    def get_big_boss(self):
        return self.__big_boss

    def find_by_name(self, name):
        for gangster in self.__preorder_traversal(self.__big_boss):
            if gangster.name == name:
                return gangster

        return None

    def add_under(self, boss, gangster):
        if not isinstance(boss, Gangster) or not isinstance(gangster, Gangster):
            raise Exception("Only gangsters can be added to the organization")

        if gangster == boss:
            raise SameGangsterException("You cannot add a gangster as subordinate of itself")

        if not self.is_member_of_organization(boss.name) or not self.__check_organization_attribute(boss):
            raise Exception("The boss gangster is not a member of this organization")

        if self.is_member_of_organization(gangster.name):
            raise Exception("The gangster is already a member of the organization")

        gangster.organization = self
        boss.add_subordinate(gangster)

    def members_count(self):
        counter = 0
        for gangster in self.__preorder_traversal(self.__big_boss):
            counter += 1

        return counter

    def is_member_of_organization(self, name):
        gangster = self.find_by_name(name)
        return bool(gangster) and gangster.status != GangsterStatus.INJAIL

    def kill_member(self, name):
        gangster = self.find_by_name(name)

        if not gangster:
            return False

        new_substitute_boss = self.__find_substitute_boss(gangster)
        gangster_boss = gangster.get_boss()
        if gangster_boss:
            if new_substitute_boss.get_boss() is not gangster_boss:
                gangster_boss.add_subordinate(new_substitute_boss)
            gangster_boss.delete_subordinate(gangster)
        else:
            self.set_big_boss(new_substitute_boss)
            new_substitute_boss.set_boss(None)

        self.__set_subordinates_attribute(gangster, {"location": GangsterLocation.UNKNOWN})
        self.__move_subordinates_to_new_boss(gangster, new_substitute_boss)

        return True

    def send_member_to_jail(self, name):
        gangster = self.find_by_name(name)

        if not gangster:
            return False

        new_substitute_boss = self.__find_substitute_boss(gangster)
        gangster_boss = gangster.get_boss()
        if gangster_boss and new_substitute_boss.get_boss() is not gangster_boss:
            gangster_boss.add_subordinate(new_substitute_boss)

        self.__set_subordinates_attribute(gangster, {"boss_in_jail": gangster})
        self.__move_subordinates_to_new_boss(gangster, new_substitute_boss)

        gangster.status = GangsterStatus.INJAIL

        return True

    def set_member_to_freedom(self, name):
        gangster = self.find_by_name(name)

        if not gangster:
            return False

        gangster.status = GangsterStatus.FREE
        self.__restore_subordinates_previous_boss(gangster)

        return True

    def __preorder_traversal(self, gangster):
        yield gangster

        for subordinate in gangster.subordinates():
            for subordinate_gangster in self.__preorder_traversal(subordinate):
                yield subordinate_gangster

    def __find_substitute_boss(self, gangster):
        new_substitute_boss = self.__find_oldest_member(gangster.get_boss(), gangster) \
            or self.__find_oldest_member(gangster)

        if not new_substitute_boss:
            raise Exception("Cannot find a substitute boss")

        return new_substitute_boss

    def __find_oldest_member(self, boss, ignore_member=None):
        max_age = 0
        oldest_member = None

        if boss:
            for gangster in boss.subordinates():
                if ignore_member == gangster:
                    continue

                if gangster.age > max_age:
                    max_age = gangster.age
                    oldest_member = gangster

        return oldest_member

    def __check_organization_attribute(self, gangster):
        return gangster.organization and gangster.organization == self

    def __move_subordinates_to_new_boss(self, gangster, new_substitute_boss):
        for subordinate in gangster.subordinates():
            gangster.delete_subordinate(subordinate)

            if new_substitute_boss != subordinate:
                self.add_under(new_substitute_boss, subordinate)

    def __set_subordinates_attribute(self, gangster, attributes):
        for subordinate in gangster.subordinates():
            for key in attributes.keys():
                setattr(subordinate, key, attributes[key])

    def __restore_subordinates_previous_boss(self, gangster):
        for g in self.__preorder_traversal(self.__big_boss):
            if getattr(g, 'boss_in_jail', None) == gangster:
                current_boss = g.get_boss()
                if not current_boss:
                    raise Exception("Cannot find current boss")

                current_boss.delete_subordinate(g)
                self.add_under(gangster, g)

