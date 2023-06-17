import re
from lbn.input.network import Network
from lbn.input.node import Node


def read_file(file):
    try:
        with open(file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("File Not Found")
        return None
    except IOError as e:
        print("IOExcpetion when reading the file：{}".format(str(e)))
        return None


def parse_formula(formula: str):
    node_regex = re.compile(r'.*?::[ ]*?{.*?}')
    node_list = re.findall(node_regex, formula)
    nodes = parse_nodes(node_list)
    formula_list = formula.split('\n\n')
    # print(f'here:{formula_list}')
    distributions_dict = {}
    if len(nodes) != len(formula_list):
        print('ERROR: formula list length is not equal as node list length')
        return
    else:
        for n, fm in zip(nodes, formula_list):
            temp_dict = {}
            changed_fm = re.sub(r'.*?::[ ]*?{.*?}\n', '', fm)
            for line in changed_fm.split('\n'):
                # could be remove later
                if line != '':
                    # if ':' not in line:
                    #     temp_dict['self'] = line
                    # else:
                    key, value = map(str.strip, line.split(':'))
                    temp_dict[key] = value
                distributions_dict[n.get_name()] = temp_dict
    return nodes, distributions_dict


def parse_domain(file_path, nodes):
    data = read_file(file_path).replace(' ', '')
    domain_list = [i for i in str.split(data, '\n') if i]

    domain_dict = {domain[:domain.index(':')]: domain[domain.index(
        ':') + 1:] for domain in domain_list}

    for node in nodes:
        domain = {}
        for para_name, para_attribute in node.get_para().items():
            domain[para_name] = domain_dict[para_attribute]
        node.set_domain(domain)
    return nodes, domain_dict


def convert_para_string_to_dict(node_para_string):
    if node_para_string == '{}':
        return {}
    else:
        pattern = re.compile(r'[{}]|\s')
        temp_para = re.sub(pattern, '', node_para_string)
        para_list = temp_para.split(',')
        return dict([x.split(':') for x in para_list])


def parse_nodes(node_list: list) -> list:
    if node_list is None or len(node_list) == 0:
        print('Can not parse the node attribute from formula')
    else:
        nodes = []
        for node in node_list:
            node_name, node_para_string = node.split('::')
            node_para = convert_para_string_to_dict(node_para_string)
            nodes.append(Node(node_name, node_para))
        return nodes


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
        if len(dist) == 1 and 'self' in dist.keys():
            evidences[node.get_name()] = set()
        else:
            evidence = set()
            for cond, value in dist.items():
                for node_name in name_list:
                    if node_name in cond:
                        evidence.add(node_name)
            evidences[node.get_name()] = evidence
    return evidences


# def sort_nodes(nodes: list, evidences: dict) -> list:
#     """
#
#     :param evidences:
#     :param nodes:  List[Node]
#     :return: list with ordered nodes
#     get the nodes list with order， which can take turn into bbn model
#
#     """
#     ordered_nodes = []
#     unfinished_nodes = set(nodes)
#     while unfinished_nodes:
#         cur_node = unfinished_nodes.pop()
#         if not evidences[cur_node.get_name()]:
#             ordered_nodes.append(cur_node)
#         elif evidences[cur_node.get_name()].issubset(node.get_name() for node in ordered_nodes):
#             ordered_nodes.append(cur_node)
#         else:
#             unfinished_nodes.add(cur_node)
#     return ordered_nodes


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


def parse_to_network(formula_file_path: str, domain_file_path: str) -> Network:
    unordered_nodes, distributions = parse_formula(
        read_file(formula_file_path))
    print(distributions)
    temp_nodes, domains = parse_domain(
        domain_file_path, unordered_nodes)
    evidences = set_evidences_from_distributions(
        temp_nodes, distributions)
    nodes = sort_nodes(temp_nodes, evidences)
    network = Network(nodes, distributions, evidences, domains)
    set_network_edges(network)
    print(network)
    return network


def set_network_statenames(network):
    # for any other case with multi parameter need to add case
    statenames = {}
    for node in network.get_nodes():
        if len(node.get_domain()) == 0:
            statenames[node.get_name()] = [True, False]
        elif len(node.get_domain()) == 1:
            statenames[node.get_name()] = list(
                range(node.get_variable_card()))
        elif len(node.get_domain()) > 1:
            # TODO: for multi parameter
            print(f' TODO for multi parameter in set_statenames')
    print(f'statename:{statenames}')
    network.set_statenames(statenames)


def set_network_edges(network):
    if len(network.get_nodes()) != 0:
        edges, freq_edges = [], []
        for c_node, p_nodes in network.get_evidences().items():
            if len(p_nodes) != 0:
                for p_node in p_nodes:
                    edges.append(tuple([p_node, c_node]))
                    for key, value in network.get_distributions()[
                        c_node].items():
                        if (len(re.findall(r'\|\|.*?' + p_node + '.*?\\|\\|', key))
                            != 0) & (tuple([p_node, c_node]) not in freq_edges):
                            freq_edges.append(tuple([p_node, c_node]))
        network.set_edges(edges)
        network.set_freq_edges(freq_edges)
        # print(network.get_edges())
        # print(f'freq_edges{network.get_freq_edges()}')
    else:
        print('have not inited nodes in set edges')


def set_network_variable_card(network: Network):
    network.set_variable_card(
        {node.get_name(): node.get_variable_card() for node in network.get_nodes()})

# def check_lifted_nodes(network: Network):
#     # return the list of nodes which could be lifted.
#     # lifted mean A(x) do not need to represent A_1,...A_n nodes with bool values,
#     # could lifted as a node A(x) has the values= 0,...,n with frequency
#     nodes =network.get_nodes()
#     children_dict = network.get_children_dict()
#     distributions = network.get_distributions()
#     print(children_dict)
#     print(distributions)
#     lifted_nodes = []
#     for node in nodes:
#         # end node do not necessary to check lifted
#         flag = True
#         if node.get_name() in children_dict:
#             print(node.get_name())
#             for child in children_dict[node.get_name()]:
#                 for formula in distributions[child].keys():
#                     # only for atom formula could use lifting node
#                     # the lifting node only as frequency atomic formula.
#                     str = rf'\|\|{node.get_name()}{node.get_lower_para_from_node()[0]}\|\|'
#                     h1 = re.findall(,formula)
#                     h2 = re.findall(rf'{node.get_name()}{node.get_lower_para_from_node()[0]}',formula)
#                     # if len(re.findall(str, formula)) != len(re.findall(rf'{node.get_name()}')) > 0:
#
#                     # if node.get_name() in formula and rf'||{node.get_name()}{node.get_lower_para_from_node()[0]}||' not in formula:
#                     #     flag = False
#         else:
#             flag = False
#         if flag:
#             lifted_nodes.append(node.get_name())
#     return lifted_nodes