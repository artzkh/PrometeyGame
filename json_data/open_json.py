import os
from json import load

path_to_pictures_json = f'{os.path.dirname(os.path.abspath(__file__))}/pict.json'

with open(path_to_pictures_json, 'r') as file:
    pictures = load(file)
