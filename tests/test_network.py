import unittest
from lbn.network_helper import parse_to_network
from numpy.ma.testutils import assert_almost_equal
from pgmpy.factors.discrete import TabularCPD
from lbn.api import generate_bn_model
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork


class TestNetwork(unittest.TestCase):

    def test_pre_computing(self):
        FORMULA_FILE = '../examples/pre_computing_case/formula_v2'
        Domain_FILE = '../examples/pre_computing_case/domain'
        network_pre = parse_to_network(FORMULA_FILE, Domain_FILE)
        print(network_pre)

        # network_pre.pre_computing()
    def test_check_redundancy(self):
        # name_list = ['A','B','C','D']
        # evidences = {'A': set(), 'B':{'A'}, 'C':{'B'},'D':{'C'}}
        # check_redundancy(name_list,evidences)
        name_list_1 = [
            'illness',
            'qualified',
            'good_teacher',
            'good_grade',
            'attends',
            'good_school']
        evidences_2 = {
            'qualified': set(),
            'good_teacher': {'qualified'},
            'illness': set(),
            'attends': {
                'good_teacher',
                'illness'},
            'good_grade': {'good_teacher'},
            'good_school': {
                'attends',
                'good_grade'}}
        self.assertEqual({'qualified', 'illness'},
                         check_redundancy(name_list_1, evidences_2))


if __name__ == '__main__':
    unittest.main()
