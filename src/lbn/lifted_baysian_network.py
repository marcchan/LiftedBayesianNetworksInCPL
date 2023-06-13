import re
from itertools import product

from lbn.input.network import Network
from lbn.input.node import Node
from lbn.network_helper import parse_to_network


class LiftedBaysianNetwork(object):
    def __init__(self, network: Network, flag: bool):
        self.abstract_network = network
        self.lifted_flag = flag


    def get_lifted_nodes(self):
        if self.lifted_flag:
            return check_lifted_nodes(self.abstract_network)

    def build_LBN(self):
        network = self.abstract_network
        for node in network.get_nodes():
            if node.get_name() in self.get_lifted_nodes():
                    pass
                    # todo


# IsDiagnosed
# for n+1 in Drive.domain():
#     cpd_d1 = TabularCPD(
#         variable='Drives_x1',
#         variable_card=2,
#         values=[[0.5],
#                 [0.5]],
#         state_names={'Drives_x1': [True, False]})
# Attends::{P: person, W: workplace}
# for
#     Attends_p1_w1
#
#
# IsShutDown::{W: workplace}
# ||IsDiagnosed(p) & Attends(p,w)||_p > 0 : 1
# ||IsDiagnosed(p) & Attends(p,w)||_p <= 0 : 0
#
# ID_p1 = 1 , ID_p2 = 0, Att_p1_w1 = 0, Att_p2_w1= 0
#
# IsShutDown{W}
# for w
#     w1

def check_lifted_nodes(network: Network):
    # return the list of nodes which could be lifted.
    # lifted mean A(x) do not need to represent A_1,...A_n nodes with bool values,
    # could lifted as a node A(x) has the values= 0,...,n with frequency
    nodes =network.get_nodes()
    children_dict = network.get_children_dict()
    distributions = network.get_distributions()
    print(children_dict)
    print(distributions)
    lifted_nodes = []
    for node in nodes:
        # end node do not necessary to check lifted
        flag = True
        if node.get_name() in children_dict:
            for child in children_dict[node.get_name()]:
                for formula in distributions[child].keys():
                    # only for atom formula could use lifting node
                    str = rf'||{node.get_name()}{node.get_lower_para_from_node()[0]}||'
                    if node.get_name() in formula and rf'||{node.get_name()}{node.get_lower_para_from_node()[0]}||' not in formula:
                        flag = False
        else:
            flag = False
        if flag:
            lifted_nodes.append(node.get_name())
    return lifted_nodes




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



if __name__ == "__main__":

    # FORMULA_FILE = '../../examples/infectious_disease/formula'
    # DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/DAF_v2/formula'
    # DOMAIN_FILE = '../../examples/DAF_v2/domain'
    # FORMULA_FILE = '../../examples/good_teacher/formula'
    # DOMAIN_FILE = '../../examples/good_teacher/domain'

    # FORMULA_FILE = '../../examples/drive_air_city/formula'
    # DOMAIN_FILE = '../../examples/drive_air_city/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/domain'
    FORMULA_FILE = '../../examples/attend_grade_school/formula'
    DOMAIN_FILE = '../../examples/attend_grade_school/domain'

    network = parse_to_network(FORMULA_FILE, DOMAIN_FILE)
    # lifted_flag = True
    # lbn = LiftedBaysianNetwork(network,lifted_flag)
    print(check_lifted_nodes(network))