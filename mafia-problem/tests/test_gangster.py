from unittest import TestCase
from src.gangster import Gangster, GangsterStatus, GangsterLocation


class TestGangster(TestCase):
    def setUp(self):
        self.g = Gangster('some gangster', 12)

    def test_constructor_creates_new_gangster_instance(self):
        self.assertIsInstance(self.g, Gangster)

    def test_constructor_sets_correct_name(self):
        self.assertEquals(self.g.name, 'some gangster')

    def test_constructor_sets_unknown_location(self):
        self.assertEquals(self.g.location, GangsterLocation.UNKNOWN)

    def test_constructor_accepts_only_int_age(self):
        self.assertRaises(Exception, Gangster, 'name', 'age')

    def test_constructor_sets_correct_age(self):
        g = Gangster('name', 45, 'my location')
        self.assertEquals(g.age, 45)

    def test_constructor_sets_correct_location(self):
        g = Gangster('name', 45, 'my location')
        self.assertEquals(g.location, 'my location')


class TestGangsterSubordinates(TestCase):
    def setUp(self):
        self.g = Gangster('Gangster', 44)

        self.gs = Gangster('Subordinate', 43)
        self.g.add_subordinate(self.gs)

    def test_subordinates_counts_returns_correct_count(self):
        self.assertEquals(self.g.subordinates_count(), 1)

    def test_add_subordinate_throws_error_on_not_gangster_instance(self):
        self.assertRaises(Exception, self.g.add_subordinate, 'gigi')

    def test_add_subordinate_can_add_gangster(self):
        self.assertEquals(self.g.subordinates_count(), 1)

    def test_add_subordinate_sets_the_correct_boss_on_gangster(self):
        self.assertEquals(self.gs.get_boss(), self.g)

    def test_subordinates_returns_iterator(self):
        self.assertEquals(self.gs, next(self.g.subordinates()))

    def test_delete_subordinate_throws_error_on_not_gangster_instance(self):
        self.assertRaises(Exception, self.g.delete_subordinate, 'gigi')

    def test_delete_subordinate_when_delete_subordinate_gangster_returns_true(self):
        self.assertTrue(self.g.delete_subordinate(self.gs))

    def test_delete_subordinate_when_delete_unknown_gangster_returns_false(self):
        ngs = Gangster('Not Subordinate', 43)
        self.assertFalse(self.g.delete_subordinate(ngs))


class TestGangsterBoss(TestCase):
    def setUp(self):
        self.g = Gangster('Gangster', 15)
        self.gb = Gangster('Gangster  Boss', 75)

        self.g.set_boss(self.gb)

    def test_has_boss_on_newly_created_gangster_return_false(self):
        g = Gangster('Gang', 12)
        self.assertFalse(g.has_boss())

    def test_set_boss_throws_error_on_not_gangster_instance(self):
        self.assertRaises(Exception, self.g.set_boss, 'gigi')

    def test_set_boss_accepts_none(self):
        self.assertTrue(self.g.set_boss(None))

    def test_set_boss_updates_the_gangster_boss(self):
        self.assertTrue(self.g.has_boss())

    def test_get_boss_returns_gangster_boss(self):
        self.assertEquals(self.g.get_boss(), self.gb)
