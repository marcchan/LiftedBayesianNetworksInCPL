from lbn.input.network import *
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

FORMULA_FILE = '../../examples/example_formula'
Domain_FILE = '../../examples/node_domain'

# generate the complete network nodes
network = Network(FORMULA_FILE, Domain_FILE)
nodes = network.get_nodes()

# setup bayesian network
DAF_model = BayesianNetwork(network.get_edges())
# tabular_cpd_nodes = []
for node in nodes:
    variable = node.get_name()
    variable_card = network.get_variable_card_by_name(node.get_name())
    values = network.get_values_by_name(node.get_name())
    evidence = network.get_evidence_list_by_name(node.get_name())
    evidence_card = network.get_evidence_card_by_name(node.get_name())
    state_names = network.get_state_names_by_name(node.get_name())
    cpd_node = TabularCPD(variable, variable_card, values, evidence, evidence_card, state_names)
    # tabular_cpd_nodes.append(cpd_node)
    DAF_model.add_cpds(cpd_node)

print(f'Network with edges: {DAF_model.edges()}')
infer = VariableElimination(DAF_model)
# margin probability
print(infer.query(["Fined"]))
# conditional probability
print(infer.query(["Fined"], evidence={"Air_is_good": False}))
# joint probability
print(infer.query(["Fined","Drives","Air_is_good"]))