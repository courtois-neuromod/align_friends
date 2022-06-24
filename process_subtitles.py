import os, sys, re
from datetime import datetime

def wds(string, ):
    res = re.sub(r'[^\w\s]', '', string)
    return set(res.lower().split(" "))



import glob
import string

times = {1:"00:12:23",
         2:"00:11:43",
         3: 17068,
         4: 16834}



ending = "a"
season = 2
for file in glob.glob(os.getcwd() + f"/subtitles/friends-season-{season}/*"):
    print(file)
    json_doc = "[\n"
    with open(file, encoding='ISO-8859-1') as f:
        episode = int(file.split('x')[1].split('-')[0])
        data = f.read().replace("\ufeff", '').replace("...", '').replace(". . .", '')

        if data[0] == "{":
            # SUB FILE CASE
            regex =    re.compile(r'.*\n', re.MULTILINE)
            re_time =  re.compile(r'(?<={)[0-9]*(?=})')
            re_word =  re.compile(r'(?<=[}|])[^|}{]*(?=[|\n])')
            for match in re.findall(regex, data):
                info = match
                time = int(re.findall(re_time, info)[0])
                words = " ".join(list(re.findall(re_word, info)))
                ref = times[episode]
                if (ending == "a" and time >= ref):
                    break
                elif (ending == "b" and time < ref):
                    continue
                if "Sub" in words:
                    continue
                words = words.replace('"', "")
                json_doc += "\t{\n\t\t\"speaker\": \"Narrator\", \n\t\t\"line\": \"" + words + "\"\n\t},\n"
                
        else:
            # SRT FILE CASE
            regex = re.compile(r'\d+\n.*\n.*\n.*\n', re.MULTILINE)
            #regex = re.compile(r'.*\n.*\n\n', re.MULTILINE)
            re_anar =  re.compile(r'(?<=[A-Z]:)[^:]*')
            re_bnar =  re.compile(r'(?<=[:\-]).*(?= [A-Z][A-Z])')
            re_brak =  re.compile(r'\[.*\]')
            for match in re.findall(regex, data):
                info = match.split("\n")
                #print(info)
                time = info[1].split(" ")[0].split(",")[0]
                #time = info[0].split(".")[0]
                #time = info[0].split(",")[0]
                time_obj = datetime.strptime(time, "%H:%M:%S")
                ref_obj = datetime.strptime(times[int(episode)], "%H:%M:%S")
                if (ending == "a" and time_obj > ref_obj):
                    break
                elif (ending == "b" and time_obj < ref_obj):
                    continue
                words = " ".join(info[2:])
                words = words.replace('"', "")
                
                words = words.replace('[br]', " ")
                characters = string.punctuation.replace("`", '').replace("'", "")
                if "[" in words:
                    words = re.sub(re_brak, '', words)
                    if re.sub(r' *', '', words) == "":
                        continue
                if re.findall(re_anar, words) != []:
                    try:
                        before = re.search(re_bnar, words).group()
                        before = before.translate(str.maketrans('','', characters))
                        json_doc += "\t{\n\t\t\"speaker\": \"Narrator\", \n\t\t\"line\": \"" + before + "\"\n\t},\n"
                    except AttributeError:
                        pass
                    after = re.findall(re_anar, words)[-1]
                    after = after.translate(str.maketrans('', '', characters))
                    json_doc += "\t{\n\t\t\"speaker\": \"Narrator\", \n\t\t\"line\": \"" + after + "\"\n\t},\n"
                else:
                    if words == "" or words == " ":
                        continue
                    words = words.translate(str.maketrans('', '', characters))
                    json_doc += "\t{\n\t\t\"speaker\": \"Narrator\", \n\t\t\"line\": \"" + words + "\"\n\t},\n"
    json_doc = json_doc[:-2] + "\n]"
    name = f"s0{season}e{episode:02d}{ending}"
    f = open(f"processed_subtitles/s{season}/{name}.json", "w")
    f.write(json_doc)
    f.close()
