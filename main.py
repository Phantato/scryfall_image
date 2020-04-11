
import json
import os
import urllib.request
import time
# import eventlet
from tqdm import tqdm
import requests


import os.path as op
import os
from sys import stdout
 
 
def downloadfile(url, filename):
    if os.path.exists(filename):
        return
        # r = urllib.request.urlopen(url)
        # fw.write(r.read())
    stdout.write('\r' + url)
        # urlResponse = urllib.request.urlopen(url)
        # url = urlResponse.geturl()
    with requests.get(url, stream=True) as r:
        with open(filename, "wb") as fw:
            filesize = r.headers["Content-Length"]
            chunk_size = 1024 * 64
            times = int(filesize) // chunk_size + 1
            show = 1 / times
            show2 = 1 / times
            start = 0
            stdout.write('\r' + filename.split('/')[-1] + ': 0.00% |')
            for chunk in r.iter_content(chunk_size):
                fw.write(chunk)
                if start <= times:
                    stdout.write('\r' + filename.split('/')[-1] + f": {show:.2%} |")
                    start += 1
                    show += show2

def downloadImage(set, dirPath):
    apiURL = 'https://api.scryfall.com/cards/'
    par = '?format=image&version=png'
    it = tqdm(set['cards'])
    for card in it:
        if card['number'][-1] == 'a':
            card['number'] = card['number'][:-1]
        try:
            cn = int(card['number'])
        except:
            continue
        if (set['type'] != 'commander' and cn > int(set['baseSetSize'])):
            continue
        cardURL = apiURL + card['scryfallId'] + par
        # cardURL = apiURL + card['scryfallId']
        if card['layout'] == 'transform' and card['side'] == 'b':
            cardURL += '&face=back'

        succ = False
        while not succ:
            filePath = dirPath + card['name'].replace(':', '').replace('"', '') + '.png'
            # with eventlet.Timeout(time_limit,False):
            downloadfile(cardURL, filePath)
            succ = True
            if not succ:
                os.remove(filePath)
        it.set_description(card['name'])



jsonPath = "./jsons/"
picPath = "D:/CockatricePortable/data/pics/downloadedPics/"
setName = "SetList.json"
available = ('core', 'expansion', 'commander', 'draft_innovation') #, 'from_the_vault', 'master')
# eventlet.monkey_patch()
# time_limit = 60

with open(jsonPath + setName, encoding="UTF-8") as f:
    sets = json.load(f)

with open('./cache/finish.cfg', 'r') as f:
    try:
        finished = json.load(f)
    except:
        finished = list()
with open('./cache/finish.cfg', 'w') as f:
    json.dump(finished, f)
    f.seek(0)
    for set_ in sets:
        if set_['code'] == 'CON':
            set_['code'] = 'CON_'
        if set_['type'] in available and not (set_['code'] in finished):
            print(set_['code'])
            setPath = picPath + set_['code'] + '/'
            if (not os.path.exists(setPath)):
                os.makedirs(setPath)
            setJsonPath = jsonPath + set_['code'] + '.json'
            with open(setJsonPath, encoding='UTF-8') as setJson:
                j = json.load(setJson)
                downloadImage(j, setPath)
                with open(setPath + 'stat.txt', 'w') as temp:
                    temp.write('Base Size: ' + str(j['baseSetSize']) + '\nTotal Size: ' + str(j['totalSetSize']))
            finished.append(set_['code'])
            json.dump(finished, f)
            f.seek(0)
            f.flush()