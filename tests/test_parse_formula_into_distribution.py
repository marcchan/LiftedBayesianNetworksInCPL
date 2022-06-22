import unittest
from lbn.parse_formula_into_distribution import *
from lbn.network_helper import parse_to_network

class TestNode(unittest.TestCase):
    def test_get_lower_para_fron_node(self):
        FORMULA_FILE_drives = '../examples/attend_grade_school/formula_v2'
        Domain_FILE_drives = '../examples/attend_grade_school/domain_v1'
        network = parse_to_network(FORMULA_FILE_drives, Domain_FILE_drives)
        nodes = network.get_nodes()
        self.assertEqual(('(x)', '_x'), get_lower_para_from_node(nodes[0]))
        self.assertEqual(('(x)', '_x'), get_lower_para_from_node(nodes[1]))
        self.assertEqual(('', ''), get_lower_para_from_node(nodes[2]))

    def test_str_expression_helper(self):
        FORMULA_FILE_school = '../examples/attend_grade_school/formula_v2'
        Domain_FILE_school = '../examples/attend_grade_school/domain_v1'
        network_ags = parse_to_network(FORMULA_FILE_school, Domain_FILE_school)
        nodes_ags = network_ags.get_nodes()

        FORMULA_FILE_drives = '../examples/drives_air_fined/formula_v2'
        Domain_FILE_drives = '../examples/drives_air_fined/domain_v1'
        network_daf = parse_to_network(FORMULA_FILE_drives, Domain_FILE_drives)
        nodes_daf = network_daf.get_nodes()
        # # v_2
        # # air_is_good
        self.assertEqual(
            '0.0 <= 0.5 ', str_expression_helper(
                '||Drives(x) <= 0.5 ||_x', evi_value_dict={
                    'Drives': 0}, state_name={
                    'AirIsGood': [
                        True, False], 'Drives': [
                        0, 1, 2, 3, 4]}, nodes=nodes_daf))
        # fined
        self.assertEqual(
            ' not False and 0.5 >= 0.7 ', str_expression_helper(
                '!AirIsGood & ||Drives(x) >= 0.7||_x ', {
                    'AirIsGood': False, 'Drives': 2}, {
                    'Fined': [
                        True, False], 'AirIsGood': [
                        True, False], 'Drives': [
                            0, 1, 2, 3, 4]}, nodes=nodes_daf))
        # good_grade

        self.assertEqual(
            '0.0 >= 0.95 and 0.0 >= 0.30 ', str_expression_helper(
                '||Attends(x) >= 0.95||_x & ||GoodGrade(x) >= 0.30||_x ', {
                    'Attends': 0, 'GoodGrade': 0}, {
                    'SchoolGood': [
                        True, False], 'Attends': [
                        0, 1, 2, 3, 4], 'GoodGrade': [
                            0, 1, 2, 3, 4]}, nodes=nodes_ags))

    def test_check_probability_from_distribution(self):
        pass

    def test_recursive_data(self):
        pass

    def test_fill_data_into_values(self):
        pass


if __name__ == '__main__':
    unittest.main()
