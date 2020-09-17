#from symspellpy import SymSpell
from re import sub, findall
from os import listdir
from json import load

#translation = {'ę': 'e', 'ó': 'o', 'ą': 'a', 'ś': 's', 'ł': 'l', 'ż': 'z', 'ź': 'z', 'ć': 'c', 'ń': 'n'}
translation = {281: 'e', 243: 'o', 261: 'a', 347: 's', 322: 'l', 380: 'z', 378: 'z', 263: 'c', 324: 'n'}
prev = ''

#symSpell = SymSpell()
#symSpell.load_dictionary('full.txt', 0, 1, encoding='utf-8')
#symSpellWords = symSpell.words
#wordSeg = symSpell.word_segmentation

for chatName in listdir('messages'):
#for chatName in ['EmiliaRose_tJG_fEH10A']:
    if chatName.startswith('uzytkownikfacebooka_'):
        continue
    with open(f'messages/{chatName}/message_1.json', 'r') as raw:
        obj = load(raw)
    if obj['thread_type']=='RegularGroup' or len(obj['participants'])!=2 :
        continue
    if len(obj['messages'])<20:
        continue

    print(chatName)
    print(len(obj['messages']))

    out = open(f'clean/{chatName}', 'w')
    for i, msg in enumerate(reversed(obj['messages'])):
        #if i%1000==0:
        #    print(i)
        #if msg['sender_name'] != 'Bartek Paulewicz':
        #    continue
        if msg['type'] != 'Generic':
            continue
        content = msg.get('content', '')
        if not content:
            continue
        if content.startswith('http'):
            continue
        content = content.encode('latin1').decode('utf8')
        content = content.lower()
        content = content.translate(translation)
        content = sub(r'[^a-z ]', ' ', content)
        content = sub(r'\s+', ' ', content)
        content = content.strip()
        if not content:
            continue
        for group in findall(r'([^in])\1', content):
            content = sub(f'{group}+', group, content)

        #content = ' '.join(
        #    [word if word in symSpellWords else wordSeg(word).corrected_string for word in content.split()])
        #content = wordSeg(content).corrected_string
        '''
        for word in content.split():
            if word not in symSpellWords:
                unknown[word] += 1
        '''
        sender = sub(r'[^a-zA-Z ]', '', msg['sender_name'])
        if sender != prev:
            out.write(f'\n{sender}:')
            prev = sender
        out.write(content + ' ')
    out.close()