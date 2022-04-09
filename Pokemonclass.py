#import stats in main
import numpy as np
import pandas as pd


class Pokemon(object):
    def __init__(self, stats,pos): #initalizing a pokemon, stores stats in statlst. 

        self.statlst = []
        self.statlst.append(stats['Name'])
        self.statlst.append(stats['Type 1'])
        self.statlst.append(stats['HP'])
        self.statlst.append(stats['Attack'])
        self.statlst.append(stats['Defense'])
        self.statlst.append(stats['Sp.Atk'])
        self.statlst.append(stats['Sp.Def'])
        self.statlst.append(stats['Speed'])
        self.statlst.append(stats['Legendary'])

        self.position = pos
        self.isAlive = True

    
    def getstats(self):
        return self.statlst

    def getpos(self):
        return self.position