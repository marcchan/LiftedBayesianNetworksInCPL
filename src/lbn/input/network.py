# from lbn.parse_formula_into_distribution import *

class Network(object):

    def __init__(self, nodes, distributions, evidences, domains):
        self.nodes = nodes
        self.distributions = distributions
        self.evidences = evidences
        self.domains = domains

    def get_domains(self):
        return self.domains

    def set_domains(self, domains):
        self.domains = domains

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes

    def get_evidences(self):
        return self.evidences

    def set_evidences(self, evidences: dict):
        self.evidences = evidences

    def set_distributions(self, distributions: dict):
        self.distributions = distributions

    def get_distributions(self):
        return self.distributions

    def get_edges(self):
        return self.edges

    def get_freq_edges(self):
        return self.freq_edges

    def get_variable_card(self):
        return self.variable_card

    def get_variable_card_by_name(self, name: str):
        return self.variable_card[name]

    def get_evidence_list_by_name(self, nodename: str):
        if self.evidences is not None:
            res = self.evidences[nodename]
            if len(res) == 0:
                return None
            else:
                return list(res)
        else:
            print('variable: evidence_dict has not defined')

    def get_evidence_card_by_name(self, nodename: str):
        evidence_list = self.get_evidence_list_by_name(nodename)
        if evidence_list is not None:
            return [self.get_variable_card_by_name(
                ev_name) for ev_name in evidence_list]

    def get_statenames(self):
        return self.statenames

    def get_state_names_by_name(self, nodename: str):
        state_name = {}
        evidence = self.evidences[nodename]
        state_name[nodename] = self.statenames[nodename]
        for evi in evidence:
            state_name[evi] = self.statenames[evi]
        return state_name

    def get_values_by_name(self, name: str):
        return self.values[name]

    def __str__(self):
        return f'------\nNetwork:\n  nodes: {[node.to_str() for node in self.nodes]}\n  distributions: {self.distributions}\n  evidences: {self.evidences}\n  domains:{self.domains}\n------\n '

    def set_values(self, values):
        self.values = values

    def set_statenames(self, statenames):
        self.statenames = statenames

    def set_edges(self, edges):
        self.edges = edges

    def set_freq_edges(self, freq_edges):
        self.freq_edges = freq_edges

    def set_variable_card(self, variable_card):
        self.variable_card = variable_card

    def get_children_dict(self):
        reverse_evidences = dict()
        for child, parents in self.evidences.items():
            # the root nodes
            if len(parents) == 0:
                parents = {'RootNodes'}
            for parent in parents:
                if parent not in reverse_evidences:
                    reverse_evidences[parent] = {child}
                else:
                    reverse_evidences[parent].add(child)
        return reverse_evidences

    def get_node_from_name(self, nodename):
        for node in self.nodes:
            if node.get_name() == nodename:
                return node