from lbn.input.node import *
from lbn.input.formula import *
import copy

FORMULA_FILE = '../../examples/example_formula'
Domain_FILE = '../../examples/node_domain'


def parse_node_from_cond(dist: dict) -> set:
    evidences = set()
    for cond, value in dist.items():
        for node_name in name_list:
            if node_name in cond:
                evidences.add(node_name)
    return evidences


'''
from string distribution to extract the relation of other nodes,
set the evidences as a Set in node object:
    Drives has evidences empty set(),
    Air_is_good.get_evidences() = {Drives}
'''


def set_evidences_from_distributions(node: Node):
    dist = node.get_distributions()
    if len(dist) == 1:
        node.set_evidences(set())
    else:
        node.set_evidences(parse_node_from_cond(dist))


'''
get the nodes list with order， which can take turn into bbn model

'''


def get_ordered_nodes(nodes) -> list:
    ordered_nodes = []
    # deep copy avoid to destroy the old nodes
    unfinished_nodes = copy.deepcopy(nodes)
    # flag_dict = evidences_dict
    while len(unfinished_nodes) > 0:
        cur_node = unfinished_nodes.pop()
        if len(cur_node.get_evidences()) == 0:
            ordered_nodes.append(cur_node.get_name())
        elif cur_node.get_evidences() <= set(ordered_nodes):
            ordered_nodes.append(cur_node.get_name())
        else:
            unfinished_nodes.insert(0, cur_node)
    return ordered_nodes


def check_only_with_frequence(node1: Node, nodes: list) -> bool:
    node_counter, freq_node_counter = 0, 0
    for node in nodes:
        if node1.get_name() != node.get_name():
            dist_keylist = node.get_distributions().keys()
            for dist_key in dist_keylist:
                node_counter += dist_key.count(node1.get_name())
                freq_node_counter += dist_key.count(f'||{node1.get_name()}')
    print(node_counter)
    print(freq_node_counter)
    return node_counter == freq_node_counter
'''
TODO
maybe need new a class with FreqNode 

'''
def replace_node_to_freqnode(node, probability):
    return

def model_with_order(ordered_nodes: list):
    for node in ordered_nodes:
        # node without dependencies
        if len(node.get_evidences()) == 0:
            probability: float = node.get_distributions['self']
            if check_only_with_frequence(node, ordered_nodes):
                # todo setup_freq_dist()
                replace_node_to_freqnode(node, probability)
        else:
            # todo
            return


def condition_from_string_to_obj():
    return


def operator_parse_to_logic():
    return


# main
# read nodes with distributions into node list objects
nodes = map_formula(
    read_formula(FORMULA_FILE),
    init_nodes_from_json(Domain_FILE))

dist_list, name_list, evidences_dict = [], [], {}
for node in nodes:
    dist_list.append(node.get_distributions())
    name_list.append(node.get_name())

print(dist_list)
# avoid name_list and dist_list which do not finish init
for node in nodes:
    set_evidences_from_distributions(node)
    evidences_dict[node.get_name()] = node.get_evidences()

# order for the nodes to set up the BN model
ordered_nodes = get_ordered_nodes(nodes)
