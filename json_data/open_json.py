import os
from json import load

path_to_pictures_json = f'{os.path.dirname(os.path.abspath(__file__))}/pict.json'
path_to_users_json = f'{os.path.dirname(os.path.abspath(__file__))}/users.json'

with open(path_to_pictures_json, 'r') as file:
    pictures = load(file)

with open(path_to_users_json, 'r') as file:
    users = load(file)
