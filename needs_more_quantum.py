from NotEnoughQuantum import categories,ARXIV_BASE,RANDOM_KEY
from textblob import TextBlob

import feedparser
import json
import os
import random
import requests

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),'entries.json'),'r') as f:
        entries = json.load(f)
    data = {'params': {'replacement': True, 'n': 1, 'decimalPlaces': 20,
                       'apiKey':RANDOM_KEY},
            'method': 'generateDecimalFractions', 'id': 1615, 'jsonrpc': '2.0'}
    r = requests.post('https://api.random.org/json-rpc/1/invoke',
                      data=json.dumps(data), headers={'content-type':
                                                      'application/json'})
    rand = r.json()['result']['random']['data'][0]
    print(rand)
    random.seed(rand)
    cat = random.choice(list(categories.keys()))
    feed = feedparser.parse(ARXIV_BASE+cat)
    if feed.entries is not None:
        entry = random.choice(feed.entries)
        entries.append({'cat':cat,'id':entry.id})
        with open(os.path.join(os.path.dirname(__file__),'entries.json'),'w') as f:
            json.dump(entries,f)
        title = entry.title.split(' (')[0]
        t = TextBlob(title)
        phrases = [phrase for phrase in t.noun_phrases if not 'quantum' in phrase]
        title = title.title()
        for pick in phrases:
            new = ' '.join(pick.split(' ')[:-1])
            new += ' quantum ' + pick.split(' ')[-1]
            title = title.replace(pick.title(),new.title())
        print(title)
