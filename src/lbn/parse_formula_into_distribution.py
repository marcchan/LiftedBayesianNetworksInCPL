# from lbn.input.network import *
from scipy.special import comb
import numpy
import re


# def parse_conditional_probability(condition: str, val, value_dict: dict,state_name):
#     for variable, value in value_dict.items():
#         if '!' in condition:
#             condition.replace('!','not')
#         if variable in condition:
#             if type(value) == bool:
#                 condition.replace(variable, value)
#             elif type(value) == 'int' or 'float':
#                 if bool(re.match(r'||'+variable+'.*||')) == True:
#                         # [0,1,2,3,4]  5-1 = 4
#                         value_ = value / (len(state_name[variable]) -1)
#                         condition = re.sub(variable,value_,condition)
#                         condition = re.sub('||','', condition)
#     if eval(condition):
#         return


def check_probability_from_distribution(
        card_list, distribution, p_names, state_name):
    evi_value_dict = {p_names[i]: card_list[i] for i in range(len(card_list))}
    prob = None
    for cond, val in distribution.items():
        condition = cond
        if '!' in condition:
            condition.replace('!', 'not')
        for variable, value in evi_value_dict.items():
            if variable in condition:
                if isinstance(value, bool):
                    condition.replace(variable, value)
                elif isinstance(value, int):
                    if bool(
                        re.search(
                            r'.*\|\|' +
                            variable +
                            '.*\\|\\|',
                            condition)):
                        # [0,1,2,3,4]  5-1 = 4
                        value_ = str(value / (len(state_name[variable]) - 1))
                        condition = re.sub('\\|\\|', '', condition)
                        print(f'Drives or variable is {value}\n')
                        print(value_)
                        print(condition)
                        print(variable)
                        condition = re.sub(variable, value_, condition)
                        # condition.replace(variable,value_)
        print(condition)
        if eval(condition):
            prob = val
            print(val)
            return prob
    if prob is None:
        return -1


def recursive_data(
        card_list,
        res_matrix,
        distribution,
        p_names,
        state_name, depth):
    for i in range(len(res_matrix)):
        if type(res_matrix[i]).__name__ == 'ndarray':
            # in different value example [0,0][0,1] -> [1,0] [1,1]
            if len(card_list) != depth:
                card_list[depth] = i
                depth += 1
            else:
                card_list.append(i)
                depth += 1
            res_matrix[i], depth = recursive_data(
                card_list, res_matrix[i], distribution, p_names, state_name, depth)
        else:
            if len(card_list) != depth + 1:
                card_list.append(i)
            else:
                card_list[depth] = i
            # for test
            # res_matrix[i] = 1
            res_matrix[i] = check_probability_from_distribution(
                card_list, distribution, p_names, state_name)
    depth -= 1

    return res_matrix, depth


def fill_data_into_values(
        node,
        row: int,
        column: int,
        evidence: set,
        distribution: dict,
        state_name: dict):
    if len(evidence) == 0:
        res_arr = []
        phi: float = distribution['self']
        if node.get_type() == 'int':
            res_arr = list(setup_bino_dist(phi, node.get_domain()).values())
            print(res_arr)

        # TODO friend(x,y)
        elif node.get_type() == 'bool':
            res_arr = [phi, 1 - phi]
        return numpy.array(res_arr).reshape(row, column)
    else:
        if node.get_type() == 'bool':
            cards = []
            p_names = []
            for p_name in evidence:
                p_names.append(p_name)
                cards.append(len(state_name[p_name]))
            res_matrix = numpy.zeros(cards)
            card_list = []
            res_matrix = recursive_data(
                card_list, res_matrix, distribution, p_names, state_name,depth=0)
            print(res_matrix)
    return

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
    return {index: comb(domain, index) * pow(phi, index) * pow(1 - phi,
            domain - index) for index in range(domain + 1)}
