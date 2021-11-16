import json


class Node(object):

    evidences: set
    distributions= {}

    def __init__(self, name: str, type: str, domain=None):
        self.name = name
        self.type = type
        self.domain = domain

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_domain(self):
        return self.domain

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.type = type

    def set_domain(self, domain):
        self.domain = domain

    def get_distributions(self):
        return self.distributions

    def set_distributions(self, distributions: dict):
        self.distributions = distributions

    def get_evidences(self):
        return self.evidences

    def set_evidences(self, evidences: set):
        self.evidences = evidences





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

# check and change to valid type of domain


def init_valid_node(name: str, type: str, domain):
    if type == 'bool':
        domain = [True, False]
    elif type == 'int':
        domain = int(domain)
    return Node(name, type, domain)

# def
# nodes = init_nodes_from_json('../../../examples/node_domain')
# print(type(nodes[0].get_domain()))
