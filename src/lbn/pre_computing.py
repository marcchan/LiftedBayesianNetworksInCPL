from lbn.input.network import Network
from lbn.input.node import Node
from lbn.network_helper import set_network_edges


def pre_computing(network) -> Network:
    # the following line should out of this function,
    # currently only to test,
    # should be in generate_baysian_network function
    if network.get_edges() is not None:
        edges, freq_edges = network.get_edges(), network.get_freq_edges()
        non_freq_edges = list(set(edges).difference(set(freq_edges)))
        print(non_freq_edges)


    # name_list = [node.get_name() for node in self.nodes]
    # redundance = find_redundancy_network(name_list, self.evidences)
    # get_edges_no_freq(self)
    # update_distributions_from_nodes(self, redundance)


## not necessary
# def find_redundancy_network(name_list: list, evidences: dict):
#     redunance_list = set()
#     # print(name_list)
#     # print(evidences)
#     for node_name in name_list[::-1]:
#         if len(evidences[node_name]) == 0:
#             redunance_list.add(node_name)
#         else:
#             if node_name in redunance_list:
#                 redunance_list.pop(node_name)
#             redunance_list.union(evidences[node_name])
#     # print(redunance_list)
#     return redunance_list

# def update_distributions_from_nodes(network: Network, redundance: set):
#     evidences = network.get_evidences()
#     distributions = network.get_distributions()
#     domains =network.get_domains()
#     updated_nodes = [node for node in network.get_nodes() if node.get_name() not in redundance]
#     # nodes, domains , distributions, evidences TODO update
#     for remove_name in redundance:
#         distributions[remove_name]