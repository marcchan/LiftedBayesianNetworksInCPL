import unittest
from lbn.input.network import Network,check_redundancy
from numpy.ma.testutils import assert_almost_equal
from pgmpy.factors.discrete import TabularCPD
from lbn.api import generate_bn_model
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

class TestNetwork(unittest.TestCase):

    def test_pre_computing(self):
        FORMULA_FILE = '../examples/pre_computing_case/formula_v2'
        Domain_FILE = '../examples/pre_computing_case/domain'
        network_pre = Network(FORMULA_FILE, Domain_FILE)
        print(network_pre.get_distributions())

        # network_pre.pre_computing()
if __name__ == '__main__':
    unittest.main()
