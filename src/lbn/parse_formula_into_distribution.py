from lbn.input.network import *
from scipy.special import comb
import numpy



def fill_data_into_values(node: Node, row: int, column: int, evidences: dict, distrubutions: dict):
    # value = numpy.ndarray([row, column], numpy.float64)
    res_list = []
    # TODO conditon maybe false,  is not always with int
    if len(evidences[node.get_name()]) == 0:
        phi: float = distrubutions[node.get_name()]['self']
        if node.get_type() == 'int':
            res_list = [setup_bino_dist(phi, node.get_domain()).values()]

        elif node.get_type() == 'bool':
            res_list = [phi, 1 - phi]
    else:
        if node.get_type() == 'bool':
            res_list = []
    # print(numpy.array(res_list).reshape(row, column))
    print(row)
    print(column)
    print(res_list)
    print(numpy.array(res_list).reshape(row,column))
    return res_list


# def check_only_with_frequence(node1: Node, nodes: list) -> bool:
#     node_counter, freq_node_counter = 0, 0
#     for node in nodes:
#         if node1.get_name() != node.get_name():
#             dist_keylist = node.get_distributions().keys()
#             for dist_key in dist_keylist:
#                 node_counter += dist_key.count(node1.get_name())
#                 freq_node_counter += dist_key.count(f'||{node1.get_name()}')
#
#     return node_counter == freq_node_counter

# maybe need new a class with FreqNode
# def replace_node_to_freqnode(node, probability):
#     return


def setup_bino_dist(phi: float, domain: int) -> dict:
    '''

    :param phi: probability
    :param domain: domain number
    :return: list for index with value of array

    example: node: Drives, phi = 0.5, domain = 4
    return:[0.0625,0.25,0.375,0.25,0.0625]

    '''
    return {index:comb(domain, index) * pow(phi, index) * pow(1 - phi,
            domain - index) for index in range(domain + 1)}

# def generate_cpd_node(node: Node):
#     variable = node.get_name()
#     if len(node.get_evidences()) == 0:
#         if node.get_type() == int:
#             phi: float = node.get_distributions['self']
#             prob_dict = setup_bino_dist(phi, node.get_domain())
#             variable_card = len(prob_dict)
#             values = prob_dict.values()
#
#             return prob_dict,variable,variable_card,values
#     # else:
#     #     return {}


# def model_with_order(ordered_nodes: list):
#     for node in ordered_nodes:
#         # node without dependencies
#         # if len(node.get_evidences()) == 0:
#         #     probability: float = node.get_distributions['self']
#         #
#         #     if check_only_with_frequence(node, ordered_nodes):
#         #     #     todo setup_freq_dist()
#         #         # replace_node_to_freqnode(node, probability)
#         # else:
#         # todo
#         return


def parse_conditional_probability(distributions: dict):
    for cond,prob in distributions.items():
        # parse_condition
        return

# def
#
# def parse_condition(str: str):
#     if '|' in str:
