import unittest
from lbn.input.lbn_node import Node, init_nodes_from_json

class NodeCase(unittest.TestCase):
    def test_init(self):
        node1 = Node("Drives","int",4)
        self.assertEqual(node1.get_name(), "Drives")
        self.assertEqual(node1.get_type(),"int")
        self.assertTrue(node1.get_domain(),4)

        node2 = Node("Air_is_good", "bool")
        self.assertEqual(node2.get_name(), "Air_is_good")
        self.assertEqual(node2.get_type(), "bool")
        self.assertTrue(node2.get_domain(), [True,False])
    def test_init_nodelist_from_json(self):
        file_path = '../examples/node_domain'
        nodes = init_nodes_from_json(file_path)
        self.assertEqual(nodes[0].get_domain(), 4)
        self.assertEqual(type(nodes[0].get_domain()), int)
        self.assertEqual(nodes[1].get_domain(), [True, False])
if __name__ == '__main__':
    unittest.main()
