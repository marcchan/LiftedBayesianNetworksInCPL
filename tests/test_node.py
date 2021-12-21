import unittest
from lbn.input.node import Node, init_nodes_from_json


class TestNode(unittest.TestCase):

    def test_get_name(self):
        node1 = Node('Drives', 'int', 4)
        self.assertEqual(node1.get_name(), "Drives")

    def test_get_type(self):
        node1 = Node('Drives', 'int', 4)
        self.assertEqual(node1.get_type(), "int")

    def test_get_domain(self):
        node1 = Node('Drives', 'int', 4)
        self.assertEqual(node1.get_domain(), int(4))

    def test_init_nodelist_from_json(self):
        file_path = '../examples/drives_air_fined/domain'
        nodes = init_nodes_from_json(file_path)
        self.assertEqual(nodes[0].get_domain(), 4)
        self.assertEqual(type(nodes[0].get_domain()), int)
        self.assertEqual(nodes[1].get_domain(), [True, False])


if __name__ == '__main__':
    unittest.main()
