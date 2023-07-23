from pgmpy.inference import VariableElimination

from lbn.main import generate_bayesian_network_model

FORMULA_FILE = 'formula'
DOMAIN_FILE = 'domain'

# Using Pre-Computing when pre-computing_flag is True
# Using node Lifting when  node_lifing_flag is False
lbn_model = generate_bayesian_network_model(FORMULA_FILE,DOMAIN_FILE,
            pre_computing_flag= True, node_lifing_flag= True)

# inferences
inference = VariableElimination(lbn_model)
# margin probability
margin_prob = inference.query(['CityRatingDrop'])
print(margin_prob)
# joint probability
# joint_prob = inference.query([ 'Drive', 'CityRatingDrop'])
# print(joint_prob)