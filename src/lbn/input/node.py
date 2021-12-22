class Node(object):

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

    def __str__(self):
        return f'nodename: {self.get_name()},\nDomain: {self.get_domain()},\nType: {self.get_type()}\n'

    def get_variable_card(self):
        if self.type == 'bool':
            return int(2)
        elif self.type == 'int':
            return int(self.domain + 1)
        # TODO any other cases

    # def set_variable_list(self):
    #     if self.type == 'bool':
    #         self.variable_list = [True, False]
    #     elif self.type == 'int':
    #         self.variable_list = list(range(self.domain+1))
    #     # TODO any other type
    #
    # def get_variable_list(self):
    #     return self.variable_list
    #
    # def get_variable_card(self):
    #     return len(self.variable_list)
    #     # TODO any other cases
