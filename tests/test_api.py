import unittest

from numpy.ma.testutils import assert_almost_equal
from pgmpy.factors.discrete import TabularCPD
from lbn.api import generate_bn_model
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork


class TestNode(unittest.TestCase):

    def test_generate_bn_model(self):
        FORMULA_FILE_drives = '../examples/drives_air_fined/formula_v2'
        Domain_FILE_drives = '../examples/drives_air_fined/domain_v1'
        BN_model = generate_bn_model(FORMULA_FILE_drives, Domain_FILE_drives)
        infer = VariableElimination(BN_model)
        True_Value = infer.query(["Fined"]).get_value(Fined=True)
        assert_almost_equal(True_Value, 0.215)
        print(f'derives runs')
        FORMULA_FILE_school = '../examples/attend_grade_school/formula_v2'
        Domain_FILE_school = '../examples/attend_grade_school/domain_v1'
        BN_model_1 = generate_bn_model(FORMULA_FILE_school, Domain_FILE_school)
        True_value_2 = VariableElimination(BN_model_1).query(
            ['SchoolGood']).get_value(SchoolGood=True)
        print(True_value_2)
        assert_almost_equal(True_value_2, 0.7342, decimal=4)
        print(f'school runs')


if __name__ == '__main__':
    unittest.main()
