from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

from lbn.input.network import *

FORMULA_FILE = '../../examples/attend_grade_school/formula_v1'
Domain_FILE = '../../examples/attend_grade_school/domain_v1'
# FORMULA_FILE = '../../examples/drives_air_fined/formula_v1'
# Domain_FILE = '../../examples/drives_air_fined/domain_v1'

def generate_bn_model(file_path_formula: str, file_path_domain: str):

    network = Network(file_path_formula, file_path_domain)

    # generate the complete Baysian network
    network.generate_bayesian_network()
    nodes = network.get_nodes()

    # setup bayesian network
    BN_model = BayesianNetwork(network.get_edges())
    # tabular_cpd_nodes = []
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
        # tabular_cpd_nodes.append(cpd_node)
        BN_model.add_cpds(cpd_node)
    return BN_model


if __name__ == "__main__":

    BN_model = generate_bn_model(FORMULA_FILE,Domain_FILE)
    infer = VariableElimination(BN_model)

    # Drives

    # margin probability

    # print(infer.query(["Fined"]))

    # a = infer.query(["Fined"]).get_value(Fined=True)
    # print(a)


    # conditional probability
    # print(infer.query(["Fined"], evidence={"Air_is_good": False}))

    # joint probability
    # print(infer.query(["Fined", "Drives", "Air_is_good"]))


    # School
    # print(infer.query(["attends"]))
    # print(infer.query(["good_grade"]))
    print(infer.query(["school_good"]))
    # conditional probability
    # print(infer.query(["school_good"], evidence={"good_grade": 0,"attends":0}))
