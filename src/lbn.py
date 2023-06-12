# coding: utf-8
# @author Xingjian Chen
# @date 2023/5/6
# @file lbn.py
from pgmpy.models import BayesianNetwork




class LBN(BayesianNetwork):
    def __init__(self, ebunch=None, latents=set()):
        super(LBN, self).__init__(ebunch=ebunch, latents=latents)
        # self.cpds = []
        # self.cardinalities = defaultdict(int)

