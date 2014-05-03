from unittest import TestCase
from mock import Mock

from src.mafia_organization import MafiaOrganization
from src.gangster import Gangster, GangsterLocation, GangsterStatus, SameGangsterException


class TestMafiaOrganization(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)
        self.mog = MafiaOrganization(self.big_boss)

    def test_constructor_accepts_only_a_gangster_as_big_boss(self):
        self.assertRaises(Exception, MafiaOrganization, '__big_boss')

    def test_constructor_creates_new_organization_instance(self):
        self.assertIsInstance(self.mog, MafiaOrganization)

    def test_get_big_boss_return_the_correct_big_boss(self):
        self.assertEquals(self.mog.get_big_boss(), self.big_boss)

    def test_set_big_boss_sets_correct_big_boss(self):
        big_boss2 = Gangster('Big Boss 2', 22)
        self.mog.set_big_boss(big_boss2)

        self.assertEquals(self.mog.get_big_boss(), big_boss2)

    def test_set_big_boss_sets_correct_big_boss_organization(self):
        self.assertEquals(self.mog.get_big_boss().organization, self.mog)


class TestMafiaOrganizationFindByName(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)
        self.mog = MafiaOrganization(self.big_boss)

    def test_find_by_name_search_for_big_boss(self):
        self.assertEquals(self.mog.find_by_name('Big Boss'), self.big_boss)

    def test_find_by_name_search_for_big_boss_subordinate(self):
        g1 = Gangster('Big Boss Subordinate Level 1', 19)
        self.big_boss.add_subordinate(g1)

        self.assertEquals(self.mog.find_by_name('Big Boss Subordinate Level 1'), g1)

    def test_find_by_name_search_for_gangster_no_matter_its_level_in_organization(self):
        g3 = Gangster('Subordinate Level 3-1', 18)
        g4 = Gangster('Subordinate Level 3-2', 18)

        g2 = Gangster('Subordinate Level 2', 19)
        g2.add_subordinate(g4)
        g2.add_subordinate(g3)

        g1 = Gangster('Big Boss Subordinate Level 1', 20)
        g1.add_subordinate(g2)

        self.big_boss.add_subordinate(g1)

        self.assertEquals(self.mog.find_by_name('Subordinate Level 3-2'), g4)


class TestMafiaOrganizationAddUnder(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)
        self.g1 = Gangster('Big Boss Subordinate Level 1', 20)
        self.g2 = Gangster('Big Boss Subordinate Level 2', 21)

        self.mog = MafiaOrganization(self.big_boss)

    def test_add_under_accepts_only_gangsters(self):
        self.assertRaises(Exception, self.mog.add_under, '__big_boss', 'subordinate')

    def test_add_under_accepts_only_organization_members_as_boss(self):
        g2 = Gangster('Subordinate Level 2', 19)

        self.assertRaises(Exception, self.mog.add_under, self.g1, g2)

    def test_add_under_doesnt_accept_a_gangster_that_is_already_member(self):
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.big_boss, self.g2)

        self.assertRaises(Exception, self.mog.add_under, self.g1, self.g2)

    def test_add_under_doesnt_accept_a_boss_without_organization_attribute(self):
        self.big_boss.organization = None

        self.assertRaises(Exception, self.mog.add_under, self.big_boss, self.g1)

    def test_add_under_doesnt_accept_adding_a_gangster_as_a_subordinate_of_itself(self):
        self.assertRaises(SameGangsterException, self.mog.add_under, self.g1, self.g1)

    def test_add_under_add_correctly_the_gangster_as_subordinate(self):
        self.big_boss.add_subordinate = Mock(name='add_subordinate')
        self.mog.add_under(self.big_boss, self.g1)

        self.assertTrue(self.big_boss.add_subordinate.called)

    def test_add_under_sets_correct_subordinate_gangster_organization(self):
        self.mog.add_under(self.big_boss, self.g1)

        self.assertEquals(self.g1.organization, self.mog)


class TestMafiaOrganizationMembersCount(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)
        self.g1 = Gangster('Gangster', 20)
        self.g2 = Gangster('Gangster 2', 20)
        self.g3 = Gangster('Gangster 3', 20)

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.big_boss, self.g2)
        self.mog.add_under(self.g1, self.g3)

    def test_members_count_returns_the_correct_number_of_organization_members(self):
        self.assertEquals(self.mog.members_count(), 4)


class TestMafiaOrganizationIsMemberOfOrganization(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)
        self.g1 = Gangster('Gangster', 20)

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)

    def test_is_member_of_organization_for_big_boss_returns_true(self):
        self.assertTrue(self.mog.is_member_of_organization('Big Boss'))

    def test_is_member_of_organization_for_a_known_member_returns_true(self):
        self.assertTrue(self.mog.is_member_of_organization('Gangster'))

    def test_is_member_of_organization_for_a_unknown_member_returns_false(self):
        self.assertFalse(self.mog.is_member_of_organization('Another Gangster'))

    def test_is_member_of_organization_for_a_member_injail_returns_false(self):
        self.g1.status = GangsterStatus.INJAIL
        self.assertFalse(self.mog.is_member_of_organization('Gangster'))


class TestMafiaOrganizationKillMember(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)

        self.g1 = Gangster('Gangster', 20)
        self.g2 = Gangster('Gangster 2', 20, 'Location 2')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)

    def test_kill_member_on_unknown_gangster_returns_false(self):
        self.assertFalse(self.mog.kill_member('Unknown Gangster'))

    def test_kill_member_on_known_gangster_returns_true(self):
        self.assertTrue(self.mog.kill_member('Gangster'))

    def test_kill_member_sets_unknown_location_to_killed_gangster_subordinates(self):
        self.mog.kill_member('Gangster')

        self.assertEquals(self.g2.location, GangsterLocation.UNKNOWN)


class TestMafiaOrganizationKillMemberCase2LevelsKillLevel1(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21, 'Location Big Boss')
        self.g1 = Gangster('Gangster', 31, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 34, 'Location Gangster 2')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.big_boss, self.g2)

        # When
        self.mog.kill_member('Big Boss')

    def test_killed_member_is_no_longer_in_organization(self):
        self.assertIsNone(self.mog.find_by_name('Big Boss'))

    def test_killed_member_subordinate2_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster'), Gangster)
        self.assertIsInstance(self.mog.find_by_name('Gangster 2'), Gangster)

    def test_killed_member_oldest_subordinate_is_the_new_big_boss(self):
        self.assertEquals(self.g2, self.mog.get_big_boss())

    def test_the_new_big_boss_doesnt_have_a_boss(self):
        self.assertIsNone(self.g2.get_boss())

    def test_all_subordinates_have_unknown_location(self):
        self.assertEquals(self.g1.location, GangsterLocation.UNKNOWN)
        self.assertEquals(self.g2.location, GangsterLocation.UNKNOWN)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 2)


class TestMafiaOrganizationKillMemberCase3LevelsKillLevel1(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21, 'Location Big Boss')
        self.g1 = Gangster('Gangster', 20, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 20, 'Location Gangster 2')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)

        #When
        self.mog.kill_member('Big Boss')

    def test_killed_member_is_no_longer_in_organization(self):
        self.assertIsNone(self.mog.find_by_name('Big Boss'))

    def test_killed_member_subordinate_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster'), Gangster)

    def test_killed_member_subordinate_is_the_new_big_boss(self):
        self.assertEquals(self.g1, self.mog.get_big_boss())

    def test_the_new_big_boss_doesnt_have_a_boss(self):
        self.assertIsNone(self.g1.get_boss())

    def test_killed_member_subordinate_has_unknown_location(self):
        self.assertEquals(self.g1.location, GangsterLocation.UNKNOWN)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 2)


class TestMafiaOrganizationKillMemberCase3LevelsKillLevel2(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21, 'Location Big Boss')
        self.g1 = Gangster('Gangster', 20, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 20, 'Location Gangster 2')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)

        # When
        self.mog.kill_member('Gangster')

    def test_killed_member_is_no_longer_in_organization(self):
        self.assertIsNone(self.mog.find_by_name('Gangster'))

    def test_killed_member_subordinate_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster 2'), Gangster)

    def test_killed_member_subordinate_has_big_boss_as_a_new_boss(self):
        self.assertEquals(self.g2.get_boss(), self.mog.get_big_boss())

    def test_killed_member_subordinate_has_unknown_location(self):
        self.assertEquals(self.g2.location, GangsterLocation.UNKNOWN)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 2)


class TestMafiaOrganizationKillMemberCase3MultiLevelsKillLevel2(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21)
        self.g1 = Gangster('Gangster', 20, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 30, 'Location Gangster 2')
        self.g3 = Gangster('Gangster 3', 32, 'Location Gangster 3')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)
        self.mog.add_under(self.g1, self.g3)

        # When
        self.mog.kill_member('Gangster')

    def test_killed_member_is_no_longer_in_organization(self):
        self.assertIsNone(self.mog.find_by_name('Gangster'))

    def test_killed_member_subordinates_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster 2'), Gangster)
        self.assertIsInstance(self.mog.find_by_name('Gangster 3'), Gangster)

    def test_killed_member_oldest_subordinate_has_big_boss_as_a_new_boss(self):
        self.assertEquals(self.g3.get_boss(), self.mog.get_big_boss())

    def test_killed_member_youngest_subordinate_has_a_new_boss(self):
        self.assertEquals(self.g2.get_boss(), self.g3)

    def test_all_subordinates_have_unknown_location(self):
        self.assertEquals(self.g2.location, GangsterLocation.UNKNOWN)
        self.assertEquals(self.g3.location, GangsterLocation.UNKNOWN)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 3)


class TestMafiaOrganizationKillMemberCase3MultiLevelsDepthKillLevel2(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21, 'Location Big Boss')
        self.g1 = Gangster('Gangster', 31, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 32, 'Location Gangster 2')
        self.g3 = Gangster('Gangster 3', 33, 'Location Gangster 3')

        self.g4 = Gangster('Gangster 4', 12, 'Location Gangster 4')
        self.g5 = Gangster('Gangster 5', 12, 'Location Gangster 5')
        self.g6 = Gangster('Gangster 6', 12, 'Location Gangster 6')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.big_boss, self.g2)
        self.mog.add_under(self.big_boss, self.g3)

        self.mog.add_under(self.g1, self.g4)
        self.mog.add_under(self.g2, self.g5)
        self.mog.add_under(self.g3, self.g6)

        # When
        self.mog.kill_member('Gangster')

    def test_killed_member_is_no_longer_in_organization(self):
        self.assertIsNone(self.mog.find_by_name('Gangster'))

    def test_killed_member_subordinate_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster 4'), Gangster)

    def test_killed_member_subordinate_has_a_new_boss(self):
        self.assertEquals(self.g4.get_boss(), self.g3)
        self.assertEquals(self.g6.get_boss(), self.g3)

    def test_killed_member_subordinates_has_unknown_location(self):
        self.assertEquals(self.g4.location, GangsterLocation.UNKNOWN)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 6)


class TestMafiaOrganizationSendMemberToJail(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)

        self.g1 = Gangster('Gangster', 20)
        self.g2 = Gangster('Gangster 2', 20, 'Location 2')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)

    def test_send_member_to_jail_on_unknown_gangster_returns_false(self):
        self.assertFalse(self.mog.send_member_to_jail('Unknown Gangster'))

    def test_send_member_to_jail_on_known_gangster_returns_true(self):
        self.assertTrue(self.mog.send_member_to_jail('Gangster'))

    def test_send_member_to_jail_sets_injailstatus(self):
        self.mog.send_member_to_jail('Gangster')

        self.assertEquals(self.g1.status, GangsterStatus.INJAIL)

    def test_send_member_to_jail_removes_all_subordinates(self):
        self.mog.send_member_to_jail('Gangster')

        self.assertEquals(self.g1.subordinates_count(), 0)

    def test_send_member_to_jail_doesnt_update_subordinate_location_to_unknown(self):
        self.mog.send_member_to_jail('Gangster')

        self.assertEquals(self.g2.location, 'Location 2')

    def test_send_member_to_jail_update_current_boss_attribute_on_subordinates(self):
        self.mog.send_member_to_jail('Gangster')
        self.assertEquals(self.g2.get_boss(), self.big_boss)

    def test_send_member_to_jail_update_previous_boss_attribute_on_subordinates(self):
        self.mog.send_member_to_jail('Gangster')
        self.assertEquals(self.g2.boss_in_jail, self.g1)


class TestMafiaOrganizationSendMemberToJailCase3MultiLevelsDepthKillLevel2(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21, 'Location Big Boss')
        self.g1 = Gangster('Gangster', 31, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 32, 'Location Gangster 2')
        self.g3 = Gangster('Gangster 3', 33, 'Location Gangster 3')

        self.g4 = Gangster('Gangster 4', 12, 'Location Gangster 4')
        self.g5 = Gangster('Gangster 5', 12, 'Location Gangster 5')
        self.g6 = Gangster('Gangster 6', 12, 'Location Gangster 6')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.big_boss, self.g2)
        self.mog.add_under(self.big_boss, self.g3)

        self.mog.add_under(self.g1, self.g4)
        self.mog.add_under(self.g2, self.g5)
        self.mog.add_under(self.g3, self.g6)

        # When
        self.mog.send_member_to_jail('Gangster')

    def test_send_member_to_jail_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster'), Gangster)

    def test_send_member_to_jail_is_no_longer_found_by_is_member_of_organization(self):
        self.assertFalse(self.mog.is_member_of_organization('Gangster'))

    def test_send_member_to_jail_subordinate_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster 4'), Gangster)

    def test_send_member_to_jail_subordinate_has_a_new_boss(self):
        self.assertEquals(self.g4.get_boss(), self.g3)
        self.assertEquals(self.g6.get_boss(), self.g3)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 7)


class TestMafiaOrganizationSendMemberToJailCase3MultiLevelsKillLevel2(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21)
        self.g1 = Gangster('Gangster', 20, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 30, 'Location Gangster 2')
        self.g3 = Gangster('Gangster 3', 32, 'Location Gangster 3')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)
        self.mog.add_under(self.g1, self.g3)

        # When
        self.mog.send_member_to_jail('Gangster')

    def test_send_member_to_jail_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster'), Gangster)

    def test_send_member_to_jail_is_no_longer_found_by_is_member_of_organization(self):
        self.assertFalse(self.mog.is_member_of_organization('Gangster'))

    def test_send_member_to_jail_oldest_subordinate_has_big_boss_as_a_new_boss(self):
        self.assertEquals(self.g3.get_boss(), self.mog.get_big_boss())

    def test_send_member_to_jail_youngest_subordinate_has_a_new_boss(self):
        self.assertEquals(self.g2.get_boss(), self.g3)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 4)


class TestMafiaOrganizationSetMemberToFreedom(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)

        self.g1 = Gangster('Gangster', 20)
        self.g2 = Gangster('Gangster 2', 20, 'Location 2')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)

        self.mog.send_member_to_jail('Gangster')

    def test_set_member_to_freedom_on_unknown_gangster_returns_false(self):
        self.assertFalse(self.mog.set_member_to_freedom('Unknown Gangster'))

    def test_set_member_to_freedom_on_known_gangster_returns_true(self):
        self.assertTrue(self.mog.set_member_to_freedom('Gangster'))

    def test_set_member_to_freedom_sets_freestatus(self):
        self.mog.set_member_to_freedom('Gangster')

        self.assertEquals(self.g1.status, GangsterStatus.FREE)

    def test_set_member_to_freedom_restores_all_subordinates(self):
        self.mog.set_member_to_freedom('Gangster')

        self.assertEquals(self.g1.subordinates_count(), 1)


class TestMafiaOrganizationSetMemberToFreedomCase3MultiLevelsDepthKillLevel2(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21, 'Location Big Boss')
        self.g1 = Gangster('Gangster', 31, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 32, 'Location Gangster 2')
        self.g3 = Gangster('Gangster 3', 33, 'Location Gangster 3')

        self.g4 = Gangster('Gangster 4', 12, 'Location Gangster 4')
        self.g5 = Gangster('Gangster 5', 12, 'Location Gangster 5')
        self.g6 = Gangster('Gangster 6', 12, 'Location Gangster 6')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.big_boss, self.g2)
        self.mog.add_under(self.big_boss, self.g3)

        self.mog.add_under(self.g1, self.g4)
        self.mog.add_under(self.g2, self.g5)
        self.mog.add_under(self.g3, self.g6)

        self.mog.send_member_to_jail('Gangster')

        # When
        self.mog.set_member_to_freedom('Gangster')

    def test_set_member_to_freedom_is_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster'), Gangster)

    def test_set_member_to_freedom_is_found_by_is_member_of_organization(self):
        self.assertTrue(self.mog.is_member_of_organization('Gangster'))

    def test_set_member_to_freedom_subordinate_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster 4'), Gangster)

    def test_set_member_to_freedom_previous_subordinate_returns_to_the_previous_boss(self):
        self.assertEquals(self.g4.get_boss(), self.g1)
        self.assertEquals(self.g6.get_boss(), self.g3)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 7)


class TestMafiaOrganizationMemberToFreedomCase3MultiLevelsKillLevel2(TestCase):
    def setUp(self):
        # Given
        self.big_boss = Gangster('Big Boss', 21)
        self.g1 = Gangster('Gangster', 20, 'Location Gangster')
        self.g2 = Gangster('Gangster 2', 30, 'Location Gangster 2')
        self.g3 = Gangster('Gangster 3', 32, 'Location Gangster 3')

        self.mog = MafiaOrganization(self.big_boss)
        self.mog.add_under(self.big_boss, self.g1)
        self.mog.add_under(self.g1, self.g2)
        self.mog.add_under(self.g1, self.g3)

        self.mog.send_member_to_jail('Gangster')

        # When
        self.mog.set_member_to_freedom('Gangster')

    def test_set_member_to_freedom_is_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster'), Gangster)

    def test_set_member_to_freedom_is_found_by_is_member_of_organization(self):
        self.assertTrue(self.mog.is_member_of_organization('Gangster'))

    def test_set_member_to_freedom_subordinate_is_still_in_organization(self):
        self.assertIsInstance(self.mog.find_by_name('Gangster 2'), Gangster)
        self.assertIsInstance(self.mog.find_by_name('Gangster 3'), Gangster)

    def test_set_member_to_freedom_previous_subordinate_returns_to_the_previous_boss(self):
        self.assertEquals(self.g3.get_boss(), self.g1)
        self.assertEquals(self.g2.get_boss(), self.g1)

    def test_correct_organization_count(self):
        self.assertEquals(self.mog.members_count(), 4)