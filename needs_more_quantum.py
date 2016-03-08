from NotEnoughQuantum import categories, ARXIV_BASE,RANDOM_KEY
from NotEnoughQuantum.secret import key, secret, access_key, access_secret
from textblob import TextBlob

import feedparser
import json
import os
import random
import requests
import tweepy

auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(access_key,access_secret)
twitter = tweepy.API(auth)

def get_entries(cat):
    feed = feedparser.parse(ARXIV_BASE+cat)
    if feed.entries is not None and not feed.bozo:
        return feed.entries
    else:
        return None

def gen_title(entry):
    title = entry.title.split(' (')[0]
    print(title)
    t = TextBlob(title)
    phrases = [phrase for phrase in t.noun_phrases if not 'quantum' in phrase]
    print(phrases)
    title = title.title()
    for pick in phrases:
        if len(pick.split(' ')) > 2:
            new_phrase = 'quantum ' + pick
        else:
            new_phrase = ' '.join(pick.split(' ')[:-1])
            new_phrase += ' quantum ' + pick.split(' ')[-1]
        title = title.replace(pick.title(),new_phrase.title())
    print(title)
    return title

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),'entries.json'),'r') as f:
        old_entries = json.load(f)
    data = {'params': {'replacement': True, 'n': 1, 'decimalPlaces': 20,
                       'apiKey':RANDOM_KEY},
            'method': 'generateDecimalFractions', 'id': 1615, 'jsonrpc': '2.0'}
    r = requests.post('https://api.random.org/json-rpc/1/invoke',
                      data=json.dumps(data), headers={'content-type':
                                                      'application/json'})
    rand = r.json()['result']['random']['data'][0]
    cats = list(categories.keys())
    random.shuffle(cats)
    for cat in cats:
        print(cat)
        entries = get_entries(cat)
        if entries is None:
            continue
        random.shuffle(entries)
        for entry in entries:
            print('Doing one')
            new_title = gen_title(entry)
            if new_title != entry.title and len(new_title)<140:
                twitter.update_status(new_title)
                old_entries.append({'id':entry.id,'cat':cat})
                with open(os.path.join(os.path.dirname(__file__),
                                       'entries.json'),'w') as f:
                    json.dump(old_entries,f,indent=2)
                exit()
