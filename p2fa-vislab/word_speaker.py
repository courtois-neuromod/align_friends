import os
from pocketsphinx import Pocketsphinx, AudioFile, get_model_path, get_data_path

temp = {}
with open(os.path.join(get_model_path(), 'cmudict-en-us.dict')) as f:
    for line in f:
        key, *value = line.split()
        temp[key] = " ".join(value)

def get_pronunciation(word):
    try:
        return temp[word]
    except KeyError:
        return ""
