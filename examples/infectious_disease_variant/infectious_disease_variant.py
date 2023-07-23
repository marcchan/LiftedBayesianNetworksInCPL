from pgmpy.inference import VariableElimination

from lbn.main import generate_bayesian_network_model
# from lbn.network_helper import parse_to_network

FORMULA_FILE = 'formula_unideal_case'
# FORMULA_FILE = 'formula_ordinary_case'
DOMAIN_FILE = 'domain_unideal_case'
# DOMAIN_FILE = 'domain_ordinary_case'

# In those two case pre-computing do not make sense
lbn_model = generate_bayesian_network_model(FORMULA_FILE,DOMAIN_FILE,
            pre_computing_flag= False, node_lifing_flag= True)

# inferences
inference = VariableElimination(lbn_model)
# margin probability
# margin_prob = inference.query(['IsShutDown'])
margin_prob = inference.query(['AllPeopleRemoteWorking'])
print(margin_prob)

# joint probability
# joint_prob = inference.query(['IsShutDown', 'AllPeopleRemoteWorking'])
# print(joint_prob)
