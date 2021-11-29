class Node(object):

    evidences: set = set()
    distributions: list = {}

    def __init__(self, name: str, type: str, domain=None):
        self.name = name
        self.type = type
        self.domain = domain

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_domain(self):
        return self.domain

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.type = type

    def set_domain(self, domain):
        self.domain = domain

    def get_distributions(self):
        return self.distributions

    def set_distributions(self, distributions: dict):
        self.distributions = distributions

    def get_evidences(self):
        return self.evidences

    def set_evidences(self, evidences: set):
        self.evidences = evidences

    def __str__(self):
        return f'nodename: {self.get_name()},\nDomain: {self.get_domain()},\nType: {self.get_type()},\n' \
               f'Distributions: {self.get_distributions()},\nevidences: {self.get_evidences()}\n\n'

    def get_variable_card(self):
        if self.type == 'bool':
            return int(2)
        elif self.type == 'int':
            return int(self.domain + 1)
        # TODO any other cases
