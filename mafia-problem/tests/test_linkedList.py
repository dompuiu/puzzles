from unittest import TestCase
from src.linked_list import LinkedList
from src.linked_list import Empty


class TestLinkedList(TestCase):
    @classmethod
    def get_next_element(cls, node):
        return node.get_next().get_element()

    def setUp(self):
        self.l = LinkedList()

    def test_is_empty_for_new_list_returns_true(self):
        self.assertTrue(self.l.is_empty)

    def test_is_empty_for_populated_list_returns_false(self):
        self.l.add_first(1)

        self.assertFalse(self.l.is_empty())

    def test_get_first_from_empty_list_throws_exception(self):
        self.assertRaises(Empty, self.l.get_first)

    def test_get_first_from_populated_list_returns_head_node(self):
        self.l.add_first(1)
        self.l.add_first(2)

        h = self.l.get_first()
        self.assertEquals(h.get_element(), 2)

    def test_add_first_returns_added_node(self):
        self.assertEquals(self.l.add_first(1).get_element(), 1)

    def test_add_first_links_nodes_between_them(self):
        self.l.add_first(2)
        self.l.add_first(1)

        h = self.l.get_first()
        self.assertEquals(TestLinkedList.get_next_element(h), 2)

    def test_length_on_empty_list_returns_0(self):
        self.assertEquals(len(self.l), 0)

    def test_length_on_populated_list_returns_correct_length(self):
        self.l.add_first(1)

        self.assertEquals(len(self.l), 1)

    def test_find_when_list_is_empty(self):
        self.assertRaises(Empty, self.l.find, 1)

    def test_find_on_populated_list_returns_the_element_node(self):
        self.l.add_first(1)

        self.assertEquals(self.l.find(1).get_element(), 1)

    def test_find_non_existing_element_returns_null(self):
        self.l.add_first(1)

        self.assertEquals(self.l.find(2), None)

    def test_contains_on_empty_list_throws_exception(self):
        self.assertRaises(Empty, self.l.contains, 1)

    def test_contains_existing_element_returns_true(self):
        self.l.add_first(1)

        self.assertTrue(self.l.contains(1))

    def test_contains_non_existing_element_returns_false(self):
        self.l.add_first(1)

        self.assertFalse(self.l.contains(2))

    def test_remove_from_empty_list_throws_error(self):
        self.assertRaises(Empty, self.l.remove, 1)

    def test_remove_non_existing_element_returns_false(self):
        self.l.add_first(10)

        self.assertFalse(self.l.remove(2))

    def test_remove_first_element_of_one_element_list_returns_true(self):
        self.l.add_first(1)

        self.assertTrue(self.l.remove(1))

    def test_remove_first_element_of_one_element_list_decreases_the_length_of_the_list(self):
        self.l.add_first(1)
        self.l.remove(1)

        self.assertEquals(len(self.l), 0)

    def test_remove_first_element_of_one_element_list_makes_head_empty(self):
        self.l.add_first(1)
        self.l.remove(1)

        self.assertRaises(Empty, self.l.get_first)

    def test_remove_first_element_of_a_list_returns_true(self):
        self.l.add_first(1)
        self.l.add_first(2)

        self.assertTrue(self.l.remove(2))

    def test_remove_first_element_of_a_list_makes_the_next_element_as_new_head(self):
        self.l.add_first(1)
        self.l.add_first(2)

        self.l.remove(2)

        self.assertTrue(self.l.get_first().get_element(), 1)

    def test_remove_last_element_of_a_list_with_two_elements_returns_true(self):
        self.l.add_first(1)
        self.l.add_first(2)

        self.assertTrue(self.l.remove(1))

    def test_remove_last_element_of_a_list_with_two_elements_doesnt_change_head(self):
        self.l.add_first(1)
        self.l.add_first(2)

        self.l.remove(1)

        self.assertTrue(self.l.get_first().get_element(), 2)

    def test_remove_last_element_of_a_list_with_two_elements_breaks_the_link_with_head(self):
        self.l.add_first(1)
        n = self.l.add_first(2)

        self.l.remove(1)

        self.assertEquals(n.get_next(), None)

    def test_remove_element_of_a_list_returns_true(self):
        self.l.add_first(1)
        self.l.add_first(2)
        self.l.add_first(3)

        self.assertTrue(self.l.remove(2))

    def test_remove_element_of_a_list_updates_link_between_nodes(self):
        self.l.add_first(1)
        self.l.add_first(2)
        self.l.add_first(3)

        self.l.remove(2)

        v = TestLinkedList.get_next_element(self.l.get_first())
        self.assertEquals(v, 1)

    def test_remove_first_element_changes_the_head_node(self):
        self.l.add_first(1)
        n = self.l.add_first(2)
        self.l.add_first(3)

        self.l.remove(3)

        self.assertEquals(self.l.get_first(), n)

    def test_list_nodes_from_empty_list_returns_nothing(self):
        r = set()

        for node in self.l.get_elements():
            r.add(node)

        self.assertEquals(r, set())

    def test_list_nodes_iterates_through_all_list(self):
        self.l.add_first(1)
        self.l.add_first(2)
        self.l.add_first(3)

        r = set()
        for node in self.l.get_elements():
            r.add(node)

        self.assertEquals(r, set([1,2,3]))