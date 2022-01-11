import numpy as numpy
from lbn.input.node import *
import json
from lbn.parse_formula_into_distribution import *
from functools import reduce
import re


class Network(object):

    def __init__(self, formula_file_path: str, domain_file_path: str):
        self.formula_file_path = formula_file_path
        self.domain_file_path = domain_file_path
        self.nodes, self.distributions, self.evidences = self.check_ordered_nodes()
        print(f'nodes:{self.nodes}')
        print(f'distribution: {self.distributions}')
        # self.edges = self.set_edges_from_nodes()
        # self.set_variable_card()
        # print(f'variable card: {self.variable_card}')
        # self.set_statenames()
        # self.set_values()
        # self.generate_Bayesian_network()

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes

    def get_evidences(self):
        return self.evidences

    def get_distributions(self):
        return self.distributions

    def get_edges(self):
        return self.edges

    def set_edges_from_nodes(self):
        if len(self.nodes) != 0:
            edges = []
            for c_node, p_nodes in self.evidences.items():
                if len(p_nodes) != 0:
                    for p_node in p_nodes:
                        edges.append(tuple([p_node, c_node]))
            return edges
        else:
            print('have not inited nodes in set edges')

    def check_ordered_nodes(self):
        # unordered_nodes = init_nodes_from_json(self.domain_file_path)
        unordered_nodes, distributions = map_formula(
            read_formula(self.formula_file_path))
        evidences = set_evidences_from_distributions(
            unordered_nodes, distributions)
        nodes = check_ordered_nodes(unordered_nodes, evidences)
        return nodes, distributions, evidences

    # def get_variable_by_node(self, node: Node):
    #     # TODO change freq_node if necessary
    #     return node.get_name()

    def set_variable_card(self):
        self.variable_card = {node.get_name(): node.get_variable_card()
                              for node in self.nodes}

    def get_variable_card(self):
        return self.variable_card

    def get_variable_card_by_name(self, name: str):
        return self.variable_card[name]

    def get_evidence_list_by_name(self, nodename: str):
        if self.evidences is not None:
            res = self.evidences[nodename]
            if len(res) == 0:
                return None
            else:
                return list(res)
        else:
            print('variable: evidence_dict has not defined')

    def get_evidence_card_by_name(self, nodename: str):
        evidence_list = self.get_evidence_list_by_name(nodename)
        if evidence_list is not None:
            return [self.get_variable_card_by_name(
                ev_name) for ev_name in evidence_list]

    def set_statenames(self):
        # todo need to change
        statenames = {}
        for node in self.nodes:
            if node.get_type() == 'int':
                statenames[node.get_name()] = list(
                    range(node.get_domain() + 1))
            elif node.get_type() == 'bool':
                statenames[node.get_name()] = node.get_domain()
        self.statenames = statenames


    def get_statenames(self):
        return self.statenames

    def get_state_names_by_name(self, nodename: str):
        state_name = {}
        evidence = self.evidences[nodename]
        state_name[nodename] = self.statenames[nodename]
        for evi in evidence:
            state_name[evi] = self.statenames[evi]
        return state_name

    def set_values(self):
        '''

        :return: None
        Values: 2D array
            Drives row = 5, col = 1
            Air_is_good row = 2, col = 5
            Fined row = 2, col = 5 * 2
        '''
        values = {}
        for node in self.nodes:
            row = self.get_variable_card_by_name(node.get_name())
            # may be has problem
            column = reduce(
                lambda x,
                y: x * y,
                self.get_evidence_card_by_name(
                    node.get_name())) if self.get_evidence_list_by_name(
                node.get_name()) is not None else 1
            values[node.get_name()] = fill_data_into_values(node,
                                                            row,
                                                            column,
                                                            self.evidences[node.get_name()],
                                                            self.distributions[node.get_name()],
                                                            self.get_state_names_by_name(node.get_name())).reshape(row,
                                                                                                                   column)

        self.values = values

    def get_values_by_name(self, name: str):
        return self.values[name]

    def generate_Bayesian_network(self):
        if self.nodes is not None:
            self.edges = self.set_edges_from_nodes()
            self.set_variable_card()
            print(f'variable card: {self.variable_card}')
            self.set_statenames()
            self.set_values()


# def init_nodes_from_json(file_path) -> list:
#     nodes = []
#     with open(file_path) as json_file:
#         data = json.load(json_file)
#         for node_str in data['nodes']:
#             node = init_valid_node(
#                 node_str['name'],
#                 node_str['type'],
#                 node_str['domain'])
#             nodes.append(node)
#     return nodes

# # check and change to valid type of domain

#
# def init_valid_node(name: str, type: str, domain):
#     if type == 'bool':
#         domain = [True, False]
#     elif type == 'int':
#         domain = int(domain)
#     return Node(name, type, domain)


def read_formula(formula_file):
    try:
        with open(formula_file, 'r') as f:
            return f.read()
    except IOError as e:
        print(str(e))
        return None


def parse_nodes(node_list: list) -> list:
    if node_list is None or len(node_list) == 0:
        print('Can not parse the node attribute from formula')
        pass
    else:
        nodes = []
        for node in node_list:
            temp = node.split('::')
            node_name, node_para = temp[0], temp[1]
            nodes.append(Node(node_name, node_para))
        return nodes


def map_formula(formula: str):
    if formula is None:
        print('Formula read function has error\n')
    else:
        # print(formula)
        node_regex = re.compile(r'.*?::{.*?}')
        # node_regex = re.compile('.*?::{.*?(.*?\n.*?)*?.*?}', re.I | re.DOTALL)
        node_list = re.findall(node_regex, formula)
        # print(node_list)
        nodes = parse_nodes(node_list)
        formula_regex = re.compile(r'\n\n')
        formula_list = re.split(formula_regex, formula)
        # print(formula_list)
        distributions_dict = {}
        if len(nodes) == len(formula_list):
            for i in range(len(nodes)):
                temp_dict = {}
                changed_fm = re.sub(r'.*?::{.*?}\n', '', formula_list[i])
                changed_fm_list = changed_fm.split('\n')
                for changed_fm_part in changed_fm_list:
                    if ':' not in changed_fm_part:
                        temp_dict['self'] = float(changed_fm_part)
                    else:
                        temp_dict[changed_fm_part[:changed_fm_part.index(':')]] = float(
                            changed_fm_part[changed_fm_part.index(':') + 1:])
                distributions_dict[nodes[i].get_name()] = temp_dict
        return nodes, distributions_dict


def set_evidences_from_distributions(nodes: list, distributions: dict) -> dict:
    '''

    :param node:  dict
    from string distribution to extract the relation of other nodes,
    set the evidences as a Set in node object:
        Drives has evidences empty set(),
        Air_is_good.get_evidences() = {Drives}

    '''
    name_list = [node.get_name() for node in nodes]
    evidences = {}
    for node in nodes:
        dist = distributions[node.get_name()]
        if len(dist) == 1:
            evidences[node.get_name()] = set()
        else:
            evidence = set()
            for cond, value in dist.items():
                for node_name in name_list:
                    if node_name in cond:
                        evidence.add(node_name)
            evidences[node.get_name()] = evidence
    return evidences


def check_ordered_nodes(nodes: list, evidences: dict) -> list:
    '''

    :param nodes:  List[Node]
    :return: list with ordered nodes
    get the nodes list with order， which can take turn into bbn model

    '''
    ordered_nodes_name = []
    ordered_nodes = []
    # deep copy avoid to destroy the old nodes
    unfinished_nodes = list(nodes)

    while len(unfinished_nodes) > 0:
        cur_node = unfinished_nodes.pop()
        if len(evidences[cur_node.get_name()]) == 0:
            ordered_nodes_name.append(cur_node.get_name())
            ordered_nodes.append(cur_node)
        elif evidences[cur_node.get_name()] <= set(ordered_nodes_name):
            ordered_nodes.append(cur_node)
            ordered_nodes_name.append(cur_node.get_name())
        else:
            unfinished_nodes.insert(0, cur_node)
    return ordered_nodes


if __name__ == "__main__":
    FORMULA_FILE = '../../../examples/drives_air_fined/formula_v1'
    # Domain_FILE = '../../../examples/drives_air_fined/domain'

    map_formula(read_formula(FORMULA_FILE))

    #
    # world = Network(FORMULA_FILE, Domain_FILE)
    # print(world.get_distributions())
    # print(world.get_edges())
    # print(world.get_variable_card())
    # print(world.get_evidences())

    # print(world.get_evidence_card_by_name('Drives'))
    # print(world.get_evidence_card_by_name('Air_is_good'))
    # print(world.get_evidence_card_by_name('Fined'))

    # print(world.get_statenames())
    # print(world.get_state_names_by_name('Drives'))
    # print(world.get_state_names_by_name('Fined'))
    # world.set_values()

    # print(world.get_values_by_name('Drives'))
    # print(world.get_values_by_name('Air_is_good'))
    # print(world.get_values_by_name('Fined'))
    # distribution = world.get_distributions()['Fined']
    # card = [2, 5]
    # # distribution = {'Air_is_good': 0.1, '!Air_is_good&||Drives>=0.7||': 0.8, '!Air_is_good&||Drives<0.7||': 0.3}
    # res_matrix = numpy.zeros(card)
    #
    # p_names = ['Air_is_good', 'Drives']
    # state_name = {'Fined': [True, False], 'Air_is_good': [True, False], 'Drives': [0, 1, 2, 3, 4]}
    # card_list = []
    # recursive_fill_data(card_list,res_matrix,distribution,p_names,state_name)
    # str = ' not False | 0.0>=0.7'
    # print(str.replace('&', ' and '))
