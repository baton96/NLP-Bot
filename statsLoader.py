from symspellpy import SymSpell
from re import sub, findall
from os import listdir
from json import load
import pandas as pd
from datetime import datetime

#translation = {'ę': 'e', 'ó': 'o', 'ą': 'a', 'ś': 's', 'ł': 'l', 'ż': 'z', 'ź': 'z', 'ć': 'c', 'ń': 'n'}
translation = {281: 'e', 243: 'o', 261: 'a', 347: 's', 322: 'l', 380: 'z', 378: 'z', 263: 'c', 324: 'n'}
prev = ''

symSpell = SymSpell()
#symSpell.load_dictionary('full.txt', 0, 1, encoding='utf-8')
symSpellWords = symSpell.words
wordSeg = symSpell.word_segmentation

data = []
for chatName in listdir('messages'):
#for chatName in ['EmiliaRose_tJG_fEH10A']:
    if chatName.startswith('uzytkownikfacebooka_'):
        continue
    print(chatName)
    for i in range(1, 4):
        try:
            with open(f'messages/{chatName}/message_{i}.json', 'r') as raw:
                obj = load(raw)
            title = obj.get('title', '').encode('latin1').decode('utf8')
            isGroup = obj['thread_type'] == 'RegularGroup'
            for msg in obj['messages']:
                timestamp = datetime.fromtimestamp(msg.get('timestamp_ms', 0) // 1000)
                sender = msg.get('sender_name', None) == 'Bartek Paulewicz'
                type = msg.get('type', None) == 'Generic'
                sticker = msg.get('sticker', None) is not None
                photos = msg.get('photos', None) is not None
                videos = msg.get('videos', None) is not None

                content = msg.get('content', '')
                content = content.encode('latin1').decode('utf8')
                content = content.lower()
                content = content.translate(translation)
                content = sub(r'[^a-z ]', ' ', content)
                content = sub(r'\s+', ' ', content)
                content = content.strip()

                data.append([isGroup, title, timestamp, content, sender, type, sticker, photos, videos])
        except:
            break

colNames = [
    'isGroup',
    'title',
    'timestamp',
    'content',
    'sender',
    'type',
    'sticker',
    'photos',
    'videos'
]
df = pd.DataFrame(data, columns=colNames)
df.set_index('title', inplace=True)
df.to_csv('all.csv')