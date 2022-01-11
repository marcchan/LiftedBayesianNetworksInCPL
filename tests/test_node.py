import unittest
from lbn.input.node import Node


class TestNode(unittest.TestCase):

    def test_get_name(self):
        node1 = Node('Drives', 'int', 4)
        self.assertEqual(node1.get_name(), "Drives")



if __name__ == '__main__':
    unittest.main()
