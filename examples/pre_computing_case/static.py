from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from lbn.input.network import *
# BN_model = BayesianNetwork(
#     [('GoodTeacher', 'GoodGrade'), ('GoodTeacher', 'Attends'), ('GoodGrade', 'GoodSchool'), ('Attends', 'GoodSchool')])
BN_model = BayesianNetwork(
    [('GoodTeacher', 'GoodGrade'),('GoodTeacher', 'Attends')])
cpd_gt = TabularCPD(
    variable='GoodTeacher',
    variable_card=5,
    values=[
        [0.053084],
        [0.23003],
        [0.3738],
        [0.26997],
        [0.073116]],
    state_names={'GoodTeacher': ['0', '1','2','3','4']})
cpd_gg = TabularCPD(variable='GoodGrade',
                   variable_card=5,
                   values=[[0.4096, 0.4096, 0.4096,0.1296,0.1296],
                            [0.4096,0.4096 , 0.4096,0.3456,0.3456],
                             [0.1536, 0.1536,0.1536,0.3456,0.3456],
                              [0.0256, 0.0256, 0.0256,0.1536,0.1536],
                               [0.0016, 0.0016, 0.0016,0.0256,0.0256]],
                   evidence=['GoodTeacher'],
                   evidence_card=[5],
                   state_names={'GoodTeacher': ['0', '1','2','3','4'], 'GoodGrade': ['0', '1','2','3','4']})


cpd_a = TabularCPD(variable='Attends',
                   variable_card=5,
                   values=[[0.4096, 0.4096, 0.4096,0.1296,0.1296],
                            [0.4096,0.4096 , 0.4096,0.3456,0.3456],
                             [0.1536, 0.1536,0.1536,0.3456,0.3456],
                              [0.0256, 0.0256, 0.0256,0.1536,0.1536],
                               [0.0016, 0.0016, 0.0016,0.0256,0.0256]],
                   evidence=['GoodTeacher'],
                   evidence_card=[5],
                   state_names={'GoodTeacher': ['0', '1','2','3','4'], 'Attends': ['0', '1','2','3','4']})
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

cpd_gs = TabularCPD(
    variable='GoodSchool', variable_card=2, values=[
        [0.1, 0.3, 0.1, 0.3, 0.1, 0.3, 0.1, 0.8, 0.1, 0.8],
        []],
        evidence=[
                    'GoodGrade', 'Attends'], evidence_card=[
                        5, 2], state_names={
                            'Fined': [
                                True, False], 'Air_is_good': [
                                    True, False], 'Drives': ['||D|| = 0', '1','2','3','4']})
BN_model.add_cpds(cpd_gt, cpd_gg)
print(BN_model.check_model())
print(f'Network with edges: {BN_model.edges()}')

infer = VariableElimination(BN_model)



print(infer.query(['GoodTeacher']))
print(infer.query(['GoodGrade']))
print(infer.query(['GoodTeacher','GoodGrade']))
print(infer.query(['GoodTeacher','GoodGrade','Attends']))


# use bip file
# BNN =  BayesianNetwork([('Drives', 'Air_is_good'), ('Air_is_good', 'Fined'), ('Drives', 'Fined')]).load('model_file')
# infer = VariableElimination(BNN)
