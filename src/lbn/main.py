# from lbn.input.node import *
# from lbn.input.formula import *
# from lbn import *
# from lbn.parse_formula_into_distribution import *
#
#
# # main
# # read nodes with distributions into node list objects
# for node in nodes:
#     set_evidences_from_distributions(node)
#     # evidences_dict[node.get_name()] = node.get_evidences()
#     print(node)
#
# # order for the nodes to set up the BN model
# # ordered_nodes = get_ordered_nodes(nodes)
# # print(nodes)
# # print(ordered_nodes)
# # prob_dict,variable,variable_card,values= generate_cpd_node(ordered_nodes[0])
# #
# # state_names = {}
# # state_names[variable] = prob_dict.keys()
# # from pgmpy.models import BayesianNetwork
# # from pgmpy.factors.discrete import TabularCPD
# # cpd_d = TabularCPD(
# #     variable= variable,
# #     variable_card=variable_card,
# #     values=values,
# #     state_names=state_names)
# # print(cpd_d.get_values())



from lbn.input.world import *

FORMULA_FILE = '../../examples/example_formula'
Domain_FILE = '../../examples/node_domain'


nodes = World(FORMULA_FILE,Domain_FILE).get_nodes()
[print(i) for i in nodes]