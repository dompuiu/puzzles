from unittest import TestCase
from mock import Mock, patch

from src.mafia_organization import MafiaOrganization
from src.gangster import Gangster


class TestMafiaOrganizationConstructor(TestCase):
    def setUp(self):
        self.big_boss = Gangster('Big Boss', 21)
        self.mog = MafiaOrganization(self.big_boss)

    def test_constructor_accepts_only_a_gangster_as_big_boss(self):
        self.assertRaises(Exception, MafiaOrganization, 'big_boss')

    def test_constructor_creates_new_organization_instance(self):
        self.assertIsInstance(self.mog, MafiaOrganization)

    def test_constructor_sets_correct_big_boss(self):
        self.assertEquals(self.mog.big_boss, self.big_boss)

    def test_constructor_sets_boss_organization(self):
        self.assertEquals(self.mog.big_boss.organization, self.mog)


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
    big_boss = Gangster('Big Boss', 21)

    def setUp(self):
        self.g1 = Gangster('Big Boss Subordinate Level 1', 20)
        self.mog = MafiaOrganization(self.big_boss)

    def test_add_under_accepts_only_gangsters(self):
        self.assertRaises(Exception, self.mog.add_under, 'big_boss', 'subordinate')

    def test_add_under_accepts_only_organization_members_as_boss(self):
        g2 = Gangster('Subordinate Level 2', 19)

        self.assertRaises(Exception, self.mog.add_under, self.g1, g2)

    @patch.object(big_boss, 'add_subordinate', Mock(name='add_subordinate'))
    def test_add_under_add_correctly_the_gangster_as_subordinate(self):
        self.mog.add_under(self.big_boss, self.g1)

        self.assertTrue(self.big_boss.add_subordinate.called)

    def test_add_under_sets_correct_subordinate_gangster_organization(self):
        self.mog.add_under(self.big_boss, self.g1)

        self.assertEquals(self.g1.organization, self.mog)
