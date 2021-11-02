from lbn.input.node import Node, init_nodes_from_json
from pgmpy.models import BayesianNetwork


# import nodes obj
nodes =init_nodes_from_json('../../examples/node_domain')
# import formula
# cancer_model = BayesianNetwork([('Pollution', 'Cancer'),
#                               ('Smoker', 'Cancer'),
#                               ('Cancer', 'Xray'),
#                               ('Cancer', 'Dyspnoea')])
#
# from pgmpy.factors.discrete import TabularCPD
#
# cpd_poll = TabularCPD(variable='Pollution', variable_card=2,
#                       values=[[0.9], [0.1]])
# cpd_smoke = TabularCPD(variable='Smoker', variable_card=2,
#                        values=[[0.3], [0.7]])
# cpd_cancer = TabularCPD(variable='Cancer', variable_card=2,
#                         values=[[0.03, 0.05, 0.001, 0.02],
#                                 [0.97, 0.95, 0.999, 0.98]],
#                         evidence=['Smoker', 'Pollution'],
#                         evidence_card=[2, 2])
# cpd_xray = TabularCPD(variable='Xray', variable_card=2,
#                       values=[[0.9, 0.2], [0.1, 0.8]],
#                       evidence=['Cancer'], evidence_card=[2])
# cpd_dysp = TabularCPD(variable='Dyspnoea', variable_card=2,
#                       values=[[0.65, 0.3], [0.35, 0.7]],
#                       evidence=['Cancer'], evidence_card=[2])
#
# # Associating the parameters with the model structure.
# cancer_model.add_cpds(cpd_poll, cpd_smoke, cpd_cancer, cpd_xray, cpd_dysp)
#
# # Checking if the cpds are valid for the model.
# cancer_model.check_model()
#
# # Check for d-separation between variables
# print(cancer_model.is_dconnected('Pollution', 'Smoker'))
# print(cancer_model.is_dconnected('Pollution', 'Smoker', observed=['Cancer']))
#
# # Get all d-connected nodes
#
# cancer_model.active_trail_nodes('Pollution')
#
# # List local independencies for a node
#
# cancer_model.local_independencies('Xray')
#
# # Get all model implied independence conditions
#
# cancer_model.get_independencies()


# from pgmpy.utils import get_example_model
#
# model = get_example_model('cancer')
# print("Nodes in the model:", model.nodes())
# print("Edges in the model:", model.edges())
# model.get_cpds()
