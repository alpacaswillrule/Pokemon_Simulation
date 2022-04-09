import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from Pokemonclass import Pokemon

statsdataframe = pd.read_csv('Pokemon.csv')
print(statsdataframe.iloc[0])

def initialize_simulation(NumPokemon = 15): #returns a list of each pokemon object, a list of coordinates aswell corresponding to list of pokemon objects
    Pokemonlst = []
    for _ in NumPokemon:
        Pokemonlst.append(Pokemon(statsdataframe.iloc[0]))
        



