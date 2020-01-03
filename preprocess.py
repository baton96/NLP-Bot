#SymSpell
#from symspellpy import SymSpell
from json import load
from re import sub, findall

translation = {281: 'e', 243: 'o', 261: 'a', 347: 's', 322: 'l', 380: 'z', 378: 'z', 263: 'c', 324: 'n'}
person = 'Bartek Paulewicz'

#SymSpell
#sym_spell = SymSpell()
#sym_spell.load_dictionary('50k.txt', 0, 1, encoding='utf-8')
#wordSeg = sym_spell.word_segmentation

with open("marcin.json", "r", encoding='latin1') as raw, open("both.txt", "w", encoding='utf-8') as out:
    obj = load(raw)
    prev = obj['messages'][-1]['sender_name']
    for i, msg in enumerate(reversed(obj['messages'])):
        #if i % 100 == 0: print(i)
        content = msg\
            .get('content', '')\
            .encode('latin1')\
            .decode('utf8')\
            .lower()
        if (not content.startswith('http')) and ('wysłał' not in content) and (not content.endswith('kolory czatu.')):
            content = sub('[^a-z ]', ' ', content.translate(translation)).strip()
            if content:
                repeated = findall(r'([eyuoam])\1+', content)
                if repeated:
                    for group in repeated:
                        content = sub(f'{group}+', group, content)
                #SymSpell
                #content = ' '.join([word if word in sym_spell.words else wordSeg(word).corrected_string for word in content.split()])
                sender = msg['sender_name']
                if (sender != person and prev == person) or (sender == person and prev != person):
                    out.write('\n')
                    prev = sender
                out.write(content+' ')
                #print(msg.get('content', ''), '|', content)