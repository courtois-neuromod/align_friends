import os
import glob
import json
from tqdm import tqdm

home = '/'.join(os.getcwd().split("/")[:-1])
s = 2 #season
tmp = glob.glob(home + f"/processed_subtitles/s{s}/*")


for i in tqdm(range(1, 5)):
    try:
        stri = "{:02d}".format(i)
        awav = f"../audios/s{s}/friends_s{s}e{stri}a.wav"
        bwav = f"../audios/s{s}/friends_s{s}e{stri}b.wav"
        ajson = f"../processed_subtitles/s{s}/s0{s}e{stri}a.json"
        bjson = f"../processed_subtitles/s{s}/s0{s}e{stri}b.json"
        aoutput = f"../aligned_output/aligned_s0{s}e{stri}a.json"
        boutput = f"../aligned_output/aligned_s0{s}e{stri}b.json"
        os.system(f"python align.py {awav} {ajson} {aoutput}")
        os.system(f"python align.py {bwav} {bjson} {boutput}")
    except:
        continue
