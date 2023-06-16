from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from lbn.input.network import *
# DAF_model = BayesianNetwork()

DAF_model = BayesianNetwork(
    [('Drives_x1', 'Air_is_good'), ('Drives_x2', 'Air_is_good'), ('Drives_x3', 'Air_is_good'),
     ('Drives_x4', 'Air_is_good')])
cpd_d1 = TabularCPD(
    variable='Drives_x1',
    variable_card=2,
    values=[[0.5],
        [0.5]])
# DAF_model.add_node(cpd_d1)
# # DAF_model.add_edge()
#
cpd_d2 = TabularCPD(
    variable='Drives_x2',
    variable_card=2,
    values=[[0.5],
        [0.5]],
    state_names={'Drives_x2': [True, False]})
# DAF_model.add_node(cpd_d2)
cpd_d3 = TabularCPD(
    variable='Drives_x3',
    variable_card=2,
    values=[[0.5],
        [0.5]],
    state_names={'Drives_x3': [True, False]})
# DAF_model.add_node(cpd_d3)
cpd_d4 = TabularCPD(
    variable='Drives_x4',
    variable_card=2,
    values=[[0.5],
        [0.5]],
    state_names={'Drives_x4': [True, False]})


# DAF_model.add_node(cpd_d4)

#    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#    |Drives_x1|   0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  1  |  1  |  1  |  1  |  1  |  1  |  1  |  1  |
#    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#    |Drives_x2|   0  |  0  |  0  |  0  |  1  |  1  |  1  |  1  |  0  |  0  |  0  |  0  |  1  |  1  |  1  |  1  |
#    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#    |Drives_x3|   0  |  0  |  1  |  1  |  0  |  0  |  1  |  1  |  0  |  0  |  1  |  1  |  0  |  0  |  1  |  1  |
#    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#    |Drives_x4|   0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |
#    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#    |    A_T    | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.6 | 0.8 | 0.8 | 0.8 | 0.6 | 0.8 | 0.6 | 0.6 | 0.6 |
#    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
#    |    A_F    | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.4 | 0.2 | 0.2 | 0.2 | 0.4 | 0.2 | 0.4 | 0.4 | 0.4 |
#    +-----------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+

cpd_a = TabularCPD(variable='Air_is_good',
                   variable_card=2,
                   values=[[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.6, 0.8, 0.8, 0.8, 0.6, 0.8, 0.6, 0.6, 0.6],
                           [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.4, 0.2, 0.4, 0.4, 0.4]],
                   evidence=['Drives_x1','Drives_x2','Drives_x3','Drives_x4'],
                   evidence_card=[2,2,2,2],
                   state_names={'Air_is_good': [True, False], 'Drives_x1': [True, False],'Drives_x2': [True, False],'Drives_x3': [True, False],'Drives_x4': [True, False] })

# DAF_model.add_node(cpd_a)
# DAF_model.add_edge('Drives_x1', 'Air_is_good')
# DAF_model.add_edge('Drives_x2', 'Air_is_good')
# DAF_model.add_edge('Drives_x3', 'Air_is_good')
# DAF_model.add_edge('Drives_x4', 'Air_is_good')
DAF_model.add_cpds(cpd_d1)
DAF_model.add_cpds(cpd_d2)
DAF_model.add_cpds(cpd_d3)
DAF_model.add_cpds(cpd_d4)
DAF_model.add_cpds(cpd_a)
# print(DAF_model)
DAF_model.check_model()
#      ('Drives_x4', 'Air_is_good'))
#
# # # The representation of CPD in pgmpy is a bit different than the CPD shown in the above picture. In pgmpy the colums
# # # are the evidences and rows are the states of the variable. So the grade CPD is represented like this:
# # #
# # #    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
# # #    |Drives_x1|  0  |  0  |  0  |  0  |  0  |  0  |  0  |  0  |  1  |  1  |  1  |  1  |  1  |  1  |  1  |  1  |
# # #    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
# # #    |Drives_x2|  0  |  0  |  0  |  0  |  1  |  1  |  1  |  1  |  0  |  0  |  0  |  0  |  1  |  1  |  1  |  1  |
# # #    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
# # #    |Drives_x3|  0  |  0  |  1  |  1  |  0  |  0  |  1  |  1  |  0  |  0  |  1  |  1  |  0  |  0  |  1  |  1  |
# # #    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
# # #    |Drives_x4|  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |
# # #    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
# # #    |      A    |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |  0  |  1  |
# # #    |    A_T    | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.6 | 0.8 | 0.8 | 0.8 | 0.6 | 0.8 | 0.6 | 0.6 | 0.6 |
# # #    +-----------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
# # #    |    A_F    | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.4 | 0.2 | 0.2 | 0.2 | 0.4 | 0.2 | 0.4 | 0.4 | 0.4 |
# # #    +-----------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
# # #    |  A_i_g  | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T | A_i_g_F | A_i_g_T |
# # #    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
# # #    | Fined_T |  0.3        0.1      0.3         0.1      0.3        0.1      0.8        0.1     0.8         0.1
# # #    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
# # #    | Fined_F |  0.7         0.9       0.7       0.9     0.7         0.9         0.2     0.9     0.2         0.9
# # #    +---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
# #
# # cpd_f = TabularCPD(
# #     variable='Fined', variable_card=2, values=[
# #         [
# #             0.1, 0.3, 0.1, 0.3, 0.1, 0.3, 0.1, 0.8, 0.1, 0.8], [
# #                 0.9, 0.7, 0.9, 0.7, 0.9, 0.7, 0.9, 0.2, 0.9, 0.2]], evidence=[
# #                     'Drives', 'Air_is_good'], evidence_card=[
# #                         5, 2], state_names={
# #                             'Fined': [
# #                                 True, False], 'Air_is_good': [
# #                                     True, False], 'Drives': [ '0', '1','2','3','4']})
# # DAF_model.add_cpds(cpd_d, cpd_a, cpd_f)
# DAF_model.add_cpds(cpd_d1,cpd_d2,cpd_d3,cpd_d4, cpd_a)
#
# print(DAF_model.check_model())
# print(DAF_model.to_junction_tree())
# print(f'Network with edges: {DAF_model.edges()}')
# infer = VariableElimination(DAF_model)
#
# print(infer.query(['Air_is_good']))
#
# print(infer.query(['Air_is_good','Drives_x1','Drives_x2','Drives_x3','Drives_x4']))
# import networkx as nx
# import matplotlib.pyplot as plt
# nx.draw(
#         DAF_model,
#         with_labels=True,
#         node_size=4000,
#         node_color="skyblue",
#         node_shape="o",
#         alpha=0.7,
#         linewidths=10,
#         arrowsize=20,
#
#         # arrows = bool
#     )
# plt.show()