from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
DAF_model = BayesianNetwork([('Drives', 'Air_is_good'), ('Air_is_good', 'Fined'), ('Drives', 'Fined')])

cpd_d = TabularCPD(
    variable='Drives',
    variable_card=5,
    values=[
        [0.0625],
        [0.25],
        [0.375],
        [0.25],
        [0.0625]],
    state_names={'Drives': ['0','1', '2','3','4']})
cpd_a = TabularCPD(variable='Air_is_good',
                   variable_card=2,
                   values=[[0.8, 0.8, 0.8,0.6,0.6],
                           [0.2,0.2, 0.2, 0.4,0.4]],
                   evidence=['Drives'],
                   evidence_card=[5],
                   state_names={'Air_is_good': ['True', 'False'],'Drives': ['0','1', '2','3','4']})
# The representation of CPD in pgmpy is a bit different than the CPD shown in the above picture. In pgmpy the colums
# are the evidences and rows are the states of the variable. So the grade CPD is represented like this:
#
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    | Drives  |   D_0   |   D_0   |   D_1   |   D_1   |   D_2   |   D_2   |   D_3   |   D_3   |   D_4   |   D_4   |
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    |  A_i_g  | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T |
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    | Fined_T |  0.3        0.1      0.3         0.1      0.3        0.1      0.8        0.1     0.8         0.1
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
#    | Fined_F |  0.7         0.9       0.7       0.9     0.7         0.9         0.2     0.9     0.2         0.9
#    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+

cpd_f = TabularCPD(variable='Fined', variable_card=2, values=[
    [0.1, 0.3, 0.1, 0.3,0.1, 0.3,0.1,0.8,0.1,0.8],
    [0.9, 0.7, 0.9, 0.7,0.9,0.7,0.9,0.2,0.9,0.2]],
                   evidence=['Drives','Air_is_good'],
                   evidence_card=[5,2],
                   state_names={'Fined': ['True', 'False'],'Air_is_good': ['True', 'False'],'Drives': ['0','1', '2','3','4']})

DAF_model.add_cpds(cpd_d, cpd_a, cpd_f)
# print(DAF_model.check_model())
# print(DAF_model.edges())
# print(DAF_model.get_cpds('Fined'))

# print(DAF_model.get_cpds('Fined').values)
infer = VariableElimination(DAF_model)
# print(infer.query(['Fined'], evidence={'Air_is_good': 'False', 'Drives': '0'}))
print(infer.query(['Fined','Drives','Air_is_good']))
print(DAF_model.get_independencies())
# DAF_model.save('model_file')
