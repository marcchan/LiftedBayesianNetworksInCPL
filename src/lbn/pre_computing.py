import re
from typing import Optional, Dict, Union, Any

from lbn.input.network import Network
from lbn.input.node import Node
from itertools import product
from lbn import network_helper
from lbn.network_helper import parse_to_network


class PreComputing(object):

    def __init__(self, network: Network):
        self.network = network
        self.backup = network
        self.queue = check_necessary(network)

    def set_network(self, network):
        self.network = network

    def get_network(self):
        return self.network

    def set_backup(self, network):
        self.backup = network

    def get_backup(self):
        return self.backup

    def optimize_network(self) -> Network:
        if len(self.queue) == 0:
            print('It is not necessary to do pre-computing for this network!!')
        else:
            print(f'\n\n ---PRE Computing Start---\n')
            for edge in self.queue:
                print(f'current edge which should be removed is {edge}')
                new_child_distribution = self.generate_new_distribution(edge)
                self.update_network(new_child_distribution, edge)
            print(f'\n ---PRE Computing END---\n\n')
        return self.network

    def generate_new_distribution(self, edge) -> Optional[dict[Union[str, Any], float]]:
        network = self.get_network()
        nodes = network.get_nodes()
        parent_name, child_name = edge
        parent_node = network.get_node_from_name(parent_name)
        parent_distribution: dict = network.get_distributions()[parent_name]
        parent_evidence = network.get_evidences()[parent_name]
        child_evidences = network.get_evidences()[child_name]
        child_distribution: dict = network.get_distributions()[child_name]
        child_new_distribution = {}

        if len(child_evidences) == 1:
            # this model contains one and only one out arrow and this arrow is non freq arrow
            # example: A -|-> B, B only has p(B|A) = x, P(B|!A) = y

            parent_format = parent_node.get_name(
            ) + parent_node.get_lower_para_from_node()[0]
            if parent_format not in child_distribution.keys():
                print('parent formula maybe has problem!!')
                return None
            else:
                p_true_c = child_distribution[parent_format]
                reverse_parent_format = '!' + parent_format
                if reverse_parent_format not in child_distribution.keys():
                    print(f'ERROR: Please check the formula of the node distribution:{parent_format}, False '
                          f'probability miss')
                    return None
                else:
                    p_false_c = child_distribution[reverse_parent_format]
                    # print(parent_distribution)
                    for condition, value in parent_distribution.items():
                        #  if parent is root: self works also
                        child_new_distribution[condition] = float(
                            p_true_c) * float(value) + float(p_false_c) * (1 - float(value))
                    # print(child_new_distribution)
                    return child_new_distribution

        elif len(child_evidences) > 1:
            bool_seperate_dict, interval_seperate_dict = get_seperate_dict(
                child_distribution, child_evidences)
            print(f'bool_seperate_dict: {bool_seperate_dict}')
            print(f'interval_seperate_dict: {interval_seperate_dict}')
            evi_nodes = [node for node in nodes if node.get_name()
                         in child_evidences]
            new_seperate_dict = {key: list(map(lambda x: (x[0], x[1]), zip(extend_list(
                value)[:-1], extend_list(value)[1:]))) for key, value in interval_seperate_dict.items()}

            for key, value in bool_seperate_dict.items():
                if key != parent_name:
                    new_seperate_dict[key] = value

            # print(new_seperate_dict)

            def enumerate_key_value(d):
                keys = list(d.keys())
                value_lists = list(d.values())
                combinations = product(*value_lists)
                for combination in combinations:
                    yield dict(zip(keys, combination))

            for result in enumerate_key_value(new_seperate_dict):
                print(result)
                new_fomula_list = get_cond_from_dict(result, evi_nodes)
                print(new_fomula_list)
                value_dict = eval_dict_value(
                    child_distribution, result, evi_nodes, parent_name)
                print(f'value_dict:{value_dict}')
                for p_formula, p_value in parent_distribution.items():
                    new_list = str.split(
                        p_formula,
                        ' & ') + new_fomula_list if len(parent_evidence) > 0 else new_fomula_list
                    new_formula = ' & '.join(new_list)
                    child_new_distribution[new_formula] = float(
                        value_dict[True]) * float(p_value) + float(value_dict[False]) * (1 - float(p_value))
            print(f'\nnew child distribution: {child_new_distribution}\n')
            return child_new_distribution

    def update_network(self, child_distribution, edge):
        self.backup = self.network
        parent, child = edge
        nodes: list = self.network.get_nodes()
        distributions: dict = self.network.get_distributions()
        # domain todo need to change
        p_node = self.network.get_node_from_name(parent)
        nodes.remove(p_node)
        distributions.pop(parent)
        distributions[child] = child_distribution
        self.network.set_nodes(nodes)
        self.network.set_distributions(distributions)

        evidences = network_helper.set_evidences_from_distributions(
            nodes, distributions)
        self.network.set_evidences(evidences)
        network_helper.set_network_edges(self.network)


def check_necessary(network) -> list:
    # return the non_freq_arrow_set which
    # is necessary to deal with pre-computing
    network_helper.set_network_edges(network)
    edges, freq_edges = network.get_edges(), network.get_freq_edges()
    common_edges = set(edges) & set(freq_edges)
    non_freq_edges = [edge for edge in edges if edge not in common_edges]
    print(f'---non_freq_edges:{non_freq_edges}')
    result = []

    # strategy: only one out arrow with non freq could be optimized
    # 有且并有一条一条出边， 且出边都是non freq arrow
    for (parent, child) in non_freq_edges:
        # out arrow only one
        if len(network.get_children_dict()[parent]) == 1:
            result.append((parent, child))
    print(f'pre-computing-queue is {result}')
    return result


def get_seperate_dict(distribution: dict, evidence: set):
    bool_evidence_set = set()
    freq_evidence_set = evidence.copy()
    interval_seperate_dict = {}

    # add all non-freq-node into bool evidence set
    for key in distribution.keys():
        match_list = re.findall(r'![a-zA-Z0-9]+', key)
        if len(match_list) != 0:
            # x[0] = '!' so we need x[1:]
            bool_evidence_set.update([x[1:] for x in match_list])

    bool_seperate_dict = {key: [True, False] for key in bool_evidence_set}
    freq_evidence_set -= bool_evidence_set
    for freq_evidence in freq_evidence_set:
        interval_set = {0, 1}
        for formular in distribution.keys():
            temp_variable = [
                x for x in re.findall(
                    r"(\|\|.*?\|\|.*? [>=<]=? \d\.?\d*)",
                    formular) if freq_evidence in x]
            if len(temp_variable) > 1:
                print(
                    f'Be Attention: this formula: {formular} contain 2 times the freq_evidence: {freq_evidence}')
            elif len(temp_variable) == 0:
                print(
                    f'Be Attention: this formula: {formular} does not contain the freq_evidence: {freq_evidence}')
            else:
                # the interval is always decimal and >0 <1
                decimal_pattern = re.compile(rf'0\.\d+')
                interval_set.update(
                    map(float, (re.findall(decimal_pattern, temp_variable[0]))))
        interval_list = sorted(interval_set)
        interval_seperate_dict[freq_evidence] = interval_list

    # if need the combination logic. e.g. & or, it could be
    return bool_seperate_dict, interval_seperate_dict


def extend_list(lst):
    result = []
    for item in lst:
        if item != 0 and item != 1:
            result.extend([item, item])
        else:
            result.append(item)
    return result


def get_cond_from_dict(d: dict, nodes) -> Optional[list]:
    new_formula_list = []
    for node in nodes:
        if node.get_name() in d.keys():
            if isinstance(d[node.get_name()], bool):
                new_formula_list.append(f'{node.get_name()}{node.get_lower_para_from_node()[0]}' if d[node.get_name(
                )] else f'!{node.get_name()}{node.get_lower_para_from_node()[0]}')
            elif isinstance(d[node.get_name()], tuple):
                var1, var2 = d[node.get_name()]
                start_freq_cond = f'||'
                end_freq_cond = f'||{node.get_lower_para_from_node()[1]}'
                para_suffix = node.get_lower_para_from_node()[0]
                freq_cond = start_freq_cond + node.get_name() + para_suffix + end_freq_cond
                if var1 != var2:
                    if var1 == 0:
                        freq_cond += f' < {var2}'
                    elif var2 == 1:
                        freq_cond += f' > {var1}'
                    else:
                        freq_cond = f'{var1} < {freq_cond} < {var2}'
                else:
                    if var1 not in (0, 1):
                        # todo currently use == replace =
                        freq_cond += f' == {var1}'
                    else:
                        print('ERROR: [0,1]')
                        return None
                print(freq_cond)
                new_formula_list.append(
                    freq_cond)
            else:
                print(
                    'Error: {node.get_name()} must only with type of bool and tuple')
                return None
    return new_formula_list


def convert_formula_dict(formula_dict: dict, nodes: list, parent_name) -> dict:
    new_dict = {}
    for formula, value in formula_dict.items():
        formula_list = str.split(formula, ' & ')
        for index, cond in enumerate(formula_list):
            temp_cond = cond
            for node in nodes:
                para, suffix = node.get_lower_para_from_node()
                if '||' in cond and node.get_name() + para in cond:
                    temp_cond = str.replace(temp_cond, '||', '')
                    temp_cond = str.replace(
                        temp_cond, f'{node.get_name()}{para}', f'{node.get_name()}')
                    temp_cond = str.replace(temp_cond, suffix, '')
                    # temp_cond = str.replace(temp_cond, ' = ', ' == ')
                elif node.get_name() + para in temp_cond:
                    temp_cond = str.replace(
                        temp_cond, node.get_name() + para, node.get_name())
                    temp_cond = str.replace(temp_cond, '!', 'not ')
            formula_list[index] = temp_cond
        new_formula = ' and '.join(formula_list)
        new_dict[new_formula] = value
    # print(new_dict)
    return new_dict


def eval_dict_value(formula_dict: dict, d: dict, nodes, parent_name):
    # case: d = {'D': (0.5, 1), 'E': (0.7, 1), 'G': False}
    # convert_d = {'D': 0.75, 'E': 0.85, 'G': False}
    convert_d = {k: (v[1] + v[0]) / 2.0 if isinstance(d[k],
                                                      tuple) else v for k, v in d.items()}
    new_formula_dict = convert_formula_dict(formula_dict, nodes, parent_name)
    bool_parent_list = [True, False]
    result = {}
    for bool_parent in bool_parent_list:
        for node in nodes:
            if node.get_name() != parent_name:
                exec(f'{node.get_name()} = {convert_d[node.get_name()]}')

        #  D = 0.75, E = 0.85, G = False
        # G(s) & C(n) & | | D(z) >= 0.45 | | _z & | | E(m) >= 0.6 | | _m: 0.9
        # G and C and D >= 0.45 and E >= 0.6
        exec(f'{parent_name} = {bool_parent}')
        for formula, value in new_formula_dict.items():
            if eval(formula):
                result[bool_parent] = value
    return result

if __name__ == "__main__":
    # FORMULA_FILE = '../../examples/drive_drink/formula'
    # DOMAIN_FILE = '../../examples/drive_drink/domain'
    FORMULA_FILE = '../../examples/drive_air_city/formula'
    DOMAIN_FILE = '../../examples/drive_air_city/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/case2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/Case2/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/domain'
    # FORMULA_FILE = '../../examples/infectious_disease/formula'
    # DOMAIN_FILE = '../../examples/infectious_disease/domain'
    network = parse_to_network(FORMULA_FILE, DOMAIN_FILE)
    print(f'the new network from Pre-Computing is {PreComputing(network).optimize_network()}')