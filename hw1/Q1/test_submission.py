
import unittest
from submission import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_no_nodes(self):
        self.assertEqual([], self.graph.get_nodes() )

    def test_add_node_new(self):
        self.graph = Graph()
        self.graph.add_node(id='2975', name='Laurence Fishburne')
        self.assertEqual(self.graph.get_nodes(), [('2975', 'Laurence Fishburne')] )

    def test_add_node_two(self):
        self.graph = Graph()
        self.graph.add_node(id='2975', name='Laurence Fishburne')
        self.graph.add_node(id='3333', name='Keanu Reeves')
        self.assertEqual(self.graph.get_nodes(), [('2975', 'Laurence Fishburne'), ('3333', 'Keanu Reeves')])

    def test_add_node_exists(self):
        self.graph = Graph()
        self.graph.add_node(id='2975', name='Laurence Fishburne')
        self.graph.add_node(id='2975', name='Laurence Fishburne')
        self.assertEqual(self.graph.get_nodes(), [('2975', 'Laurence Fishburne')] )

    def test_count_no_nodes(self):
        self.graph = Graph()
        self.assertEqual(self.graph.total_nodes(), 0)
 
    def test_count_no_nodes(self):
        self.graph = Graph()
        self.graph.add_node(id='2975', name='Laurence Fishburne')
        self.assertEqual(self.graph.total_nodes(), 1)       

    def test_count_no_nodes(self):
        self.graph = Graph()
        self.graph.add_node(id='2975', name='Laurence Fishburne')
        self.graph.add_node(id='3333', name='Keanu Reeves')
        self.assertEqual(self.graph.total_nodes(), 2)

    # def test_neg_int(self):
    #     self.__assert_csv_formatted_correctly((-5,), b'-5\r\n')

    # def test_zero_int(self):
    #     self.__assert_csv_formatted_correctly((0,), b'0\r\n')
