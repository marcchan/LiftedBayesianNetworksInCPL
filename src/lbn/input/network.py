import numpy as numpy
from lbn.input.node import *
import json
from lbn.parse_formula_into_distribution import *
from functools import reduce

class Network(object):

    def __init__(self, formula_file_path: str, domain_file_path: str):
        self.formula_file_path = formula_file_path
        self.domain_file_path = domain_file_path
        self.nodes = self.check_ordered_nodes()
        self.edges = self.set_edges_from_nodes()
        self.set_variable_card()
        self.set_evidence_dict()
        # self.set_values()
        # self.generate_Bayesian_network()

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes

    def get_edges(self):
        return self.edges

    def set_edges_from_nodes(self):
        if len(self.nodes) != 0:
            edges = []
            for node in self.nodes:
                if len(node.get_evidences()) != 0:
                    for parent_node in node.get_evidences():
                        list_ = [parent_node, node.get_name()]
                        edges.append(tuple(list_))
            return edges
        else:
            print('have not inited nodes in set edges')

    def check_ordered_nodes(self) -> list:
        unordered_nodes = map_formula(
            read_formula(
                self.formula_file_path), init_nodes_from_json(
                self.domain_file_path))
        set_evidences_from_distributions(unordered_nodes)

        return check_ordered_nodes(unordered_nodes)

    def get_variable_by_node(self, node: Node):
        # TODO change freq_node if necessary
        return node.get_name()

    def set_variable_card(self):
        self.variable_card = {node.get_name(): node.get_variable_card()
                              for node in self.nodes}

    def get_variable_card(self):
        return self.variable_card

    def get_variable_card_by_name(self, name: str):
        return self.variable_card[name]

    def set_values(self):
        '''

        :return: None
        Values: 2D array
            Drives row = 5, col = 1
            Air_is_good row = 2, col = 5
            Fined row = 2, col = 5 * 2
        '''
        values_dict = {}
        for node in self.nodes:
            row = self.get_variable_card_by_name(node.get_name())
            column = reduce(
                lambda x,
                y: x * y,
                self.get_evidence_card_by_name(
                    node.get_name())) if self.get_evidence_dict_by_name(
                node.get_name()) is not None else 1
            values_dict[node.get_name()] = fill_data_into_values(node,row,column)
        self.values_dict = values_dict

    def get_values_by_name(self, name: str):
        return self.values_dict[name]

    def set_evidence_dict(self):
        evidence_dict = {}
        for node in self.nodes:
            list = []
            if len(node.get_evidences()) == 0:
                evidence_dict[node.get_name()] = list
            else:
                for n in self.nodes:
                    if n.get_name() in node.get_evidences():
                        list.append(n.get_name())
                evidence_dict[node.get_name()] = list
        self.evidence_dict = evidence_dict

    def get_evidence_dict(self):
        return self.evidence_dict

    def get_evidence_dict_by_name(self, nodename: str):
        if self.evidence_dict is not None:
            res = self.evidence_dict[nodename]
            if len(res) == 0:
                return None
            else:
                return res
        else:
            print('variable: evidence_dict has not defined')

    def get_evidence_card_by_name(self, nodename: str):
        evidence_list = self.get_evidence_dict_by_name(nodename)
        if evidence_list is not None:
            return [self.get_variable_card_by_name(
                ev_name) for ev_name in evidence_list]

    # def get_state_names_by_name(self, nodename: str):
    #     dict = {}
    #
    #     return

    # def generate_Bayesian_network(self):

        # self.set_values()


# # check and change to valid type of domain
def init_valid_node(name: str, type: str, domain):
    if type == 'bool':
        domain = [True, False]
    elif type == 'int':
        domain = int(domain)
    return Node(name, type, domain)


def map_formula(formula: str, nodes: list) -> list:
    formula_list = formula.split('\n\n')
    print(f'formula_list =  {formula_list}')
    for node in nodes:
        dict = {}
        for fm in formula_list:
            if f'{node.get_name()}::\n' in fm:
                changed_fm = fm.replace(f'{node.get_name()}::\n', '')
                changed_fm = changed_fm.replace(' ', '')
                changed_fm_list = changed_fm.split('\n')
                print(changed_fm_list)
                for changed_fm_part in changed_fm_list:
                    if ':' not in changed_fm_part:
                        dict['self'] = float(changed_fm_part)
                    else:
                        dict[changed_fm_part[:changed_fm_part.index(':')]] = float(
                            changed_fm_part[changed_fm_part.index(':') + 1:])
        node.set_distributions(dict)
    print('--------------- \n')
    return nodes


def read_formula(formula_file):
    with open(formula_file, 'r') as f:
        return f.read()


def set_evidences_from_distributions(nodes: list) -> None:
    '''

    :param node:  Node
    from string distribution to extract the relation of other nodes,
    set the evidences as a Set in node object:
        Drives has evidences empty set(),
        Air_is_good.get_evidences() = {Drives}

    '''
    name_list = [node.get_name() for node in nodes]
    for node in nodes:
        dist = node.get_distributions()
        if len(dist) == 1:
            node.set_evidences(set())
        else:
            evidences = set()
            for cond, value in dist.items():
                for node_name in name_list:
                    if node_name in cond:
                        evidences.add(node_name)
            node.set_evidences(evidences)


def check_ordered_nodes(nodes) -> list:
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
        if len(cur_node.get_evidences()) == 0:
            ordered_nodes_name.append(cur_node.get_name())
            ordered_nodes.append(cur_node)
        elif cur_node.get_evidences() <= set(ordered_nodes_name):
            ordered_nodes.append(cur_node)
            ordered_nodes_name.append(cur_node.get_name())
        else:
            unfinished_nodes.insert(0, cur_node)
    return ordered_nodes


def init_nodes_from_json(file_path):
    nodes = []
    with open(file_path) as json_file:
        data = json.load(json_file)
        for node_str in data['nodes']:
            node = init_valid_node(
                node_str['name'],
                node_str['type'],
                node_str['domain'])
            nodes.append(node)
    return nodes


if __name__ == "__main__":
    FORMULA_FILE = '../../../examples/example_formula'
    Domain_FILE = '../../../examples/node_domain'

    world = Network(FORMULA_FILE, Domain_FILE)
    # print(world.get_variable_card())
    # print(world.get_evidence_dict())
    # print(world.get_evidence_card_by_name('Drives'))
    # print(world.get_evidence_card_by_name('Air_is_good'))
    # print(world.get_evidence_card_by_name('Fined'))
    world.set_values()
    print(world.get_values_by_name('Drives'))
