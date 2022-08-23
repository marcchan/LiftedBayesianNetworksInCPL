from functools import reduce
from lbn.pre_computing import check_necessary, delete_node
from lbn.parse_formula_into_distribution import fill_data_into_values
from network_helper import set_network_edges,set_network_statenames,set_network_variable_card,parse_to_network

def set_network_values(network):
    # TODO need to refactor
    """

    :return: None
    Values: 2D array
        Drives row = 5, col = 1
        Air_is_good row = 2, col = 5
        Fined row = 2, col = 5 * 2
    """
    values = {}
    for node in network.get_nodes():
        print(f'current node is {node.get_name()}')
        row = network.get_variable_card_by_name(node.get_name())
        # maybe has problem
        column: int = reduce(
            lambda x,
                   y: x * y,
            network.get_evidence_card_by_name(
                node.get_name())) if network.get_evidence_list_by_name(
            node.get_name()) is not None else 1
        temp_value = fill_data_into_values(node,
                                           row,
                                           column,
                                           network.get_evidences()[node.get_name()],
                                           network.get_distributions()[node.get_name()],
                                           network.get_state_names_by_name(node.get_name()),
                                           network.get_nodes())
        if temp_value is not None:
            print(f'nodename: {node.get_name()} has the value of{temp_value.reshape(row, column)}')
        else:
            print(f'nodename: {node.get_name()} can not get the value')

        values[node.get_name()] = temp_value.reshape(row, column)
    network.set_values(values)

def pre_computing(network):
    pre_computing_queue = check_necessary(network)
    temp_network = network
    if len(pre_computing_queue) == 0:
        print('It is not necessary to do pre-computing for this network!!')
    else:
        for pre_computing_edge in pre_computing_queue:
            # temp_network = delete_node(temp_network, pre_computing_edge)
            pass
    return

def generate_bayesian_network(network):
    # update_network = pre_computing(network)
    # current need set_edges, if pre_computing is done, please remove this loc
    if network.get_nodes() is not None:
        set_network_variable_card(network)
        print('---------')
        print(network.get_variable_card())
        set_network_statenames(network)
        print(network.get_statenames())
        print('---------')
        set_network_values(network)


if __name__ == "__main__":
    FORMULA_FILE = '../../examples/pre_computing_case/temp_3'
    Domain_FILE = '../../examples/pre_computing_case/domain'
    # FORMULA_FILE = '../../examples/drives_air_fined/formula_v2'
    # Domain_FILE = '../../examples/drives_air_fined/domain_v1'
    # FORMULA_FILE = '../../examples/test_two_network/formula'
    # Domain_FILE = '../../examples/test_two_network/domain'
    network = parse_to_network(FORMULA_FILE, Domain_FILE)

    # pre_computing(network)
    generate_bayesian_network(network)
    # world.generate_bayesian_network()
    # nodes = world.get_nodes()
    # for n in nodes:
    #     print((n.get_para().keys()))
    # print(f'edges: {world.get_edges()}')
    # print(f'variable_card: {world.get_variable_card()}')
    # print(f'statenames: {world.get_statenames()}')
