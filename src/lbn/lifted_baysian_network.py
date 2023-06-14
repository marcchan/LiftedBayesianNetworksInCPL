import re
from itertools import product
from lbn.input.network import Network
from lbn.input.node import Node
from lbn.network_helper import parse_to_network

# class LiftedNode(object):
#     def __init__(self, node: Node, flag):
#         self.abstract_node = node
#         self.lifted_flag = flag
#
#     #



class LiftedBaysianNetwork(object):
    def __init__(self, network: Network, flag: bool):
        self.abstract_network = network
        self.lifted_flag = flag

    def get_lifted_nodes(self):
        if self.lifted_flag:
            return check_lifted_nodes(self.abstract_network)

    def build_LBN(self):
        network = self.abstract_network
        # node_topo_dict = {'IsInfectious' : ['IsInfctious_p1', 'IsInfctious_p2', ...,'IsInfctious_p4'  ],
        #  'IsDiagnosed' : ['IsDiagnosed_p1', ..., 'IsDiagnosed_pn'],
        node_topo_dict = self.get_node_topo_dict()
        print(node_topo_dict)
        # evi_topo_dict =
        for node in network.get_nodes():
            pass
        #     # lifted_node = LiftedNode()
        #     if self.lifted_flag:
        #         if node.get_name() in self.get_lifted_nodes():
        #             pass
        #     else:
        #         generate_n_nodenames_as_list(node)

            # node_topo_dict[node.get_name()] = generate_n_nodenames_as_list(node)


            #  在没有lifting node的情况下， 所有variable = 'IsInfctious_p1'，...
            # variable_card always 2
            # evidence = [' p1, p2, pn']
            # evidence_card
            # state_names = {variable: [True, False]}
            #value 比较难， 需要通过distribution来

            # if node is root node


    def get_node_topo_dict(self):
        # node_topo_dict = {'IsInfectious' : ['IsInfctious_p1', ...,'IsInfctious_p4'  ],
        #  'IsDiagnosed' : ['IsDiagnosed_p1', ..., 'IsDiagnosed_pn'],
        node_topo_dict = {}
        for node in self.abstract_network.get_nodes():
            node_topo_dict[node.get_name()] = generate_n_nodenames_as_list(node)
        return node_topo_dict

    def get_evi_topo_dict(self):

        # evi_topo_dict = {
        # 'IsInfectious': {'IsInfectious_p1': set(),...,'IsInfectious_pn': set() }
        # 'IsDiagnosed': {'IsDiagnosed_p1':{'IsInfectious_p1'},...,'IsInfectious_pn': {'IsInfectious_pn'} }
        # 'Attends': {'Attends_p1_w1': set(), 'Attends_p1_w2': set(), 'Attends_pn_wm': set()}
        #  'IsShutDown': {'IsShutDown_w1': {'IsDiagnosed_p1',..., 'IsDiagnosed_pn','Attends_p1_w1',..., 'Attends_pn_w1' },
        #                 'IsShutDown_w2': {'IsDiagnosed_p1', ..., 'IsDiagnosed_pn', 'Attends_p1_w2', ..., 'Attends_pn_w2'}
        #  }
        # }
        network = self.abstract_network
        node_topo_dict = self.get_node_topo_dict()
        evi_topo_dict = {}
        evidences = network.get_evidences()
        nodes = network.get_nodes()
        edges = network.get_edges()
        for node in nodes:
            evi_topo = {}
            node_topo = node_topo_dict[node.get_name()]
            for n in node_topo:
                # root node
                if not evidences[node.get_name()]:
                    evi_topo[n] = set()
                else:
                    # non-lifted-edges which 1 to 1 for domain n, i.e.: IsInfectious_p1 -> IsDiagnosed_p1
                    if len(evidences[node.get_name()]) == 1:
                        for evi_name in evidences[node.get_name()]:
                            evi_node = network.get_node_from_name(evi_name)
                            if evi_node.get_domain() == node.get_domain():
                                temp_name = n
                                evi_topo[n] = str.replace(temp_name,node.get_name(),evi_node.get_name())
                    else:
                        # multi evidences todo
                        for evi_name in evidences[node.get_name()]:
                            evi_node = network.get_node_from_name(evi_name)

            evi_topo_dict[node.get_name()] = evi_topo
        print(evi_topo_dict)


    def get_node_value_dict(self, node):
        network = self.abstract_network
        node_distribution = network.get_distributions()[node.get_name()]
        if network.get_evidences()[node.get_name()]:
            probability = float(network.get_distributions()[node.get_name()]['self'])
            value_dict = [[probability, 1 - probability]]
        if len(node.get_domain()):
            pass
# def set_lifted_network_variable_card(lbn: LiftedBaysianNetwork):
#     pass
#
# def set_Lifted_network_statenames(LBN: LiftedBaysianNetwork):
#     # for any other case with multi parameter need to add case
#     statenames = {}
#     for node in network.get_nodes():
#         if len(node.get_domain()) == 0:
#             statenames[node.get_name()] = [True, False]
#         elif len(node.get_domain()) == 1:
#             statenames[node.get_name()] = list(
#                 range(node.get_variable_card()))
#         elif len(node.get_domain()) > 1:
#             # TODO: for multi parameter
#             print(f' TODO for multi parameter in set_statenames')
#     print(f'statename:{statenames}')
#     network.set_statenames(statenames)
#
#
# def set_lifted_network_edges(network):
#     if len(network.get_nodes()) != 0:
#         edges, freq_edges = [], []
#         for c_node, p_nodes in network.get_evidences().items():
#             if len(p_nodes) != 0:
#                 for p_node in p_nodes:
#                     edges.append(tuple([p_node, c_node]))
#                     for key, value in network.get_distributions()[
#                         c_node].items():
#                         if (len(re.findall(r'\|\|.*?' + p_node + '.*?\\|\\|', key))
#                             != 0) & (tuple([p_node, c_node]) not in freq_edges):
#                             freq_edges.append(tuple([p_node, c_node]))
#         network.set_edges(edges)
#         network.set_freq_edges(freq_edges)
#         # print(network.get_edges())
#         # print(f'freq_edges{network.get_freq_edges()}')
#     else:
#         print('have not inited nodes in set edges')


# def set_lifted_network_variable_card(network: Network):
#     network.set_variable_card(
#         {node.get_name(): node.get_variable_card() for node in network.get_nodes()})







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


def generate_n_nodenames_as_list(node: Node) -> list:
    # From Node to LiftedNode which we need to release domain into every node
    # example node : name: Qualified, Domain:{'T': '4'}             -> Qualified[t~1], ... Qualified[t~4]
    #                name: GoodSchool, Domain:{}'                   -> GoodSchool
    #                name: Something, Domain: {'T': '4', 'S': '3'}  -> Something[t~1,s~1], ... Something[t~4,s~3]

    normal_node_list = []
    domain = node.get_domain()
    for combination in product(*[range(int(value)) for value in domain.values()]):

        result_dict = {key: combination[i] + 1 for i, key in enumerate(domain.keys())}
        kv_pair = ''.join('_{}{}'.format(str.lower(key), value) for key, value in result_dict.items())

        # consider the situation which node without para, as Air_Is_Good and Fined in DAF graph
        name = f'{node.get_name()}' if kv_pair == '' else f'{node.get_name()}{kv_pair}'
        normal_node_list.append(name)
    return normal_node_list



if __name__ == "__main__":

    # FORMULA_FILE = '../../examples/infectious_disease/formula'
    # DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/DAF_v2/formula'
    # DOMAIN_FILE = '../../examples/DAF_v2/domain'
    # FORMULA_FILE = '../../examples/good_teacher/formula'
    # DOMAIN_FILE = '../../examples/good_teacher/domain'

    FORMULA_FILE = '../../examples/drive_air_city/formula'
    DOMAIN_FILE = '../../examples/drive_air_city/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/domain'
    # FORMULA_FILE = '../../examples/attend_grade_school/formula'
    # DOMAIN_FILE = '../../examples/attend_grade_school/domain'

    network = parse_to_network(FORMULA_FILE, DOMAIN_FILE)
    lifted_flag = False
    lbn = LiftedBaysianNetwork(network,lifted_flag)
    print(lbn.get_evi_topo_dict())
    # lbn.build_LBN()
    # print(check_lifted_nodes(network))
