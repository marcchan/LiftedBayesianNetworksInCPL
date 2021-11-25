from lbn.input.node import *
import json
class World(object):

    def __init__(self, formula_file_path: str, domain_file_path: str):
        self.formula_file_path = formula_file_path
        self.domain_file_path = domain_file_path
        self.nodes = self.generate_world()

    def get_nodes(self):
        return self.nodes

    def set_nodes(self,nodes):
        self.nodes = nodes



    def generate_world(self)-> list:
        unordered_nodes = map_formula(read_formula(self.formula_file_path),
                            init_nodes_from_json(self.domain_file_path))
        set_evidences_from_distributions(unordered_nodes)

        return check_ordered_nodes(unordered_nodes)


#
# # check and change to valid type of domain
#
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
                        dict[changed_fm_part[
                             :changed_fm_part.index(':')]] \
                            = float(changed_fm_part[changed_fm_part.index(':') + 1:])
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

    world = World(FORMULA_FILE,Domain_FILE)
    nodes = world.get_nodes()
    [print(i) for i in nodes]