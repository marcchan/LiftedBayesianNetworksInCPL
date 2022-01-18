from scipy.special import comb
import numpy
import re

# def str_expression_helper(condition: str, variable: str)-> str:
#     '''
#
#     :param condition:
#     :param variable:
#     :return:
#
#     To Deal with the case:
#     case 1-2: TOBEDONE in this branch
#     || A < 0.5|| & B
#     || A < 0.5 || & || B < 0.5||
#     case 3-4: TOBEDONE in branch parameter
#     || A(x) < 0.5||_x & ||B < 0.5||
#      || A(x) < 0.5||_x & ||B(x) < 0.5||_x
#
#     '''


def check_probability_from_distribution(
        card_list, distribution, p_names, state_name):
    # evi_value_dict = {p_names[i]: state_name[p_names[i]][i] for i in range(len(card_list))}
    evi_value_dict = {p_names[i]: state_name[p_names[i]][va]
                      for i, va in enumerate(card_list)}
    prob = None
    for cond, val in distribution.items():
        condition = cond
        condition = condition.replace('!', ' not ')
        condition = condition.replace(' & ', ' and ')
        condition = condition.replace(' | ', ' or ')
        for variable, value in evi_value_dict.items():
            if variable in condition:
                # print(f'{variable} : {value}')
                if isinstance(value, bool):
                    condition = condition.replace(variable, str(value))
                elif isinstance(value, int):
                    regex = re.compile(f'\\|\\|{variable}.*?\\|\\|')
                    c_list = re.findall(regex, condition)
                    if len(c_list) != 0:
                        for content in c_list:
                            value_ = str(
                                value / (len(state_name[variable]) - 1))
                            # print(content)
                            con = content.replace('||', '')
                            # print(f'con is {con}')
                            con = con.replace(variable, value_)
                            # print(f'con after {con}')
                            condition = re.sub(regex, con, condition, 1)

        # print(condition)
        if eval(condition):
            prob = val
            # print(val)
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
        if len(node.get_domain()) == 0:
            res_arr = [phi, 1 - phi]
        elif len(node.get_domain()) == 1:
            res_arr = list(setup_bino_dist(phi, node.get_variable_card() - 1).values())
            print(f'node: {node.get_name()} with values {res_arr}')
        elif len(node.get_domain()) > 1:
            # TODO friend(x,y)
            print(f'TODO for case with multi parameter in function fill_data_into_values')
        return numpy.array(res_arr).reshape(row, column)
    else:
        if len(node.get_domain()) == 0:
            cards = []
            p_names = []
            for p_name in evidence:
                p_names.append(p_name)
                cards.append(len(state_name[p_name]))
            res_matrix = numpy.zeros(cards)
            card_list = []
            res_matrix, _ = recursive_data(
                card_list, res_matrix, distribution, p_names, state_name, depth=0)
            return numpy.append(res_matrix, 1 - res_matrix, axis=0)

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
    return {index: comb(domain, index) * pow(phi, index) * pow(1 - phi,
            domain - index) for index in range(domain + 1)}
