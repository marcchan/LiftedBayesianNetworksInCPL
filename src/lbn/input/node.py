class Node(object):

    def __init__(self, name: str, para: dict):
        self.name = name
        self.para = para

    def get_name(self):
        return self.name

    # def get_type(self):
        # return self.type

    def get_domain(self):
        return self.domain

    def get_para(self):
        return self.para

    def set_name(self, name):
        self.name = name

    # def set_type(self, type):
    #     self.type = type

    def set_domain(self, domain):
        self.domain = domain

    def set_para(self,para:dict):
        self.para = para

    def __str__(self):
        if self.domain is not None:
            return f'nodename: {self.get_name()},\n Para: {self.get_para()}\n'
        else:
            return f'nodename: {self.get_name()},\n Para: {self.get_para()},\n Domain:{self.get_domain()} '

    def get_variable_card(self) -> int:
        """
        :return: avaiable variable
        Example:
            * Drives: 4, res = 5 -> {0,1,2,3,4}
            * Fined  res = 2 -> {True, False}
            * Friend(X,Y) x,y from Student = 10
                    res -> {??}
            * Teach(T,S): T = 2, S =3 res-> {??}
        """
        if self.get_domain() == {}: return int(2)
        else:
            values = list(self.get_domain().values())
            if len(values) == 1:
                return int(values[0]) + 1
            else:
                print(f'TODO with case of multi parameter in function get_variable_card in Object Node')
                return 0
            # return reduce((lambda x, y: x * y), values)
