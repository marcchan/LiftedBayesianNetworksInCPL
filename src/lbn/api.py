from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

from lbn.network_helper import *

# FORMULA_FILE = '../../examples/attend_grade_school/formula_v2'
# Domain_FILE = '../../examples/attend_grade_school/domain_v1'
FORMULA_FILE = '../../examples/drives_air_fined/formula_v2'
Domain_FILE = '../../examples/drives_air_fined/domain_v1'
# FORMULA_FILE = '../../examples/pre_computing_case/temp_3'
# Domain_FILE = '../../examples/pre_computing_case/domain'

def generate_bn_model(file_path_formula: str, file_path_domain: str):

    network = parse_to_network(file_path_formula, file_path_domain)

    # generate the complete Baysian network
    generate_bayesian_network(network)
    nodes = network.get_nodes()

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
    return BN_model


if __name__ == "__main__":

    BN_model = generate_bn_model(FORMULA_FILE,Domain_FILE)
    infer = VariableElimination(BN_model)

    # # Drives
    #
    # # margin probability
    #
    # print(infer.query(["Fined"]))
    # # a = infer.query(["Fined"]).get_value(Fined=True)
    # # print(a)
    #
    #
    # # conditional probability
    # print(infer.query(["Fined"], evidence={"AirIsGood": True}))
    #
    # # joint probability
    # print(infer.query(["Fined", "Drives", "AirIsGood"]))


    # # School
    # print(infer.query(["Attends"]))
    # print(infer.query(["GoodGrade"]))
    # print(infer.query(["SchoolGood"]))
    # # conditional probability
    # print(infer.query(["SchoolGood"], evidence={"GoodGrade": 0,"Attends":0}))
    # # joint probability
    # print(infer.query(["Attends", "GoodGrade", "SchoolGood"]))

    # pre_computing
    # print(infer.query(["GoodGrade"]))
    print(BN_model.get_independencies())