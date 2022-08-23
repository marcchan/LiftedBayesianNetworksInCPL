from lbn.input.network import Network
from lbn.input.node import Node
from lbn.network_helper import get_lower_para_from_node


def check_necessary(network) -> set:
    # return the non_freq_arrow_set which
    # is necessary to deal with pre-computing

    edges, freq_edges = network.get_edges(), network.get_freq_edges()
    non_freq_edges = set(edges).difference(set(freq_edges))
    print(f'---non_freq_edges:{non_freq_edges}')
    result = set()

    # strategy: only one out arrow with non freq could be optimized
    for (parent, child) in non_freq_edges:
        # out arrow only one
        if len(network.get_children_dict()[parent]) == 1:
            result.add((parent, child))
    print(f'pre-computing-set is {result}')
    # sort
    print([node.get_name() for node in network.get_nodes()])
    return result



def delete_node(network, edge):
    nodes = network.get_nodes()
    parent, child = edge
    node = network.get_node_from_name(parent)
    parent_distribution = network.get_distributions()[parent]
    parent_evidence = network.get_evidences()[parent]
    child_evidence = network.get_evidences()[child]
    child_distribution =  network.get_distributions()[child]
    print(parent_distribution)
    print(parent_evidence)
    # remove parent node
    nodes.remove(node)
    # if parent node is root
    if len(parent_evidence) == 0:
        parent_probability = float(parent_distribution['self'])
        new_child_prob : float = -1
        # doesn't have other parent nodes for child node
        if len(child_evidence) == 1:
            single_true_condition = parent+get_lower_para_from_node(node)[0]
            new_child_prob = calculate_single_condition_probability(child_distribution, single_true_condition, parent_probability)
        else:
        # child has other parent nodes
        # A -|- > B, B:  A and ||C||
        # 先把贝叶斯网络设置几个方法打包一下， 然后算分割点， 比如0.5， 求 P（B ｜ ||C||） 然后导出
        # 需要对pre-computing-queue 进行排序： 排序 包括 包含其他节点
            pass





    # delete node domain
    # node_domain = node.get_domain()
    # delete node edges


    # if len(node_evidence) == 0:
    #     # nodes.remove(node)
    #     pass
    return network

def calculate_single_condition_probability(distribution: dict, single_true_condition: str, evidence_prob):
    if single_true_condition in distribution.keys():
        condition_true_prob = distribution[single_true_condition]
        single_not_true_condition = '!'+single_true_condition
        if single_not_true_condition not in distribution.keys():
            print('formula maybe has problem!!')
            return
        else:
            condition_not_ture_prob = distribution[single_not_true_condition]
        return float(condition_true_prob) * evidence_prob + float(condition_not_ture_prob) * (1-evidence_prob)

def update_distributions_from_nodes(network: Network):
    pass


def pgmpy_adapter(distribution, divide_list) -> dict:
    pass


def update_network():
    pass
