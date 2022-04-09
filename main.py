import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from Pokemonclass import Pokemon
import random

statsdataframe = pd.read_csv('Pokemon.csv')

def initialize_simulation(NumPokemon = 15, Area = 300): #returns a list of each pokemon object, a list of coordinates aswell corresponding to list of pokemon objects
    Pokemonlst = []
    x = random.sample(range(0, Area), NumPokemon)
    y = random.sample(range(0, Area), NumPokemon)
    for i in NumPokemon:
        Pokemonlst.append(Pokemon(statsdataframe.iloc[0],(x[i],y[i])))
    


        



