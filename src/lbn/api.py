from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork
from main import generate_bayesian_network

from lbn.network_helper import *

# FORMULA_FILE = '../../examples/attend_grade_school/formula'
# Domain_FILE = '../../examples/attend_grade_school/domain'
FORMULA_FILE = '../../examples/drive_air_city/formula'
Domain_FILE = '../../examples/drive_air_city/domain'

# FORMULA_FILE = '../../examples/drive_air_city/test/formula'
# Domain_FILE = '../../examples/drive_air_city/test/domain'

# FORMULA_FILE = '../../examples/pre_computing_case/temp_3'
# FORMULA_FILE = '../../examples/pre_computing_case/temp_3'
# Domain_FILE = '../../examples/pre_computing_case/domain'

# FORMULA_FILE = '../../examples/test_two_network/formula'
# Domain_FILE = '../../examples/test_two_network/domain'

# FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/formula'
# Domain_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/domain'
def generate_bn_model(file_path_formula: str, file_path_domain: str):

    network = parse_to_network(file_path_formula, file_path_domain)
    set_network_edges(network)
    # generate the complete Baysian network
    generate_bayesian_network(network)
    nodes = network.get_nodes()
    # edges, freq_edges = network.get_edges(), network.get_freq_edges()
    # non_freq_edges = list(set(edges).difference(set(freq_edges)))
    # print(f'{non_freq_edges}---------')
    # setup bayesian network
    BN_model = BayesianNetwork(network.get_edges())
    for node in nodes:
        variable = node.get_name()
        variable_card = network.get_variable_card_by_name(node.get_name())
        values = network.get_values_by_name(node.get_name())
        evidence = network.get_evidence_list_by_name(node.get_name())
        evidence_card = network.get_evidence_card_by_name(node.get_name())
        state_names = network.get_state_names_by_name(node.get_name())
        cpd_node = TabularCPD(
            variable,
            variable_card,
            values,
            evidence,
            evidence_card,
            state_names)
        BN_model.add_cpds(cpd_node)
        print(f'{variable} with variable_card:{variable_card}, evidence:{evidence},evi_card:{evidence_card}, state_names:{state_names}')
    return BN_model


if __name__ == "__main__":

    BN_model = generate_bn_model(FORMULA_FILE,Domain_FILE)
    # BN_model.check_model()
    # BN_model = BayesianNetwork.load('model_file')
    # print(BN_model.check_model())
    infer = VariableElimination(BN_model)

    # # Drives
    #
    # # margin probability
    #
    # print(infer.query(["H"]))
    # # a = infer.query(["Fined"]).get_value(Fined=True)
    # # print(a)
    #
    #
    print(f'P(Fined):')
    print(infer.query(["Fined"]))
    print('\n')
    # conditional probability
    # print(f'P(Fined | Drives = True):')
    # print(infer.query(["Fined"], evidence={"Drives": True}))
    print('\n')
    #
    # # joint probability
    print(infer.query(["Fined", "Drives"]))


    # # School
    # print(infer.query(["Attends"]))
    # print(infer.query(["GoodGrade"]))
    # print(infer.query(["SchoolGood"]))
    # # conditional probability
    # print(infer.query(["SchoolGood"], evidence={"GoodGrade": 0,"Attends":0}))
    # print(infer.query(["GoodGrade"], evidence={"Attends": 0}))
    # print(infer.query(["GoodGrade"], evidence={"Attends": 1}))
    # print(infer.query(["GoodGrade"], evidence={"Attends": 2}))
    # # joint probability
    # print(infer.query(["Attends", "GoodGrade", "SchoolGood"]))

    # pre_computing
    # print(infer.query(["GoodGrade"]))
    # print(BN_model.get_independencies())