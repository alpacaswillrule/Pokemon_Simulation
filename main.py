import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from Pokemonclass import Pokemon
import random

statsdataframe = pd.read_csv('Pokemon.csv')
typechart = pd.read_csv('Pokemon_Type_Chart.csv')

print(np.unique(statsdataframe['Type 1']))
def initialize_simulation(NumPokemon = 15, Area = 300): #returns a list of each pokemon object, a list of coordinates aswell corresponding to list of pokemon objects
    Pokemonlst = []
    x = random.sample(range(0, Area), NumPokemon)
    y = random.sample(range(0, Area), NumPokemon)
    for i in range(NumPokemon):
        Pokemonlst.append(Pokemon(statsdataframe.iloc[0],(x[i],y[i])))
    return Pokemonlst
    
def battle(Pokemonlst, index1, index2): #hasnt been debugged yet
    stat1 = Pokemonlst[index1].getstats()
    stat2 = Pokemonlst[index2].getstats() # gets pokemon stats
    
    firstadv = typechart.loc[stat1[1]].loc[stat2[1]] #looks up type advantage in typechart, returns number from .5 to 2
    secondadv = typechart.loc[stat2[1]].loc[stat1[1]]


    stren1 = np.random.normal(loc=1,scale=.8) * stat1[3] * stat1[2] * stat1[4] * stat1[5] * stat1[7] * firstadv #calculates their strenghts, adds randomness
    stren2 = np.random.normal(loc=1,scale=.8) * stat2[3] * stat2[2] * stat2[4] * stat2[5] * stat2[7] * secondadv

    if stren1>stren2: #the battle! one of them is killed, maybe adjust in future so theres a chance that one survives
        Pokemonlst[index2].kill()
    else:
        Pokemonlst[index1].kill()


def move(Pokemonlst,Area):
    pass

def oneiter(Pokemonlst, NumPokemon, Area):
    pass

initialize_simulation()
        



