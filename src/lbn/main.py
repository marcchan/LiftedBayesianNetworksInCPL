from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
model = BayesianModel(
    [('Drives', 'Air_is_good'), ('Air_is_good', 'Fined'), ('Drives', 'Fined')])
cpd_d = TabularCPD(variable='Drives', variable_card=5, values=[
                   [0.0625], [0.25], [0.375], [0.25], [0.0625]])
cpd_a = TabularCPD(variable='Air_is_good', variable_card=2, values=[
    [0.8 * 0.0625, 0.8 * 0.25, 0.8 * 0.375, 0.6 * 0.25, 0.6 * 0.0625],
    [0.2 * 0.0625, 0.2 * 0.25, 0.2 * 0.375, 0.4 * 0.25, 0.4 * 0.0625]],
                   evidence=['Drives'],
                   evidence_card=[5])
# The representation of CPD in pgmpy is a bit different than the CPD shown in the above picture. In pgmpy the colums
# are the evidences and rows are the states of the variable. So the grade CPD is represented like this:
#
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    | Drives  |   D_0   |   D_0   |   D_1   |   D_1   |   D_2   |   D_2   |   D_3   |   D_3   |   D_4   |   D_4   |
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    |  A_i_g  | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T |
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    | Fined_T |
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    | Fined_F |
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+

cpd_f = TabularCPD(variable='Fined', variable_card=2, values=[
    [0.005, 0.00375,  0.02 , 0.015, 0.03,0.0225, 0.015,0.08, 0.00375, 0.02],
    [0.045, 0.00875, 0.18 , 0.035, 0.27,0.0525, 0.135, 0.02,0.03375,0.005]],
                   evidence=['Drives','Air_is_good'],
                   evidence_card=[5,2])

model.add_cpds(cpd_d, cpd_a, cpd_f)
print(model.check_model())