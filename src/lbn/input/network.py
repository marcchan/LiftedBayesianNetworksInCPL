import numpy as numpy
from lbn.input.node import *
from lbn.parse_formula_into_distribution import *
from functools import reduce
import re


class Network(object):
    def __init__(self, nodes, distributions, evidences, domains):
        self.nodes = nodes
        self.distributions = distributions
        self.evidences = evidences
        self.domains = domains

    def get_domains(self):
        return self.domains

    def set_domains(self, domains):
        self.domains = domains

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes

    def get_evidences(self):
        return self.evidences

    def get_distributions(self):
        return self.distributions

    def get_edges(self):
        return self.edges if hasattr(self, 'edges') else None

    def get_freq_edges(self):
        return self.freq_edges if hasattr(self, 'freq_edges') else None

    def get_non_freq_edges(self):
        return list(set(self.edges).difference(set(self.freq_edges))) if (hasattr(self,'edges') and hasattr(self, 'freq_edges')) else None

    def set_edges_from_nodes(self):
        if len(self.nodes) != 0:
            edges, freq_edges = [], []
            for c_node, p_nodes in self.evidences.items():
                if len(p_nodes) != 0:
                    for p_node in p_nodes:
                        edges.append(tuple([p_node, c_node]))
                        for key, value in self.distributions[c_node].items():
                            if (len(re.findall(r'\|\|.*?' + p_node + '.*?\\|\\|', key))
                                    != 0) & (tuple([p_node, c_node]) not in freq_edges):
                                freq_edges.append(tuple([p_node, c_node]))
            self.edges = edges
            self.freq_edges = freq_edges
            print(self.edges)
            print(f'freq_edges{self.freq_edges}')
        else:
            print('have not inited nodes in set edges')

    def set_variable_card(self):
        self.variable_card = {node.get_name(): node.get_variable_card()
                              for node in self.nodes}

    def get_variable_card(self):
        return self.variable_card if hasattr(self, 'variable_card') else None

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
        # for any other case with multi parameter need to add case
        statenames = {}
        for node in self.nodes:
            if len(node.get_domain()) == 0:
                statenames[node.get_name()] = [True, False]
            elif len(node.get_domain()) == 1:
                statenames[node.get_name()] = list(
                    range(node.get_variable_card()))
            elif len(node.get_domain()) > 1:
                # TODO: for multi parameter
                print(f' TODO for multi parameter in set_statenames')
        self.statenames = statenames

    def get_statenames(self):
        return self.statenames if hasattr(self, 'statenames') else None

    def get_state_names_by_name(self, nodename: str):
        state_name = {}
        evidence = self.evidences[nodename]
        state_name[nodename] = self.statenames[nodename]
        for evi in evidence:
            state_name[evi] = self.statenames[evi]
        return state_name

    def set_values(self):
        # TODO
        """

        :return: None
        Values: 2D array
            Drives row = 5, col = 1
            Air_is_good row = 2, col = 5
            Fined row = 2, col = 5 * 2
        """
        values = {}
        print('set valueing')
        for node in self.nodes:
            print(f'current node is {node.get_name()}')
            row = self.get_variable_card_by_name(node.get_name())
            # may be has problem
            column: int = reduce(
                lambda x,
                y: x * y,
                self.get_evidence_card_by_name(
                    node.get_name())) if self.get_evidence_list_by_name(
                node.get_name()) is not None else 1
            temp_value = fill_data_into_values(node,
                                  row,
                                  column,
                                  self.evidences[node.get_name()],
                                  self.distributions[node.get_name()],
                                  self.get_state_names_by_name(node.get_name()),
                                  self.nodes)
            if temp_value is not None:
                print(f'nodename: {node.get_name()} has the value of{temp_value.reshape(row, column)}')
            else:
                print(f'nodename: {node.get_name()} can not get the value')

            values[node.get_name()] = temp_value.reshape(row, column)
        self.values = values

    def get_values_by_name(self, name: str):
        return self.values[name]

    def generate_bayesian_network(self):

        # self.pre_computing()
        self.set_edges_from_nodes()
        if self.nodes is not None:
            self.set_variable_card()
            self.set_statenames()
            self.set_values()
    # def pre_computing(self):
    #     # the following line should out of this function,
    #     # currently only to test,
    #     # should be in generate_baysian_network function
    #     self.set_edges_from_nodes()
    #     edges, freq_edges, non_freq_edges = self.edges, self.freq_edges, self.get_non_freq_edges()
    #     print(non_freq_edges)


        # name_list = [node.get_name() for node in self.nodes]
        # redundance = find_redundancy_network(name_list, self.evidences)
        # get_edges_no_freq(self)
        # update_distributions_from_nodes(self, redundance)

    def __str__(self):
        # check if generate_bayesian_network
        # if not hasattr(self,'edges'):
        return f'------\nNetwork:\n  nodes: {[node.to_str() for node in self.nodes]}\n  distributions: {self.distributions}\n  evidences: {self.evidences}\n  domains:{self.domains}\n------\n'

# def set_non_freq_arrow_priority(network: Network):
#     network.set_edges_from_nodes()
#     edges, freq_edges, non_freq_edges = network.get_edges(), network.get_freq_edges(), network.get_non_freq_edges()
#     evidences, distributions = network.get_evidences(),network.get_distributions()
#     for (p_node_name,c_node_name) in non_freq_edges:
#         # check p_node whether without evidence and c_node whether only has this evidence
#         if network.get_evidence_list_by_name(p_node_name) == None:
#             # calculate the probability of p_node and check if p_node only has 1 child
#             if len(network.get_evidence_list_by_name(c_node_name)) == 1:
#
#
#
# def pre_computing(network: Network):
#     network.set_edges_from_nodes()
#     edges, freq_edges, non_freq_edges = network.get_edges(), network.get_freq_edges(), network.get_non_freq_edges()
#     print(non_freq_edges)

def update_distributions_from_nodes(network: Network, redundance: set):
    evidences = network.get_evidences()
    distributions = network.get_distributions()
    domains =network.get_domains()
    updated_nodes = [node for node in network.get_nodes() if node.get_name() not in redundance]
    # nodes, domains , distributions, evidences TODO update
    for remove_name in redundance:
        distributions[remove_name]


def read_file(formula_file):
    try:
        with open(formula_file, 'r') as f:
            return f.read()
    except IOError as e:
        print(str(e))
        return None


def parse_domain(file_path, nodes):
    data = str.replace(read_file(file_path), ' ', '')
    domain_list = [i for i in str.split(data, '\n') if i != '']
    # {'driver': '4'}
    domain_dict = {domain[:domain.index(':')]: domain[domain.index(
        ':') + 1:] for domain in domain_list}

    for node in nodes:
        domain = {}
        if len(node.get_para()) != 0:
            for para_name, para_attribute in node.get_para().items():
                domain[para_name] = domain_dict[para_attribute]
        node.set_domain(domain)
    return nodes, domain_dict


def convert_string_to_dict(node_para_string):
    node_para_string = str.replace(node_para_string, ' ', '')
    if node_para_string == '{}':
        return {}
    else:
        para_dict = {}
        pattern = re.compile(r'[{}]')
        temp_para = re.sub(pattern, '', node_para_string)
        para_list = re.split(',', temp_para)
        for k_v_pair in para_list:
            temp = re.split(':', k_v_pair)
            para_dict[temp[0]] = temp[1]
        return para_dict


def parse_nodes(node_list: list) -> list:
    if node_list is None or len(node_list) == 0:
        print('Can not parse the node attribute from formula')
        pass
    else:
        nodes = []
        for node in node_list:
            temp = node.split('::')
            node_name, node_para_string = temp[0], temp[1]
            node_para = convert_string_to_dict(node_para_string)
            nodes.append(Node(node_name, node_para))
        return nodes


def parse_formula(formula: str):
    if formula is None:
        print('Formula read function has error\n')
    else:
        # print(formula)
        # node_regex = re.compile(r'.*?::[ ]*?\{.*?\}')
        node_regex = re.compile(r'.*?::[ ]*?{.*?}')
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
                # redundance
                # changed_fm = re.sub(r'.*?::[ ]*?\{.*?\}\n', '', formula_list[i])
                changed_fm = re.sub(r'.*?::[ ]*?{.*?}\n', '', formula_list[i])
                changed_fm_list = changed_fm.split('\n')
                for changed_fm_part in changed_fm_list:
                    if ':' not in changed_fm_part:
                        # temp_dict['self'] = float(changed_fm_part)
                        temp_dict['self'] = changed_fm_part
                    else:
                        # temp_dict[changed_fm_part[:changed_fm_part.index(':')]] = float(
                        #     changed_fm_part[changed_fm_part.index(':') + 1:])
                        temp_dict[changed_fm_part[:changed_fm_part.index(':')]] = \
                            changed_fm_part[changed_fm_part.index(':') + 1:]
                distributions_dict[nodes[i].get_name()] = temp_dict
        return nodes, distributions_dict


def set_evidences_from_distributions(nodes: list, distributions: dict) -> dict:
    """

    :param nodes:
    :param distributions:
    :return:
    from string distribution to extract the relation of other nodes,
    set the evidences as a Set in node object:
        Drives has evidences empty set(),
        Air_is_good.get_evidences() = {Drives}
    """
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


def sort_nodes(nodes: list, evidences: dict) -> list:
    """

    :param evidences:
    :param nodes:  List[Node]
    :return: list with ordered nodes
    get the nodes list with order， which can take turn into bbn model

    """
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


def parse_to_network(formula_file_path: str, domain_file_path: str):
    """

    :param formula_file_path:
    :param domain_file_path:
    :return: None
    easy to test
    """
    unordered_nodes, distributions = parse_formula(
        read_file(formula_file_path))
    temp_nodes, domains = parse_domain(
        domain_file_path, unordered_nodes)
    evidences = set_evidences_from_distributions(
        temp_nodes, distributions)
    nodes = sort_nodes(temp_nodes, evidences)
    return Network(nodes, distributions, evidences, domains)


def find_redundancy_network(name_list: list, evidences: dict):
    redunance_list = set()
    # print(name_list)
    # print(evidences)
    for node_name in name_list[::-1]:
        if len(evidences[node_name]) == 0:
            redunance_list.add(node_name)
        else:
            if node_name in redunance_list:
                redunance_list.pop(node_name)
            redunance_list.union(evidences[node_name])
    # print(redunance_list)
    return redunance_list


if __name__ == "__main__":
    FORMULA_FILE = '../../../examples/pre_computing_case/formula_v2'
    Domain_FILE = '../../../examples/pre_computing_case/domain'
    #
    network = parse_to_network(FORMULA_FILE, Domain_FILE)
    print(network)
    # network.set_edges_from_nodes()

    # pre_computing(network)
    # print(network)
    # network.pre_computing()

    # print(world.get_distributions())
    # print(f'evidences: {world.get_evidences()}')
    # world.generate_bayesian_network()
    # nodes = world.get_nodes()
    # for n in nodes:
    #     print((n.get_para().keys()))
    # print(f'edges: {world.get_edges()}')
    # print(f'variable_card: {world.get_variable_card()}')
    # print(f'statenames: {world.get_statenames()}')

    # regex_all = re.complie(r'\|\|.*?{variable}.*?\|\|(_[a-z]){0,}')

    # FORMULA_FILE = '../../../examples/pre_computing_case/formula_v2'
    # Domain_FILE = '../../../examples/pre_computing_case/domain'
    # network_pre = Network(FORMULA_FILE, Domain_FILE)
    # network_pre.pre_computing()
