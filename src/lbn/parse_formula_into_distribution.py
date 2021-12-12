from lbn.input.network import *
from scipy.special import comb
import numpy
import re

def parse_conditional_probability(condition: str, value_dict: dict):
    for variable, value in value_dict.items():
        if variable in condition:
            if type(value) == bool:
                condition.replace(variable, value)
            elif type(value) == 'int' or 'float':
                if bool(re.match(r'||'+variable+'.*||')) == True:
                    return



def check_probability_from_distribution(distribution, card_list, p_names):
    evi_value_dict = {[p_names[i]] : card_list[i] for i in range(len(card_list))}
    for cond, value in distribution.item():
        return
        # parse_logic(cond)



def recursive_fill_data(res_matrix,distribution, card_list,p_names):
    for i in range(len(res_matrix)):
        card_list.append(i)
        if type(res_matrix[i]).__name__ == 'ndarray':
            res_matrix[i] =  recursive_fill_data(res_matrix[i],distribution,card_list,p_names)
        else:
            res_matrix[i] = check_probability_from_distribution(distribution,card_list,p_names)
    return res_matrix

def fill_data_into_values(node: Node, row: int, column: int, evidence: set, distrubution: dict,state_name: dict):
    if len(evidence) == 0:
        res_arr = []
        phi: float = distrubution['self']
        if node.get_type() == 'int':
            res_arr = list(setup_bino_dist(phi, node.get_domain()).values())
            print(res_arr)
        elif node.get_type() == 'bool':
            res_arr = [phi, 1 - phi]
        return numpy.array(res_arr).reshape(row, column)
    else:
        if node.get_type() == 'bool':
            cards =[]
            p_names = []
            for p_name in evidence:
                p_names.append(p_name)
                cards.append(len(state_name[p_name]))
            res_matrix = numpy.zeros(cards)
            res_matrix = recursive_fill_data(cards, res_matrix,distrubution, p_names)









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



