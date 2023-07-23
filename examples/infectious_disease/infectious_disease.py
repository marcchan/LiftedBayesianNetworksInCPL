from pgmpy.inference import VariableElimination

from lbn.main import generate_bayesian_network_model

FORMULA_FILE = 'formula'
# FORMULA_FILE = 'formula_v1'
DOMAIN_FILE = 'domain'

# Using Pre-Computing when pre-computing_flag is True
# Using node Lifting when  node_lifing_flag is True
# Grounding when node_lifting_flay = False
lbn_model = generate_bayesian_network_model(FORMULA_FILE,DOMAIN_FILE,
            pre_computing_flag= True, node_lifing_flag= False)

# inferences
inference = VariableElimination(lbn_model)
# margin probability
margin_prob = inference.query(['IsShutDown_w1'])
print(margin_prob)