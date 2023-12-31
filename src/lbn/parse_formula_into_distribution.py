# from scipy.special import comb
# import numpy
# import re
# from lbn.input.node import Node
# from itertools import product
# from scipy.stats import binom
#
# def get_node_from_nodes(variable: str, nodes: list) -> Node:
#     for node in nodes:
#         if node.get_name() == variable:
#             return node
#     print(f'nodes do not contain the node with the name: {variable}')
#
#
# def str_expression_helper(
#         cond: str,
#         evi_value_dict: dict,
#         state_name: dict,
#         nodes: list) -> str:
#     """
#     To Deal with the case:
#     case 1-2: TOBEDONE in this branch
#     || A < 0.5|| & B
#     || A < 0.5 || & || B < 0.5||
#     case 3-4: TOBEDONE in branch parameter
#     || A(x) < 0.5||_x & ||B < 0.5||
#      || A(x) < 0.5||_x & ||B(x) < 0.5||_x
#     ||A(x,y) <0.5||_x_y
#     """
#     # print('----')
#     # print(cond)
#     # print(evi_value_dict)
#     # print(f'statename: {state_name}')
#     # parse the math symbol into program logical symbol
#     condition = cond.replace(
#         '!',
#         ' not ').replace(
#         ' & ',
#         ' and ').replace(
#             ' | ',
#         ' or ')
#     freq_list = re.findall(r'\|\|.*?\|\|[\w]*', condition)
#
#     """
#     for case:
#     ||A(x) > 0.5||_x
#     B & || A(x) > 0.5||_x
#     ||A(x) > 0.5||_x & ||B(x) > 0.5||_x
#     exception ||A | B(x)||_x two variable in one freq
#     """
#     for variable, value in evi_value_dict.items():
#         # count: count of variable in single condition
#         # count_in_freq: count of variable in ||...||
#         count = condition.count(variable)
#         count_in_freq = sum(variable in s for s in freq_list)
#         cur_node = get_node_from_nodes(variable, nodes)
#
#         """
#         example: ||A(x) > 0.5||_x
#         variable_para: (x)。
#         variable_suffix: _x
#         """
#         variable_para, variable_suffix = cur_node.get_lower_para_from_node()
#         freq_list_copy = list(freq_list)
#         # value in frequence, example: ||A(1)||_4: value= 1/4
#         freq_value = str(value / (len(state_name[variable]) - 1))
#         # compare variable count in condition with variable count in frequency
#         # area ||...||
#         if count < count_in_freq:
#             print(
#                 f'error in count variable:{variable} with freq and all condition')
#         # count >= count_in_freq
#         else:
#             # condition doesn't contain this variable
#             if count == count_in_freq == 0:
#                 pass
#             # count >= count_in_freq >= 0, count > 0
#             # example:
#             #  * ||A(x) > 0.5||_x
#             #  * ||A & B(x) > 0.5||_x

#             else:
#                 if count_in_freq > 0:
#                     # first replace the variable as value in ||...||
#                     for idx, freq in enumerate(freq_list):
#                         # || A & B(x)||_x change A

#                         # if len(variable_para) == 0:

#                         #     freq_list_copy[idx] = str.replace(freq_list_copy[idx], variable, str(value))
#
#                         # || A & B(x)||_x change B:   len(para) = (x) and B(x) in freq
#                         if len(
#                                 variable_para) != 0 and f'{variable}{variable_para}' in freq:
#                             # print(freq_list_copy[idx])
#                             # remove suffix: i.e. _x_y
#                             freq_list_copy[idx] = str.replace(
#                                 freq_list_copy[idx], variable_suffix, '')
#                             # remove freq mark: i.e. ||     ||
#                             freq_list_copy[idx] = str.replace(
#                                 freq_list_copy[idx], '||', '')
#                             freq_list_copy[idx] = str.replace(
#                                 freq_list_copy[idx], f'{variable}{variable_para}', freq_value)
#                             # print(freq_list_copy[idx])
#                             condition = condition.replace(
#                                 freq_list[idx], freq_list_copy[idx])
#                 # then replace in 2 cases:
#                 #   * variable as value without ||...||, example: A & ||B(x) > 0.5||_x for variable A
#                 #   * ||A & B(x) > 0.5||_x maybe not necessary
#                 condition = condition.replace(variable, str(value))
#
#     # print(condition)
#     # print('---')
#     return condition
#
# def check_probability_from_distribution(
#         card_list, distribution, p_names, state_name, nodes):
#     evi_value_dict = {p_names[i]: state_name[p_names[i]][va]
#                       for i, va in enumerate(card_list)}
#     prob = None
#     for cond, val in distribution.items():
#         str_expression = str_expression_helper(
#             cond, evi_value_dict, state_name, nodes)
#         print(str_expression)
#         if eval(str_expression):
#             prob = val
#             return prob
#     if prob is None:
#         return -1
#
# def recursive_data(
#         card_list,
#         res_matrix,
#         distribution,
#         p_names,
#         state_name, depth, nodes):
#     for i in range(len(res_matrix)):
#         if type(res_matrix[i]).__name__ == 'ndarray':
#             # in different value example [0,0][0,1] -> [1,0] [1,1]
#             if len(card_list) != depth:
#                 card_list[depth] = i
#                 depth += 1
#             else:
#                 card_list.append(i)
#                 depth += 1
#             res_matrix[i], depth = recursive_data(
#                 card_list, res_matrix[i], distribution, p_names, state_name, depth, nodes)
#         else:
#             if len(card_list) != depth + 1:
#                 card_list.append(i)
#             else:
#                 card_list[depth] = i
#             # for test
#             # res_matrix[i] = 1
#             res_matrix[i] = check_probability_from_distribution(
#                 card_list, distribution, p_names, state_name, nodes)
#     depth -= 1
#     return res_matrix, depth
#
# def fill_data_into_values(
#         node,
#         row: int,
#         column: int,
#         evidence: set,
#         distribution: dict,
#         state_name: dict,
#         nodes: list):

#     if len(evidence) == 0:
#         res_arr = []
#         phi: float = float(distribution['self'])
#         if len(node.get_domain()) == 0:
#             res_arr = [phi, 1 - phi]
#         elif len(node.get_domain()) == 1:
#             res_arr = list(
#                 setup_bino_dist(
#                     phi,
#                     node.get_variable_card() -
#                     1).values())
#             print(f'node: {node.get_name()} with values {res_arr}')
#         elif len(node.get_domain()) > 1:
#

#         return numpy.array(res_arr).reshape(row, column)
#     else:
#         if len(node.get_domain()) == 0:
#             cards = []
#             p_names = []
#             for p_name in evidence:
#                 p_names.append(p_name)
#                 cards.append(len(state_name[p_name]))
#             res_matrix = numpy.zeros(cards)
#             card_list = []
#             res_matrix, _ = recursive_data(
#                 card_list, res_matrix, distribution, p_names, state_name, depth=0, nodes=nodes)
#             print(f'{res_matrix}')
#             return numpy.append(res_matrix, 1 - res_matrix, axis=0)
#         elif len(node.get_domain()) == 1:
#             cards = []
#             p_names = []
#             for p_name in evidence:
#                 p_names.append(p_name)
#                 cards.append(len(state_name[p_name]))
#             res_matrix = numpy.zeros(cards)
#             card_list = []
#             res_matrix, _ = recursive_data(
#                 card_list, res_matrix, distribution, p_names, state_name, depth=0, nodes=nodes)
#             k = numpy.arange(row)
#             result = numpy.zeros((row, len(res_matrix)))
#             for i, p in enumerate(res_matrix):
#                 result[:, i] = binom.pmf(k, row-1, p)
#             return result
#         else:
#             # must consider the case (x,y)
#             pass
#
#
#
#
# def fill_data_into_values_two(
#         node,
#         row: int,
#         column: int,
#         evidence: set,
#         distribution: dict,
#         state_name: dict,
#         nodes: list):

#     if len(evidence) == 0:
#         res_arr = []
#         phi: float = float(distribution['self'])
#         if len(node.get_domain()) == 0 or 1:
#             res_arr = [phi]
#         elif len(node.get_domain()) > 1:
#         return numpy.array(res_arr)
#     else:
#         if len(node.get_domain()) == 0:
#             cards = []
#             p_names = []
#             for p_name in evidence:
#                 p_names.append(p_name)
#                 cards.append(len(state_name[p_name]))
#             res_matrix = numpy.zeros(1,column)
#             card_list = []
#             res_matrix, _ = recursive_data(
#                 card_list, res_matrix, distribution, p_names, state_name, depth=0, nodes=nodes)
#             # print(f'{res_matrix}')
#             return numpy.append(res_matrix)
#         elif len(node.get_domain()) == 1:
#             cards = []
#             p_names = []
#             for p_name in evidence:
#                 p_names.append(p_name)
#                 cards.append(len(state_name[p_name]))
#             res_matrix = numpy.zeros(1, column)
#             card_list = []
#             res_matrix, _ = recursive_data(
#                 card_list, res_matrix, distribution, p_names, state_name, depth=0, nodes=nodes)
#             k = numpy.arange(row)
#             result = numpy.append(res_matrix)
#             return result
#         else:
#             # must consider the case (x,y)
#             pass
#
#
#
#
# def setup_bino_dist(phi: float, domain: int) -> dict:
#     return {index: comb(domain, index) * pow(phi, index) *
#             pow(1 - phi, domain - index) for index in range(domain + 1)}
#
#
# def fill_true_data():
#     def enumerate_key_value(d):
#         keys = list(d.keys())
#         value_lists = list(d.values())
#         combinations = product(*value_lists)
#         for combination in combinations:
#             yield dict(zip(keys, combination))
#
#     for result in enumerate_key_value():
#         pass
#
