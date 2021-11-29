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

# setup cpdnodes