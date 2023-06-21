import operator
import re
from functools import reduce
from itertools import product

import numpy as np

from lbn.input.lifted_bayesian_network import LiftedBaysianNetwork
from lbn.input.node import Node
from lbn.network_helper import parse_to_network

from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from lbn.pre_computing import PreComputing
import datetime
from scipy.stats import binom


class Grounding(object):
    def __init__(self, network: LiftedBaysianNetwork, flag: bool):
        self.abstract_network = network
        self.lifting_flag = flag
        self.lifting_queue = check_lifting_nodes(self.abstract_network) if self.lifting_flag else []
        self.backup_evi_dict = {}

    def set_lifting_queue(self):
        if self.lifting_flag == False:
            self.lifting_queue = []
        else:
            self.lifting_queue = check_lifting_nodes(self.abstract_network)

    def get_lifting_queue(self):
        return self.lifting_queue

    def get_node_grounding_dict(self):
        # node_grounding_dict = {'IsInfectious' : ['IsInfctious_p1', ...,'IsInfctious_p4'  ],
        #  'IsDiagnosed' : ['IsDiagnosed_p1', ..., 'IsDiagnosed_pn'],
        node_grounding_dict = {}
        for node in self.abstract_network.get_nodes():
            if node.get_name() in self.lifting_queue:
                node_grounding_dict[node.get_name()] = [node.get_name()]
            else:
                node_grounding_dict[node.get_name()] = generate_n_nodenames_as_list(node)
        return node_grounding_dict

    def get_evi_grounding_dict(self):

        # evi_grounding_dict = {
        # 'IsInfectious': {'IsInfectious_p1': set(),...,'IsInfectious_pn': set() }
        # 'IsDiagnosed': {'IsDiagnosed_p1':{'IsInfectious_p1'},...,'IsInfectious_pn': {'IsInfectious_pn'} }
        # 'Attends': {'Attends_p1_w1': set(), 'Attends_p1_w2': set(), 'Attends_pn_wm': set()}
        #  'IsShutDown': {'IsShutDown_w1': {'IsDiagnosed_p1',..., 'IsDiagnosed_pn','Attends_p1_w1',..., 'Attends_pn_w1' },
        #                 'IsShutDown_w2': {'IsDiagnosed_p1', ..., 'IsDiagnosed_pn', 'Attends_p1_w2', ..., 'Attends_pn_w2'}
        #  }
        # }
        network = self.abstract_network
        node_grounding_dict = self.get_node_grounding_dict()
        evi_grounding_dict = {}
        evidences = network.get_evidences()
        nodes = network.get_nodes()
        edges = network.get_edges()

        for node in nodes:
            evi_grounding = {}
            node_grounding = node_grounding_dict[node.get_name()]
            for n in node_grounding:
                # root node
                if not evidences[node.get_name()]:
                    evi_grounding[n] = []
                else:
                    grounding_list = []
                    for evi_name in evidences[node.get_name()]:
                        evi_node = network.get_node_from_name(evi_name)
                        if (evi_name, node.get_name()
                            ) not in network.get_lifted_edges():
                            common_para_list = get_common_element_as_list(
                                list(evi_node.get_domain().keys()), list(node.get_domain().keys()))
                            keyword_list = [item.lower()
                                            for item in common_para_list]
                            para_suffix_dict = {}
                            for s in keyword_list:
                                if '_' + s in n:
                                    result = re.findall(rf'_{s}[^_]*', n)
                                    para_suffix_dict[s] = result[0]
                            res = evi_name
                            for s in keyword_list:
                                res += para_suffix_dict[s]
                            grounding_list.append(res)
                        # for case which use frequency reduce the domain
                        else:
                            # remain_para_list means that we need to evi_para_index one to one map to n_para_index
                            # that the para actually not be reduced
                            # for example n_x1 we need use remain x, to get
                            # evi_x1
                            sub_formula_list = get_sub_formula_set(
                                network.get_distributions()[node.get_name()])
                            freq_suffixs = set()
                            for s in sub_formula_list:
                                if '||' in s and evi_node.get_name(
                                ) + evi_node.get_lower_para_from_node()[0] in s:
                                    matches = re.findall(r'\|\|(_[^| ]*)', s)
                                    for match in matches:
                                        for suffix in match.split('_')[1:]:
                                            freq_suffixs.add(suffix)
                            evi_para_list = list(evi_node.get_domain().keys())
                            remain_para_list = [str.lower(evi_para) for evi_para in evi_para_list if
                                                str.lower(evi_para) not in freq_suffixs]
                            if not remain_para_list:
                                grounding_list.extend(node_grounding_dict[evi_name])
                            else:
                                new_para_list = []
                                result_list = re.findall(r"_([a-zA-Z0-9]+)", n)
                                for para in remain_para_list:
                                    for data in result_list:
                                        if para in data:
                                            new_para_list.append(data)
                                for item in node_grounding_dict[evi_name]:
                                    flag = True
                                    for p in new_para_list:
                                        if p not in item:
                                            flag = False
                                    if flag:
                                        grounding_list.append(item)
                    evi_grounding[n] = grounding_list
            evi_grounding_dict[node.get_name()] = evi_grounding
        return evi_grounding_dict


    def get_evi_variable_card_dict(self):
        node_grounding_dict = self.get_node_grounding_dict()
        evi_grounding_dict = self.get_evi_grounding_dict()
        network = self.abstract_network
        variable_card_dict = {}
        for node in network.get_nodes():
            variable_node_cards = {}
            evi_dict = evi_grounding_dict[node.get_name()]
            for n in node_grounding_dict[node.get_name()]:
                variable_card_list = []
                for eviname in evi_dict[n]:
                    if eviname in self.lifting_queue:
                        variable_card_list.append(network.get_node_from_name(eviname).get_variable_card())
                    else:
                        variable_card_list.append(2)
                variable_node_cards[n] = variable_card_list
            variable_card_dict[node.get_name()] = variable_node_cards
        return variable_card_dict

    def get_lifting_node_variable_dict(self):
        lifting_node_variable_dict = {}
        for node in self.abstract_network.get_nodes():
            if node.get_name() in self.lifting_queue:
                # currently only consider lifting node with single domain
                lifting_node_variable_dict[node.get_name()] = list(range(node.get_variable_card()))
        return lifting_node_variable_dict

    def update_info_lifting(self):
        self.lifting_flag = False
        self.set_lifting_queue()
        old_evi_dict = self.get_evi_grounding_dict()
        self.lifting_flag = True
        self.set_lifting_queue()
        backup_evi_dict = {}
        for node in self.abstract_network.get_nodes():
            if node.get_name() in self.lifting_queue:
                value = old_evi_dict[node.get_name()]
                backup_evi_dict[node.get_name()] = value

        self.backup_evi_dict = backup_evi_dict



    def get_node_value_dict_with_lifting(self):

        network = self.abstract_network
        if self.lifting_flag:
            lbn.update_info_lifting()
        node_grounding_list = self.get_node_grounding_dict()
        evi_grounding_list = self.get_evi_grounding_dict()
        value_dict = {}
        for node in network.get_nodes():
            print(rf'-------')
            print(rf'current node is {node.get_name()}')
            node_value_dict = {}

            node_distribution = network.get_distributions()[node.get_name()]
            # root node
            if not network.get_evidences()[node.get_name()]:
                probability = float(node_distribution['self'])
                if node.get_name() not in self.lifting_queue:
                    value_list = [[probability], [1 - probability]]
                    for n in node_grounding_list[node.get_name()]:
                        node_value_dict[n] = value_list
                else:
                    for n in node_grounding_list[node.get_name()]:
                        value_list = [[binom.pmf(k,node.get_variable_card()-1,probability)] for k in list(range(node.get_variable_card()))]
                        node_value_dict[n] = value_list
                value_dict[node.get_name()] = node_value_dict
            else:
                # get subformula in node_distribution
                # sub_formula_list : {'||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p'}
                sub_formula_set = get_sub_formula_set(node_distribution)
                print(sub_formula_set)

                # grounding the node for example n : Attends_x1_p1,
                # IsDiagnosed_p1
                for n in node_grounding_list[node.get_name()]:
                    # print(rf'grounding node :{n}')
                    evi_name_list = evi_grounding_list[node.get_name()][n]
                    grounding_value_list = []
                    evi_variable_dict = {}
                    lifting_value_list = []


                    for evi_n in evi_name_list:
                        if evi_n in self.lifting_queue:
                            evi_variable_dict[evi_n] = self.get_lifting_node_variable_dict()[evi_n]
                        else:
                            evi_variable_dict[evi_n] = [True, False]
                    for evi_value_dict in enumerate_key_value(evi_variable_dict):
                        # sub_formula_list : {'||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p'}
                        # evi_value_dict: {'Attends_p1_w1': True, 'Attends_p2_w1': True, 'Attends_p3_w1': True, 'Attends_p4_w1': True,
                        # 'IsDiagnosed_p1': True, 'IsDiagnosed_p2': True, 'IsDiagnosed_p3': True, 'IsDiagnosed_p4': True}
                        # sub_formula_value_dict : {'IsInfectious(p)': True, '||IsDiagnodes(p)||_p' : 0.3, '||IsDiagnosed(p) AND Attends(p,w)||_p': 0.2}

                        # 'IsShutDown_w1': ['IsDiagnosed_p1', 'IsDiagnosed_p2', 'IsDiagnosed_p3', 'IsDiagnosed_p4',
                        #                   'Attends_p1_w1', 'Attends_p2_w1', 'Attends_p3_w1',
                        #                   'Attends_p4_w1'],
                        # 'IsShutDown_w2': ['IsDiagnosed_p1', 'IsDiagnosed_p2',
                        #                                                       'IsDiagnosed_p3', 'IsDiagnosed_p4',
                        #                                                       'Attends_p1_w2', 'Attends_p2_w2',
                        #                                                       'Attends_p3_w2', 'Attends_p4_w2']
                        iterate_time = 1
                        temp_evi_value_dict = evi_value_dict
                        temp_n = n
                        temp_evi_name_list = evi_name_list
                        # for lifitng node, [0.8,0.3,0.3,0.8]
                        probability_list = []
                        grounding_n_list = generate_n_nodenames_as_list(node)
                        if n in self.lifting_queue:
                                iterate_time = node.get_variable_card() - 1
                        for i in range(iterate_time):
                            # temp_evi_value_dict
                            # temp_evi_value_dict = self.backup_evi_dict[n]
                            # evi_name_list 需要处理一下
                            if node.get_name() in self.lifting_queue:
                                temp_n = grounding_n_list[i]
                                temp_evi_value_dict =  { n: evi_value_dict[n] for n in self.backup_evi_dict[n][temp_n] if n in list(evi_value_dict.keys())}
                                temp_evi_name_list = self.backup_evi_dict[n][temp_n]

                            sub_formula_value_dict = {}
                            evi_node_list = [network.get_node_from_name(
                                evi) for evi in network.get_evidences()[node.get_name()]]
                            for sub_formula in sub_formula_set:
                                lifting_flag = False
                                # print(rf'current analysis the sub_formula: {sub_formula}')
                                for lifting_name in self.lifting_queue:
                                    if lifting_name in sub_formula:
                                        lifting_flag = True
                                if not lifting_flag:
                                    if '||' not in sub_formula:
                                        # CiryRatingDrop: AirIsGood & ||Drive(d)||_d > 0.5; !AirIsGood
                                        # BlockedByTrafficJam(d): Drive(d) & ||Drive(d)||_d > 0.9
                                        # CarAccident(d): Drive(d) & Drink(d)
                                        # IsDiagnosed(p): IsInfectious(p) ;
                                        # !IsInfectious(p)
                                        for evi_node in evi_node_list:
                                            if evi_node.get_name() in sub_formula:
                                                keyword_set = {
                                                    item.lower() for item in set(
                                                        evi_node.get_domain().keys()) & set(
                                                        node.get_domain().keys())}
                                                suffix_dict = {
                                                    s: re.findall(
                                                        rf'_{s}[^_]*',
                                                        temp_n)[0] for s in keyword_set if '_' +
                                                    s in temp_n}
                                                print(suffix_dict)
                                                res = evi_node.get_name()
                                                for s in keyword_set:
                                                    res = res + suffix_dict[s]
                                                sub_formula_value_dict[sub_formula] = temp_evi_value_dict[res]
                                                # print(sub_formula_value_dict)
                                    else:
                                        # '||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p', ||A(x,y) AND B(x,y,z)||_x_y
                                        # suffix_dict = {'p': n, 'x': m, 'y': q}
                                        conditional_flag = False
                                        changed_sub_formula = sub_formula
                                        conditional_formula = ''

                                        if ' | ' in sub_formula:
                                            conditional_flag = True
                                            conditional_formula = re.findall(
                                                r' \| (.*?)\|\|', changed_sub_formula)[0]
                                            changed_sub_formula = str.replace(
                                                changed_sub_formula, ' | ', ' AND ')
                                        suffix_dict = {}
                                        suffixes = [s.strip().replace('_', '') for s in sub_formula.split(
                                            "||") if s.strip().startswith("_")]
                                        for suffix in suffixes:
                                            for evi_node in evi_node_list:
                                                # print(evi_node.get_domain())
                                                if str.upper(suffix) in list(
                                                        evi_node.get_domain().keys()):
                                                    if str.upper(suffix) not in list(
                                                            suffix_dict.keys()):
                                                        suffix_dict[suffix] = int(
                                                            evi_node.get_domain()[str.upper(suffix)])

                                        suffix_values = [
                                            suffix_dict[suffix] for suffix in suffixes]
                                        combinations = list(
                                            product(*(range(1, value + 1) for value in suffix_values)))
                                        suffix_enumerate_list = [
                                            f"_{'_'.join(f'{key}{i}' for key, i in zip(suffix, combination))}" for combination in combinations]
                                        # print(suffix_enumerate_list)
                                        # print(evi_name_list)

                                        # get result_list as [True, False, True,
                                        # False,...]
                                        result_list = []
                                        conditional_list = []
                                        changed_sub_formula = str.replace(
                                            changed_sub_formula, 'AND', 'and')
                                        changed_sub_formula = str.replace(
                                            changed_sub_formula, 'OR', 'or')
                                        if conditional_flag:
                                            conditional_formula = str.replace(
                                                conditional_formula, 'AND', 'and')
                                            conditional_formula = str.replace(
                                                conditional_formula, 'OR', 'or')
                                        pattern = r"\|\|(.*?)\|\|"
                                        # conditonal proabbility || A(x) | B(x,y)||_x
                                        # 在这里修改
                                        changed_sub_formula = re.search(
                                            pattern, changed_sub_formula).group(1)
                                        for suffix_enumerate in suffix_enumerate_list:
                                            temp_formula = changed_sub_formula
                                            temp_conditional_formula = ''
                                            if conditional_flag:
                                                temp_conditional_formula = conditional_formula
                                            grounding_pairs = [
                                                evi_name for evi_name in temp_evi_name_list if suffix_enumerate in evi_name]
                                            for evi_node in evi_node_list:
                                                evi_name_with_para = evi_node.get_name(
                                                ) + evi_node.get_lower_para_from_node()[0]
                                                if evi_name_with_para in temp_formula:
                                                    for grounding in grounding_pairs:
                                                        if evi_node.get_name() in grounding:
                                                            new_value = str(
                                                                temp_evi_value_dict[grounding])
                                                            temp_formula = str.replace(
                                                                temp_formula, evi_name_with_para, new_value)
                                                            # conditional frequency
                                                            # implemtation here
                                                            if conditional_flag:
                                                                temp_conditional_formula = str.replace(
                                                                    temp_conditional_formula, evi_name_with_para, new_value)

                                            # print(temp_formula)

                                            eval_result = eval(temp_formula)
                                            result_list.append(eval_result)
                                            if conditional_flag:
                                                conditional_eval_result = eval(
                                                    temp_conditional_formula)
                                                conditional_list.append(
                                                    conditional_eval_result)

                                        # print(rf' when evi_value_dict as {evi_value_dict}')
                                        # print(rf' {sub_formula} with the result {result_list}')
                                        # caluate relative frequency value

                                        baseline_counter = reduce(
                                            operator.mul, list(suffix_dict.values()))
                                        frequency_value = result_list.count(
                                            True) / baseline_counter
                                        if conditional_flag:
                                            conditional_value = conditional_list.count(
                                                True) / baseline_counter
                                            sub_formula_value_dict[sub_formula] = frequency_value / \
                                                conditional_value if conditional_value != 0 else 0
                                        else:
                                            sub_formula_value_dict[sub_formula] = frequency_value
                                else:
                                    changed_sub_formula = sub_formula
                                    # sub_formula contains lifting node
                                    # sub_formula example: ||Drive(d)||_d
                                    # 先处理||, 提取Drive(d)
                                    pattern = r"\|\|(.*?)\|\|"
                                    changed_sub_formula = re.search(pattern, changed_sub_formula).group(1)
                                    # print(changed_sub_formula)
                                    for lifting_name in self.lifting_queue:
                                        if lifting_name in changed_sub_formula:
                                            lifting_node = network.get_node_from_name(lifting_name)
                                            baseline_counter = lifting_node.get_variable_card() - 1
                                            sub_formula_value_dict[sub_formula] = int(evi_value_dict[lifting_name])/baseline_counter

                                # print(rf'here:{sub_formula_value_dict}')

                            # get grounding node n value dict
                            for cond, value in node_distribution.items():
                                temp_cond = str.replace(cond, '&', 'and')
                                temp_cond = str.replace(temp_cond, '!', 'not ')
                                for sub_f, sub_value in sub_formula_value_dict.items():
                                    temp_cond = str.replace(
                                        temp_cond, sub_f, str(sub_value))
                                # print(temp_cond)
                                eval_value = eval(temp_cond)
                                if eval_value:
                                    if node.get_name() in self.lifting_queue:
                                        probability_list.append(float(value))
                                    else:
                                        grounding_value_list.append(float(value))
                        print(rf'{probability_list} when {evi_value_dict}')
                        if node.get_name() in self.lifting_queue:
                            # if np.array_equal(lifting_value_list, np.empty((5,1))):
                            if not len(lifting_value_list):
                                lifting_value_list = np.array(calculate_probability(probability_list))\
                                    .reshape(node.get_variable_card(),1)
                            else:
                                lifting_value_list = np.concatenate((lifting_value_list,
                                                                     np.array(calculate_probability(probability_list)). reshape(node.get_variable_card(),1))
                                                                    , axis=1)

                    # print(rf'evi_node_list_length:{len(evi_name_list)}')
                    # print(rf'In {n} length of 1d - list:{len(grounding_value_list)}')
                    if node.get_name() not in self.lifting_queue:
                        result_array = 1 - np.array(grounding_value_list)
                        combined_2d_array = np.vstack(
                            (grounding_value_list, result_array))
                        node_value_dict[n] = combined_2d_array
                    else:
                        node_value_dict[n] = lifting_value_list

                value_dict[node.get_name()] = node_value_dict
        print(value_dict)
        return value_dict







    def build_LBN(self):
        network = self.abstract_network
        # node_grounding_dict = {'IsInfectious' : ['IsInfctious_p1', 'IsInfctious_p2', ...,'IsInfctious_p4'  ],
        #  'IsDiagnosed' : ['IsDiagnosed_p1', ..., 'IsDiagnosed_pn'],

        node_grounding_dict = self.get_node_grounding_dict()
        print(rf'Grounding all Nodes:{node_grounding_dict}')
        node_evi_grounding_dict = self.get_evi_grounding_dict()
        print(rf'Evidences grounding Nodes:{node_evi_grounding_dict}')
        # print(value_dict)
        value_dict = self.get_node_value_dict_with_lifting()
        evi_variable_card_dict = self.get_evi_variable_card_dict()
        lbn_model = BayesianNetwork(self.get_edges())


        for node in network.get_nodes():
            evi_grounding_dict = node_evi_grounding_dict[node.get_name()]
            evi_variable_card = evi_variable_card_dict[node.get_name()]
            grounding_value_dict = value_dict[node.get_name()]
            for n in node_grounding_dict[node.get_name()]:
                lbn_model.add_node(n)
                if not evi_grounding_dict[n]:
                    if n in self.lifting_queue:
                        lbn_model.add_cpds(
                            TabularCPD(
                                variable=n,
                                variable_card=node.get_variable_card(),
                                values=grounding_value_dict[n]))
                    else:
                        lbn_model.add_cpds(
                            TabularCPD(
                                variable=n,
                                variable_card=2,
                                values=grounding_value_dict[n]))
                else:
                    if n in self.lifting_queue:
                        lbn_model.add_cpds(TabularCPD(variable=n,
                                                      variable_card=node.get_variable_card(),
                                                      values=grounding_value_dict[n],
                                                      evidence=evi_grounding_dict[n],
                                                      evidence_card=evi_variable_card[n]))
                    else:
                        lbn_model.add_cpds(TabularCPD(variable=n,
                                                      variable_card=2,
                                                      values=grounding_value_dict[n],
                                                      evidence=evi_grounding_dict[n],
                                                      evidence_card=evi_variable_card[n]))

        return lbn_model

    def get_edges(self):
        nodes = self.abstract_network.get_nodes()
        node_evi_grounding_dict = self.get_evi_grounding_dict()
        node_grounding_dict = self.get_node_grounding_dict()
        edges = []
        for node in nodes:
            if network.get_evidences():
                evi_grounding_dict = node_evi_grounding_dict[node.get_name()]
                for n in node_grounding_dict[node.get_name()]:
                    evi_grounding = evi_grounding_dict[n]
                    for p_n in evi_grounding:
                        edges.append((p_n, n))
        return edges


    def get_node_value_dict(self):
        network = self.abstract_network
        node_grounding_list = self.get_node_grounding_dict()
        evi_grounding_list = self.get_evi_grounding_dict()
        value_dict = {}
        for node in network.get_nodes():
            print(rf'-------')
            print(rf'current node is {node.get_name()}')
            node_value_dict = {}
            node_distribution = network.get_distributions()[node.get_name()]
            # root node
            if not network.get_evidences()[node.get_name()]:
                probability = float(node_distribution['self'])
                if node.get_name() not in self.lifting_queue:

                    value_list = [[probability], [1 - probability]]
                    for n in node_grounding_list[node.get_name()]:
                        node_value_dict[n] = value_list
                    value_dict[node.get_name()] = node_value_dict
                else:
                    if len(node.get_domain()) == 1:
                        doamin = int(list(node.get_domain().values())[0])
                        node_value_dict = [[binom.pmf(k,doamin,probability)]for k in range(doamin+1)]
                        value_dict[node.get_name()] = node_value_dict

            else:
                # get subformula in node_distribution
                # sub_formula_list : {'||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p'}
                sub_formula_set = get_sub_formula_set(node_distribution)
                print(rf'sub_formula_set for node {node.get_name()} are {sub_formula_set}')
                # grounding the node for example n : Attends_x1_p1,
                # IsDiagnosed_p1
                for n in node_grounding_list[node.get_name()]:
                    # print(rf'grounding node :{n}')
                    evi_name_list = evi_grounding_list[node.get_name()][n]
                    grounding_value_list = []
                    variable_dict = {}
                    # evinode variabel dict
                    for evi_n in evi_name_list:
                        if evi_n in self.lifting_queue:
                            lifting_node = network.get_node_from_name(evi_n)
                            # todo currently only consider the single para for lifting node
                            if len(lifting_node.get_domain()) == 1:
                                # available variable for lifting node
                                variable_dict[evi_n] = self.get_lifting_node_variable_dict()[evi_n]
                        else:
                            variable_dict[evi_n] = [True, False]
                    print(variable_dict)
                    for evi_value_dict in enumerate_key_value(variable_dict):
                        # sub_formula_list : {'||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p'}
                        # evi_value_dict: {'Attends_p1_w1': True, 'Attends_p2_w1': True, 'Attends_p3_w1': True, 'Attends_p4_w1': True,
                        # 'IsDiagnosed_p1': True, 'IsDiagnosed_p2': True, 'IsDiagnosed_p3': True, 'IsDiagnosed_p4': True}
                        # sub_formula_value_dict : {'IsInfectious(p)': True, '||IsDiagnodes(p)||_p' : 0.3, '||IsDiagnosed(p) AND Attends(p,w)||_p': 0.2}
                        sub_formula_value_dict = {}
                        evi_node_list = [network.get_node_from_name(
                            evi) for evi in network.get_evidences()[node.get_name()]]
                        for sub_formula in sub_formula_set:
                            # print(rf'current analysis the sub_formula: {sub_formula}')
                            if '||' not in sub_formula:
                                # CiryRatingDrop: AirIsGood & ||Drive(d)||_d > 0.5; !AirIsGood
                                # BlockedByTrafficJam(d): Drive(d) & ||Drive(d)||_d > 0.9
                                # CarAccident(d): Drive(d) & Drink(d)
                                # IsDiagnosed(p): IsInfectious(p) ;
                                # !IsInfectious(p)
                                for evi_node in evi_node_list:
                                    if evi_node.get_name() in sub_formula:
                                        keyword_set = {
                                            item.lower() for item in set(
                                                evi_node.get_domain().keys()) & set(
                                                node.get_domain().keys())}
                                        suffix_dict = {
                                            s: re.findall(
                                                rf'_{s}[^_]*',
                                                n)[0] for s in keyword_set if '_' +
                                            s in n}
                                        # print(suffix_dict)
                                        res = evi_node.get_name()
                                        for s in keyword_set:
                                            res = res + suffix_dict[s]
                                        sub_formula_value_dict[sub_formula] = evi_value_dict[res]
                                        # print(sub_formula_value_dict)
                            else:
                                # '||IsDiagnodes(p)||_p', '||IsDiagnosed(p) AND Attends(p,w)||_p', ||A(x,y) AND B(x,y,z)||_x_y
                                # suffix_dict = {'p': n, 'x': m, 'y': q}
                                conditional_flag = False
                                changed_sub_formula = sub_formula
                                conditional_formula = ''

                                if ' | ' in sub_formula:
                                    conditional_flag = True
                                    conditional_formula = re.findall(
                                        r' \| (.*?)\|\|', changed_sub_formula)[0]
                                    changed_sub_formula = str.replace(
                                        changed_sub_formula, ' | ', ' AND ')
                                suffix_dict = {}
                                suffixes = [s.strip().replace('_', '') for s in sub_formula.split(
                                    "||") if s.strip().startswith("_")]
                                for suffix in suffixes:
                                    for evi_node in evi_node_list:
                                        # print(evi_node.get_domain())
                                        if str.upper(suffix) in list(
                                                evi_node.get_domain().keys()):
                                            if str.upper(suffix) not in list(
                                                    suffix_dict.keys()):
                                                suffix_dict[suffix] = int(
                                                    evi_node.get_domain()[str.upper(suffix)])
                                baseline_counter = reduce(
                                    operator.mul, list(suffix_dict.values()))
                                suffix_values = [
                                    suffix_dict[suffix] for suffix in suffixes]
                                combinations = list(
                                    product(*(range(1, value + 1) for value in suffix_values)))
                                suffix_enumerate_list = [
                                    f"_{'_'.join(f'{key}{i}' for key, i in zip(suffix, combination))}" for combination in combinations]
                                # print(suffix_enumerate_list)
                                # print(evi_name_list)

                                # get result_list as [True, False, True,
                                # False,...]
                                result_list = []
                                conditional_list = []
                                changed_sub_formula = str.replace(
                                    changed_sub_formula, 'AND', 'and')
                                changed_sub_formula = str.replace(
                                    changed_sub_formula, 'OR', 'or')
                                if conditional_flag:
                                    conditional_formula = str.replace(
                                        conditional_formula, 'AND', 'and')
                                    conditional_formula = str.replace(
                                        conditional_formula, 'OR', 'or')
                                pattern = r"\|\|(.*?)\|\|"
                                # conditonal proabbility || A(x) | B(x,y)||_x
                                changed_sub_formula = re.search(
                                    pattern, changed_sub_formula).group(1)
                                for suffix_enumerate in suffix_enumerate_list:
                                    temp_formula = changed_sub_formula
                                    if conditional_flag:
                                        temp_conditional_formula = conditional_formula
                                    grounding_pairs = [
                                        evi_name for evi_name in evi_name_list if suffix_enumerate in evi_name]
                                    for evi_node in evi_node_list:
                                        evi_name_with_para = evi_node.get_name(
                                        ) + evi_node.get_lower_para_from_node()[0]
                                        if evi_name_with_para in temp_formula:
                                            for grounding in grounding_pairs:
                                                if evi_node.get_name() in grounding:
                                                    new_value = str(
                                                        evi_value_dict[grounding])
                                                    temp_formula = str.replace(
                                                        temp_formula, evi_name_with_para, new_value)
                                                    # conditional frequency
                                                    # implemtation here
                                                    if conditional_flag:
                                                        temp_conditional_formula = str.replace(
                                                            temp_conditional_formula, evi_name_with_para, new_value)

                                    # print(temp_formula)

                                    eval_result = eval(temp_formula)
                                    result_list.append(eval_result)
                                    if conditional_flag:
                                        conditional_eval_result = eval(
                                            temp_conditional_formula)
                                        conditional_list.append(
                                            conditional_eval_result)

                                # print(rf' when evi_value_dict as {evi_value_dict}')
                                # print(rf' {sub_formula} with the result {result_list}')
                                # caluate relative frequency value

                                frequency_value = result_list.count(
                                    True) / baseline_counter
                                if conditional_flag:
                                    conditional_value = conditional_list.count(
                                        True) / baseline_counter
                                    sub_formula_value_dict[sub_formula] = frequency_value / \
                                        conditional_value if conditional_value != 0 else 0
                                else:
                                    sub_formula_value_dict[sub_formula] = frequency_value

                            # print(rf'here:{sub_formula_value_dict}')

                        # get grounding node n value dict
                        for cond, value in node_distribution.items():
                            temp_cond = str.replace(cond, '&', 'and')
                            temp_cond = str.replace(temp_cond, '!', 'not ')
                            for sub_f, sub_value in sub_formula_value_dict.items():
                                temp_cond = str.replace(
                                    temp_cond, sub_f, str(sub_value))
                            # print(temp_cond)
                            eval_value = eval(temp_cond)
                            if eval_value:
                                grounding_value_list.append(float(value))
                    # print(rf'evi_node_list_length:{len(evi_name_list)}')
                    # print(rf'In {n} length of 1d - list:{len(grounding_value_list)}')
                    result_array = 1 - np.array(grounding_value_list)
                    combined_2d_array = np.vstack(
                        (grounding_value_list, result_array))
                    node_value_dict[n] = combined_2d_array
                value_dict[node.get_name()] = node_value_dict
        # print(value_dict)
        return value_dict









def calculate_probability(prob_list):
    n = len(prob_list)
    dp = np.zeros(n + 1)
    dp[0] = 1
    for i in range(n):
        dp1 = np.zeros(n + 1)
        for j in range(n):
            dp1[j] += dp[j] * (1 - prob_list[i])  # 当前节点为 False
            dp1[j + 1] += dp[j] * prob_list[i]  # 当前节点为 True
            # dp1[j] += dp[j] * (prob_list[i])  # 当前节点为 False
            # dp1[j + 1] += dp[j] * (1- prob_list[i])  # 当前节点为 True
        dp = dp1
    return dp


def get_common_element_as_list(list1, list2):
    return [l for l in list1 if l in list2]


def get_sub_formula_set(distribution: dict):
    sub_formula_set = set()
    for line_formula, value in distribution.items():
        temp_list = re.split(r' & | or ', line_formula)
        for temp_sub_formula in temp_list:
            if '||' not in temp_sub_formula:
                temp_sub_formula = str.replace(temp_sub_formula, "!", "")
            else:
                temp_sub_formula = re.sub(
                    r'\s*[<>=]+\s*[\d.]*', '', temp_sub_formula)
            sub_formula_set.add(temp_sub_formula)
    return sub_formula_set


def enumerate_key_value(d):
    keys = list(d.keys())
    value_lists = list(d.values())
    combinations = product(*value_lists)
    for combination in combinations:
        yield dict(zip(keys, combination))


def check_lifting_nodes(network: LiftedBaysianNetwork):
    # return the list of nodes which could be lifted.
    # lifted mean A(x) do not need to represent A_1,...A_n nodes with bool values,
    # could lifted as a node A(x) has the values= 0,...,n with frequency
    nodes = network.get_nodes()
    children_dict = network.get_children_dict()
    distributions = network.get_distributions()
    lifting_nodes = []
    for node in nodes:
        # end node do not necessary to check lifting
        flag = True
        if node.get_name() in children_dict:
            for child in children_dict[node.get_name()]:
                for formula in distributions[child].keys():
                    # 比较A(x) ||A(x)|| 出现的次数是否一致即可， ||... A(x) ...|| 就代表着 A(x)出现的次数 > ||A(x)||
                    node_with_para = node.get_name() + node.get_lower_para_from_node()[0]
                    node_with_para_in_freq = '||'+ node_with_para + '||'
                    h1 = re.findall(re.escape(node_with_para_in_freq), formula)
                    h2 = re.findall(re.escape(node_with_para), formula)
                    if len(h1) != len(h2) :
                        flag = False
        else:
            flag = False
        if flag:
            lifting_nodes.append(node.get_name())
    return lifting_nodes


def generate_n_nodenames_as_list(node: Node) -> list:
    # From Node to Lifting Node which we need to release domain into every node
    # example node : name: Qualified, Domain:{'T': '4'}             -> Qualified[t~1], ... Qualified[t~4]
    #                name: GoodSchool, Domain:{}'                   -> GoodSchool
    # name: Something, Domain: {'T': '4', 'S': '3'}  -> Something[t~1,s~1],
    # ... Something[t~4,s~3]

    normal_node_list = []
    domain = node.get_domain()
    for combination in product(*[range(int(value))
                               for value in domain.values()]):

        result_dict = {
            key: combination[i] +
            1 for i,
            key in enumerate(
                domain.keys())}
        kv_pair = ''.join('_{}{}'.format(str.lower(key), value)
                          for key, value in result_dict.items())

        # consider the situation which node without para, as Air_Is_Good and
        # Fined in DAF graph
        name = f'{node.get_name()}' if kv_pair == '' else f'{node.get_name()}{kv_pair}'
        normal_node_list.append(name)
    return normal_node_list


if __name__ == "__main__":

    # FORMULA_FILE = '../../examples/infectious_disease/formula'
    # DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/infectious_disease/formula_v1'
    # DOMAIN_FILE = '../../examples/infectious_disease/domain'
    FORMULA_FILE = '../../examples/infectious_disease/formula_v2'
    DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/infectious_disease/formula_v3'
    # DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/infectious_disease/formula_v4'
    # DOMAIN_FILE = '../../examples/infectious_disease/domain'
    # FORMULA_FILE = '../../examples/DAF_v2/formula'
    # DOMAIN_FILE = '../../examples/DAF_v2/domain'


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
    # FORMULA_FILE = '../../examples/test/formula'
    # DOMAIN_FILE = '../../examples/test/domain'
    #
    network = parse_to_network(FORMULA_FILE, DOMAIN_FILE)
    lifting_flag = True
    # print(rf'nodes = { [n.get_name() for n in network.get_nodes()]}')
    # network = PreComputing(network).optimize_network()
    # print(check_lifting_nodes(network))

    # print(f'the new network from Pre-Computing is {network}')

    lbn = Grounding(network, lifting_flag)
    print(lbn.lifting_queue)
    # print(lbn.get_node_grounding_dict())
    # print(lbn.get_evi_grounding_dict())

    # # print(lbn.get_node_value_dict())
    # # print(lbn.get_evi_variable_card_dict())
    # print(lbn.get_node_value_dict_with_lifting())
    #
    # # starttime = datetime.datetime.now()
    lbn_model = lbn.build_LBN()
    infer = VariableElimination(lbn_model)

    print(infer.query(["IsShutDown"]))
    # print(infer.query(["IsShutDown_w1"]))
    # print(infer.query(["IsShutDown_w2"]))
    print(infer.query(["AllPeopleRemoteWorking"]))
    # print(infer.query(["AllPeopleRemoteWorking", "IsShutDown"]))
    print(infer.query(["AllPeopleRemoteWorking", "IsShutDown_w1"]))
    # print(infer.query(["AllPeopleRemoteWorking","IsShutDown_w1","IsShutDown_w2"]))

    # endtime = datetime.datetime.now()
    # print(endtime - starttime)

    # print(infer.query(["CityRatingDrop"]))
    # print(infer.query(["AllPeopleRemoteWorking"]))

    # starttime = datetime.datetime.now()

    # print(infer.query(["CityRatingDrop"]))
    # endtime = datetime.datetime.now()
    # print (endtime - starttime)
