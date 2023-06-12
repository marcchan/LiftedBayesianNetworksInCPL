from itertools import product

from lbn.input.network import Network
from lbn.input.node import Node


class LiftedBaysianNetwork(object):
    def __init__(self, network: Network, flag: bool):
        self.abstract_network = network
        self.lifted_flag = flag


    def check_lifted_nodes(self):
        # return the list of nodes which could be lifted.
        # lifted mean A(x) do not need to represent A_1,...A_n nodes with bool values,
        # could lifted as a node A(x) has the values= 0,...,n with frequency
        nodes = self.abstract_network.get_nodes()
        children_dict = self.abstract_network.get_children_dict()
        distributions = self.abstract_network.get_distributions()
        print(children_dict)
        print(distributions)
        for node in nodes:
            if node.get_name() in children_dict:
                flag = True
                for child in children_dict[node.get_name()]:
                    print(distributions[child])





def check_nodes_with_domain(network: Network, lifted_flag):
    pending_node_list = []
    distributions = network.get_distributions()
    evidences = network.get_evidences()
    if not lifted_flag:
        pending_node_list = network.get_nodes()
    else:
        # todo 可以不用
        pass
    lifted_node_list = []
    map_dict = {}
    new_evidences = {}
    new_distributions = {}
    for node in pending_node_list:
        map_dict[node.get_name()] = generate_n_nodes(node)
        print([n.get_name() for n in generate_n_nodes(node)])
        lifted_node_list.extend(generate_n_nodes(node))
    # for node in pending_node_list:
    #     if not evidences[node.get_name()]:
    #         for l_n in map_dict[node.get_name()]:
    #             new_distributions[l_n.get_name()] = distributions[node.get_name()]
    #             evidences[l_n.get_name()] = set()
    #     else:
    #         for


def generate_n_nodes(node: Node) -> list:
    # From Node to LiftedNode which we need to release domain into every node
    # example node : name: Qualified, Domain:{'T': '4'}             -> Qualified[t~1], ... Qualified[t~4]
    #                name: GoodSchool, Domain:{}'                   -> GoodSchool
    #                name: Something, Domain: {'T': '4', 'S': '3'}  -> Something[t~1,s~1], ... Something[t~4,s~3]
    lifted_nodes = []
    domain = node.get_domain()
    for combination in product(*[range(int(value)) for value in domain.values()]):
        result_dict = {key: combination[i] + 1 for i, key in enumerate(domain.keys())}
        # 有待重新定义
        kv_pair = ''.join('_{}{}'.format(str.lower(key), value) for key, value in result_dict.items())
        # consider the situation which node without para, as Air_Is_Good and Fined in DAF graph
        name = f'{node.get_name()}' if kv_pair == '' else f'{node.get_name()}{kv_pair}'
        # lifted_nodes.append(NormalNode(name, para={}, domain={},prototype=node))
    return lifted_nodes



