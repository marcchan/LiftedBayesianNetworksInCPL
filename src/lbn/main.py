from functools import reduce
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork
import re
import datetime
import time
# from lbn.parse_formula_into_distribution import fill_data_into_values, fill_data_into_values_two
from lbn.network_helper import set_network_edges, set_network_statenames, set_network_variable_card, parse_to_network
from lbn.pre_computing import PreComputing
from lbn.grounding import Grounding

# def set_network_values(network):
#     """
#     :return: None
#     Values: 2D array
#         Drives row = 5, col = 1
#         Air_is_good row = 2, col = 5
#         Fined row = 2, col = 5 * 2
#     """
#     values = {}
#     for node in network.get_nodes():
#         print(f'current node is {node.get_name()}')
#         row = network.get_variable_card_by_name(node.get_name())
#         # maybe has problem
#         column: int = reduce(
#             lambda x,
#             y: x * y,
#             network.get_evidence_card_by_name(
#                 node.get_name())) if network.get_evidence_list_by_name(
#             node.get_name()) is not None else 1
#         print(f'row is:{row}, column is:{column}')
#         temp_value = fill_data_into_values(
#             node, row, column, network.get_evidences()[
#                 node.get_name()], network.get_distributions()[
#                 node.get_name()], network.get_state_names_by_name(
#                 node.get_name()), network.get_nodes())
#         print(f'temp_value is {temp_value}')
#         if temp_value is not None:
#             print(
#                 f'nodename: {node.get_name()} has the value of{temp_value.reshape(row, column)}')
#         else:
#             print(f'nodename: {node.get_name()} can not get the value')
#         values[node.get_name()] = temp_value.reshape(row, column)
#
#
#     network.set_values(values)
#
# def set_network_basic_values(network):

#     """
#     :return: None
#     Values: 2D array
#         Drives row = 5, col = 1
#         Air_is_good row = 2, col = 5
#         Fined row = 2, col = 5 * 2
#     """
#     values = {}
#     for node in network.get_nodes():
#         print(f'current node is {node.get_name()}')
#         row = network.get_variable_card_by_name(node.get_name())
#         # maybe has problem
#         column: int = reduce(
#             lambda x,
#             y: x * y,
#             network.get_evidence_card_by_name(
#                 node.get_name())) if network.get_evidence_list_by_name(
#             node.get_name()) is not None else 1
#         print(f'row is:{row}, column is:{column}')
#         temp_value = fill_data_into_values_two(
#             node, row, column, network.get_evidences()[
#                 node.get_name()], network.get_distributions()[
#                 node.get_name()], network.get_state_names_by_name(
#                 node.get_name()), network.get_nodes())
#         print(f'temp_value is {temp_value}')
#         if temp_value is not None:
#             print(
#                 f'nodename: {node.get_name()} has the value of{temp_value.reshape(1, column)}')
#         else:
#             print(f'nodename: {node.get_name()} can not get the value')
#         values[node.get_name()] = temp_value.reshape(1,column)
#     return values
# def generate_bayesian_network(network):
#     set_network_edges(network)
#     if network.get_nodes() is not None:
#         print('--- PREPARE GENERATE BAYSIAN NETWORK------\n')
#         set_network_variable_card(network)
#         print(f'network variable_card is {network.get_variable_card()}')
#         set_network_statenames(network)
#         # print(set_network_basic_values(network))
#         print(set_network_values(network))
#         print('---------')
#
#         BN_model = BayesianNetwork(network.get_edges())
#         for node in network.get_nodes():
#             variable = node.get_name()
#             variable_card = network.get_variable_card_by_name(node.get_name())
#             values = network.get_values_by_name(node.get_name())
#             evidence = network.get_evidence_list_by_name(node.get_name())
#             evidence_card = network.get_evidence_card_by_name(node.get_name())
#             state_names = network.get_state_names_by_name(node.get_name())
#             cpd_node = TabularCPD(
#                 variable,
#                 variable_card,
#                 values,
#                 evidence,
#                 evidence_card,
#                 state_names)
#             BN_model.add_cpds(cpd_node)
#             print(
#                 f'{variable} with variable_card:{variable_card}, evidence:{evidence},evi_card:{evidence_card}, state_names:{state_names}')
#         return BN_model
#     # lbn = Grounding(network)

def generate_bayesian_network_model(formula_file: str, domain_file:str, pre_computing_flag:bool, node_lifing_flag: bool, basic_grounding_flag: bool = False):
    # build abstract network for LBN-CPL
    abstract_lbn = parse_to_network(formula_file,domain_file)

    # pre-computing depends on the pre-computing flag
    if pre_computing_flag:
        abstract_lbn = PreComputing(abstract_lbn).optimize_network()
        print(f'the new network from Pre-Computing is {abstract_lbn}')

    # grounding to build bayesian networks model using PGMPY
    lbn_model = Grounding(abstract_lbn,node_lifing_flag,basic_grounding_flag).build_LBN()
    return lbn_model




if __name__ == "__main__":

    # FORMULA_FILE = '../../examples/drive_air_city/formula'
    # DOMAIN_FILE = '../../examples/drive_air_city/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/domain'
    FORMULA_FILE = '../../examples/infectious_disease/formula'
    DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/DAF_v2/formula'
    # DOMAIN_FILE = '../../examples/DAF_v2/domain'
    # FORMULA_FILE = '../../examples/good_teacher/formula'
    # DOMAIN_FILE = '../../examples/good_teacher/domain'

    lbn_model = generate_bayesian_network_model(FORMULA_FILE,DOMAIN_FILE,pre_computing_flag= False, node_lifing_flag= False, basic_grounding_flag= False)
    starttime = datetime.datetime.now()
    infer = VariableElimination(lbn_model)
    # print(infer.query(["CityRatingDrop"]))
    endtime = datetime.datetime.now()
    print(endtime - starttime)


