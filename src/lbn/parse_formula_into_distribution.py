from lbn.input.node import *
from scipy.special import comb
import numpy

def check_only_with_frequence(node1: Node, nodes: list) -> bool:
    node_counter, freq_node_counter = 0, 0
    for node in nodes:
        if node1.get_name() != node.get_name():
            dist_keylist = node.get_distributions().keys()
            for dist_key in dist_keylist:
                node_counter += dist_key.count(node1.get_name())
                freq_node_counter += dist_key.count(f'||{node1.get_name()}')

    return node_counter == freq_node_counter

# maybe need new a class with FreqNode
# def replace_node_to_freqnode(node, probability):
#     return


def setup_bino_dist(phi: float, domain: int) -> dict:
    '''

    :param phi: probability
    :param domain: domain number
    :return: dict for index with value of 2D array

    example: node: Drives, phi = 0.5, domain = 4
    return: dict: {0: [0.0625], 1: [0.25], 2: [0.375], 3: [0.25], 4: [0.0625]}

    '''
    probability_dist = {}
    for index in range(domain + 1):
        probability_dist[index] =\
            [comb(domain, index) * pow(phi, index) * pow(1 - phi, domain - index)]
    return probability_dist

def generate_cpd_node(node: Node):
    variable = node.get_name()
    if len(node.get_evidences()) == 0:
        if node.get_type() == int:
            phi: float = node.get_distributions['self']
            prob_dict = setup_bino_dist(phi, node.get_domain())
            variable_card = len(prob_dict)
            values = prob_dict.values()

            return prob_dict,variable,variable_card,values
    # else:
    #     return {}


def model_with_order(ordered_nodes: list):
    for node in ordered_nodes:
        # node without dependencies
        # if len(node.get_evidences()) == 0:
        #     probability: float = node.get_distributions['self']
        #
        #     if check_only_with_frequence(node, ordered_nodes):
        #     #     todo setup_freq_dist()
        #         # replace_node_to_freqnode(node, probability)
        # else:
        # todo
        return


def condition_from_string_to_obj():
    return


def operator_parse_to_logic():
    return

