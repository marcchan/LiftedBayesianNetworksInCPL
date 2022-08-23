from scipy.special import comb
import numpy
import re
from lbn.input.node import Node
from network_helper import get_lower_para_from_node


def get_node_from_nodes(variable: str, nodes: list) -> Node:
    # todo delete refactor by get_node_from_nodes()...
    for node in nodes:
        if node.get_name() == variable:
            return node
    print(f'nodes do not contain the node with the name: {variable}')


def str_expression_helper(
        cond: str,
        evi_value_dict: dict,
        state_name: dict,
        nodes: list) -> str:
    """
    To Deal with the case:
    case 1-2: TOBEDONE in this branch
    || A < 0.5|| & B
    || A < 0.5 || & || B < 0.5||
    case 3-4: TOBEDONE in branch parameter
    || A(x) < 0.5||_x & ||B < 0.5||
     || A(x) < 0.5||_x & ||B(x) < 0.5||_x
    ||A(x,y) <0.5||_x_y
    """
    print('----')
    print(cond)
    print(evi_value_dict)
    print(f'statename: {state_name}')
    # parse the math symbol into program logical symbol
    condition = cond.replace(
        '!',
        ' not ').replace(
        ' & ',
        ' and ').replace(
            ' | ',
        ' or ')
    freq_list = re.findall(r'\|\|.*?\|\|[\w]*', condition)

    """
    for case:
    ||A(x) > 0.5||_x
    B & || A(x) > 0.5||_x
    ||A(x) > 0.5||_x & ||B(x) > 0.5||_x
    exception ||A | B(x)||_x two variable in one freq
    """
    for variable, value in evi_value_dict.items():
        # count: count of variable in single condition
        # count_in_freq: count of variable in ||...||
        count = condition.count(variable)
        count_in_freq = sum(variable in s for s in freq_list)
        cur_node = get_node_from_nodes(variable, nodes)

        """
        example: ||A(x) > 0.5||_x
        variable_para: (x)
        variable_suffix: _x
        """
        variable_para, variable_suffix = get_lower_para_from_node(cur_node)
        freq_list_copy = list(freq_list)
        # value in frequence, example: ||A(1)||_4: value= 1/4
        freq_value = str(value / (len(state_name[variable]) - 1))
        # compare variable count in condition with variable count in frequency
        # area ||...||
        if count < count_in_freq:
            print(
                f'error in count variable:{variable} with freq and all condition')
        # count >= count_in_freq
        else:
            # condition doesn't contain this variable
            if count == count_in_freq == 0:
                pass
            # count >= count_in_freq >= 0, count > 0
            # example:
            #  * ||A(x) > 0.5||_x
            #  * ||A & B(x) > 0.5||_x
            # todo ||A(x) | B(x,y)>0.5||_y in next spring
            else:
                if count_in_freq > 0:
                    # first replace the variable as value in ||...||
                    for idx, freq in enumerate(freq_list):
                        # || A & B(x)||_x change A
                        # # todo maybe not necessary
                        # if len(variable_para) == 0:
                        # #     todo check the replace value
                        #     freq_list_copy[idx] = str.replace(freq_list_copy[idx], variable, str(value))

                        # || A & B(x)||_x change B:   len(para) = (x) and B(x) in freq
                        if len(
                                variable_para) != 0 and f'{variable}{variable_para}' in freq:
                            # print(freq_list_copy[idx])
                            # remove suffix: i.e. _x_y
                            freq_list_copy[idx] = str.replace(
                                freq_list_copy[idx], variable_suffix, '')
                            # remove freq mark: i.e. ||     ||
                            freq_list_copy[idx] = str.replace(
                                freq_list_copy[idx], '||', '')
                            freq_list_copy[idx] = str.replace(
                                freq_list_copy[idx], f'{variable}{variable_para}', freq_value)
                            # print(freq_list_copy[idx])
                            condition = condition.replace(
                                freq_list[idx], freq_list_copy[idx])
                # then replace in 2 cases:
                #   * variable as value without ||...||, example: A & ||B(x) > 0.5||_x for variable A
                #   * ||A & B(x) > 0.5||_x maybe not necessary
                condition = condition.replace(variable, str(value))
    # iteration evidence variable and value
    # for variable, value in evi_value_dict.items():
    #     if variable in condition:
    #         print(f'{variable} : {value}')
    # if isinstance(value, bool):
    #     condition = condition.replace(variable, str(value))
    # elif isinstance(value, int):
    #     regex = re.compile(f'\\|\\|{variable}.*?\\|\\|')
    #     c_list = re.findall(regex, condition)
    #     if len(c_list) != 0:
    #         for content in c_list:
    #             value_ = str(
    #                 value / (len(state_name[variable]) - 1))
    #             # print(content)
    #             con = content.replace('||', '')
    #             # print(f'con is {con}')
    #             con = con.replace(variable, value_)
    #             # print(f'con after {con}')
    #             condition = re.sub(regex, con, condition, 1)

    # if isinstance(value, bool):
    #     condition = condition.replace(variable, str(value))
    # elif isinstance(value, int):

    # still has problem : || A and B(x,y) < 0.5||_x_y
    # regex_all = re.compile(r'\|\|.*?{variable}(\(\)).*?\|\|(\_[a-z])*')
    # c_list = re.findall(regex_all, condition)
    # print(f'c_list is {c_list}')

    # generate list for any freqence || A(x)> 0.5||_x or || A>0.5||
    # freq_list = re.findall(r'\|\|.*?\|\|[\w]*', condition)

    # if len(c_list) != 0:
    #     for content in c_list:
    #         value_ = str(
    #                     value / (len(state_name[variable]) - 1))
    #         # con = content.replace('||', '')
    #         con = re.sub(r'\|\|(_[a-z])*','',content)
    #         # con = con.replace(variable, value_)
    #         con = re.sub(r'{variable}\(.*?\)',value_,con)
    #         print(con)
    #         condition = re.sub(regex_all, con, condition, 1)
    # print(condition)
    print(condition)
    print('---')
    return condition

def check_probability_from_distribution(
        card_list, distribution, p_names, state_name, nodes):
    evi_value_dict = {p_names[i]: state_name[p_names[i]][va]
                      for i, va in enumerate(card_list)}
    prob = None
    for cond, val in distribution.items():
        str_expression = str_expression_helper(
            cond, evi_value_dict, state_name, nodes)
        # condition = cond.replace('!', ' not ').replace(' & ', ' and ').replace(' | ', ' or ')
        # for variable, value in evi_value_dict.items():
        #     if variable in condition:
        #         print(f'{variable} : {value}')
        #         if isinstance(value, bool):
        #             condition = condition.replace(variable, str(value))
        #         elif isinstance(value, int):
        #             regex = re.compile(f'\\|\\|{variable}.*?\\|\\|')
        #             c_list = re.findall(regex, condition)
        #             if len(c_list) != 0:
        #                 for content in c_list:
        #                     value_ = str(
        #                         value / (len(state_name[variable]) - 1))
        #                     # print(content)
        #                     con = content.replace('||', '')
        #                     # print(f'con is {con}')
        #                     con = con.replace(variable, value_)
        #                     # print(f'con after {con}')
        #                     condition = re.sub(regex, con, condition, 1)
        print(str_expression)
        if eval(str_expression):
            prob = val
            return prob
    if prob is None:
        return -1

def recursive_data(
        card_list,
        res_matrix,
        distribution,
        p_names,
        state_name, depth, nodes):
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
                card_list, res_matrix[i], distribution, p_names, state_name, depth, nodes)
        else:
            if len(card_list) != depth + 1:
                card_list.append(i)
            else:
                card_list[depth] = i
            # for test
            # res_matrix[i] = 1
            res_matrix[i] = check_probability_from_distribution(
                card_list, distribution, p_names, state_name, nodes)
    depth -= 1
    return res_matrix, depth

def fill_data_into_values(
        node,
        row: int,
        column: int,
        evidence: set,
        distribution: dict,
        state_name: dict,
        nodes: list):
    # todo need to check maybe use flag better
    if len(evidence) == 0:
        res_arr = []
        phi: float = float(distribution['self'])
        if len(node.get_domain()) == 0:
            res_arr = [phi, 1 - phi]
        elif len(node.get_domain()) == 1:
            res_arr = list(
                setup_bino_dist(
                    phi,
                    node.get_variable_card() -
                    1).values())
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
                card_list, res_matrix, distribution, p_names, state_name, depth=0, nodes=nodes)
            return numpy.append(res_matrix, 1 - res_matrix, axis=0)

def setup_bino_dist(phi: float, domain: int) -> dict:
    return {index: comb(domain, index) * pow(phi, index) *
            pow(1 - phi, domain - index) for index in range(domain + 1)}
