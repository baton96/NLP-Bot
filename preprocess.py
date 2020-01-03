from json import load
from re import sub

translation = {281: 'e', 243: 'o', 261: 'a', 347: 's', 322: 'l', 380: 'z', 378: 'z', 263: 'c', 324: 'n'}
person = 'Bartek Paulewicz'

#sym_spell = SymSpell()
#sym_spell.load_dictionary('pl_50k.txt', 0, 1, encoding='utf-8')
#wordSeg = sym_spell.word_segmentation

with open("marcin.json", "r", encoding='latin1') as raw, open("both.txt", "w", encoding='utf-8') as out:
    obj = load(raw)
    prev = obj['messages'][-1]['sender_name']
    for i, msg in enumerate(reversed(obj['messages'])):
        #if i % 100 == 0: print(i)
        #print(#wordSeg(
        content = sub('\s+', ' ',
            sub('[^a-z \?]', ' ',
                sub('\s*\?+\s*', " ? ",
                    msg
                            .get('content', '')
                            .encode('latin1')
                            .decode('utf8')
                            .lower()
                            .translate(translation)
                            .strip()
                )
            )+' '
        )
        # )
        if (
                'wyslal' not in content
        ) and (
                not content.startswith('http')
        ) and (
                len(content) > 1
        ):
            sender = msg['sender_name']
            if (sender != person and prev == person) or (sender == person and prev != person):
                out.write('\n')
                prev = sender
            out.write(content)