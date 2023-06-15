import re
from itertools import product
from lbn.input.network import Network
from lbn.input.node import Node
from lbn.network_helper import parse_to_network
import numpy

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
        node_evi_topo_dict = self.get_evi_topo_dict()
        print(rf'Grounding all Nodes:{node_topo_dict}')
        print(rf'Evidences topo Nodes:{node_evi_topo_dict}')
        # evi_topo_dict =
        for node in network.get_nodes():
            if self.lifted_flag:
                if node.get_name() in self.get_lifted_nodes():
                    pass
            else:
                for n in node_topo_dict[node.get_name()]:
                    pass
                #  在没有lifting node的情况下， 所有variable = 'IsInfctious_p1'，...
                # variable_card always 2
                # evidence = ['p1, p2, pn']
                # evidence_card
                #value 比较难



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
                    evi_topo[n] = []
                else:
                    if len(evidences[node.get_name()]) == 1:
                        for evi_name in evidences[node.get_name()]:
                            evi_node = network.get_node_from_name(evi_name)
                            # as case IsDiagnosed_p1 evi_name: Is
                            if (evi_name,node.get_name()) not in network.get_freq_edges()\
                                    and evi_node.get_domain() == node.get_domain():
                                temp_name = n

                                evi_topo[n] = [str.replace(temp_name,node.get_name(),evi_node.get_name())]
                            else:
                                # as case AirIsGood , evi_name: Drive_x1
                                # evidence node topo list = [Drive_x1, ...Drive_xn]
                                evi_topo[n] = node_topo_dict[evi_name]

                    else:
                        # multi evidences
                        topo_list = []
                        for evi_name in evidences[node.get_name()]:
                            evi_node = network.get_node_from_name(evi_name)
                            if (evi_name, node.get_name()) not in network.get_freq_edges():
                                both_set = set(evi_node.get_domain().keys()) & set(node.get_domain().keys())
                                keyword_set = {item.lower() for item in both_set}
                                my_dict = {}
                                for s in keyword_set:
                                    if '_' + s in n:
                                        result = re.findall(rf'\_{s}[^\_]*', n)
                                        my_dict[s] = result[0]
                                res = evi_name
                                for s in keyword_set:
                                    res+=my_dict[s]
                                # todo deal with B_x1_p1 with evidences IsDiagnosed_p1 ,and B_x1, but the fact that IsDiagnosed_x1_p1, seems fixed, tobe confirmed
                                # topo_list.append(str.replace(temp_name, node.get_name(), evi_node.get_name()))
                                topo_list.append(res)
                            # for case which use frequency reduce the domain
                            else:
                                # case reduce domain totally
                                # CiryRating  and drive(d)
                                remain_para_set = set(evi_node.get_para().keys()) & set(node.get_para().keys())
                                if not remain_para_set:
                                    topo_list.extend(node_topo_dict[evi_name])
                                else:
                                    new_para_set = set()
                                    result_set = set(re.findall(r"_([a-zA-Z0-9]+)", n))
                                    for para in {element.lower() for element in remain_para_set}:
                                        for data in result_set:
                                            if para in data:
                                                new_para_set.add(data)
                                    for item in node_topo_dict[evi_name]:
                                        flag = True
                                        for p in new_para_set:
                                            if p not in item:
                                                flag = False
                                        if flag == True:
                                            topo_list.append(item)
                        evi_topo[n] = topo_list

            evi_topo_dict[node.get_name()] = evi_topo
        return evi_topo_dict


    def get_node_value_dict(self):
        network = self.abstract_network
        node_topo_list = self.get_node_topo_dict()
        evi_topo_list = self.get_evi_topo_dict()
        print(node_topo_list)
        print(evi_topo_list)
        value_dict ={}
        for node in network.get_nodes():
            node_value_dict = {}
            node_distribution = network.get_distributions()[node.get_name()]
            # root node
            if not network.get_evidences()[node.get_name()]:
                probability = float(node_distribution['self'])
                value_list = [[probability],[1 - probability]]
                for n in node_topo_list[node.get_name()]:
                        node_value_dict[n] = value_list
            else:
                # get subformula in node_distribution
                sub_formula_list = set()
                for line_formula, value in node_distribution.items():
                    temp_list = re.split(r' \& | or ', line_formula)
                    for temp_sub_formula in temp_list:
                        if '||' not in temp_sub_formula:
                            temp_sub_formula = str.replace(temp_sub_formula, "!", "")
                        else:
                            temp_sub_formula = re.sub(r'\s*[<>=]+\s*[\d.]*', '', temp_sub_formula)
                        sub_formula_list.add(temp_sub_formula)
                print(sub_formula_list)
                for n in node_topo_list[node.get_name()]:
                    evi_name_list = evi_topo_list[node.get_name()][n]
                    for evi_value_dict in enumerate_key_value({evi_n: [True, False] for evi_n in evi_name_list}):
                         # sub_formula_list : {'||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p'}
                        # evi_value_dict: {'Attends_p1_w1': True, 'Attends_p2_w1': True, 'Attends_p3_w1': True, 'Attends_p4_w1': True,
                         # 'IsDiagnosed_p1': True, 'IsDiagnosed_p2': True, 'IsDiagnosed_p3': True, 'IsDiagnosed_p4': True}
                         # sub_formula_value_dict : {'IsInfectious(p)': True, '||IsDiagnodes(p)||_p' : 0.3, '||IsDiagnosed(p) AND Attends(p,w)||_p': 0.2}
                        sub_formula_value_dict ={}
                        evi_node_list = [network.get_node_from_name(evi) for evi in network.get_evidences()[node.get_name()]]
                        for sub_formula in sub_formula_list:
                            if '||' not in sub_formula:
                                # CiryRatingDrop: AirIsGood & ||Drive(d)||_d > 0.5; !AirIsGood
                                # BlockedByTrafficJam(d): Drive(d) & ||Drive(d)||_d > 0.9
                                # CarAccident(d): Drive(d) & Drink(d)
                                # IsDiagnosed(p): IsInfectious(p) ; !IsInfectious(p)
                                for evi_node in evi_node_list:
                                    if evi_node.get_name() in sub_formula:
                                        keyword_set = {item.lower() for item in set(evi_node.get_domain().keys()) & set(node.get_domain().keys())}
                                        suffix_dict = {s:re.findall(rf'\_{s}[^\_]*', n)[0] for s in keyword_set if '_'+s in n}
                                        # print(suffix_dict)
                                        res = evi_node.get_name()
                                        for s in keyword_set:
                                            res = res + suffix_dict[s]
                                        sub_formula_value_dict[sub_formula] = evi_value_dict[res]
                                        # print(sub_formula_value_dict)
                            else:
                                # '||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p'
                                for evi_node in evi_node_list:
                                    # todo deal with parsing the frequency
                                    pass












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

def enumerate_key_value(d):
    keys = list(d.keys())
    value_lists = list(d.values())
    combinations = product(*value_lists)
    for combination in combinations:
        yield dict(zip(keys, combination))



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
    FORMULA_FILE = '../../examples/infectious_disease/formula_v1'
    DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/DAF_v2/formula'
    # DOMAIN_FILE = '../../examples/DAF_v2/domain'
    # FORMULA_FILE = '../../examples/good_teacher/formula'
    # DOMAIN_FILE = '../../examples/good_teacher/domain'
    # FORMULA_FILE = '../../examples/drive_drink/formula'
    # DOMAIN_FILE = '../../examples/drive_drink/domain'
    # FORMULA_FILE = '../../examples/drive_air_city/formula'
    # DOMAIN_FILE = '../../examples/drive_air_city/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_1_P_2/domain'
    # FORMULA_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/formula'
    # DOMAIN_FILE = '../../examples/pre_computing_case/test_case/C_3_P_2/domain'
    # FORMULA_FILE = '../../examples/attend_grade_school/formula'
    # DOMAIN_FILE = '../../examples/attend_grade_school/domain'
    #
    network = parse_to_network(FORMULA_FILE, DOMAIN_FILE)
    lifted_flag = False
    lbn = LiftedBaysianNetwork(network,lifted_flag)
    print(lbn.get_node_topo_dict())
    print(lbn.get_evi_topo_dict())
    lbn.get_node_value_dict()

