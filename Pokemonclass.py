#import stats in main
from logging import raiseExceptions
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
        self.statlst.append(stats['Sp. Atk'])
        self.statlst.append(stats['Sp. Def'])
        self.statlst.append(stats['Speed'])
        self.statlst.append(stats['Legendary'])

        self.position = pos
        self.isAlive = True
        self.reproducecap = self.statlst[2]/10
        self.reproducecounter = 0 # their cooldown is based on hp, when counter hits their cap they can reproduce

    def kill(self):
        self.isAlive = False #need to remeber to ensure that dead pokemon are ignored in pdist calculations.
        self.position = (-1,-1) 
    
    def oneround(self): #just reduces cooldown on reproduce
        if self.isAlive == True:
            self.reproducecounter += 1
        else:
            raise Exception("dead pokemon in oneround")

    def newpos(self,pos):
        if self.isAlive == True:
            self.position = pos
        else:
            raise Exception("dead pokemon moved")

    def can_reproduce(self):  #both pokemon need to return true for it to happen
        if self.reproducecounter > self.reproducecap:
            return True
        else:
            return False
    
    def reproduce(self):
        if self.isAlive == True:
            self.reproducecounter = 0
        else:
            raise Exception("dead pokemon reproduced")

    def getstats(self):
        if self.isAlive == True:
            return self.statlst
        else:
            raise Exception("dead stats accessed")

    def getpos(self):
        if self.isAlive == True:
            return self.position
        else:
            raise Exception("dead position accessed")