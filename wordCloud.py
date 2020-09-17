import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import numpy as np
import PIL.Image
import re
swearings = re.compile(r'kurw|huj|pierd|jeb')

df = pd.read_csv('all.csv', usecolslist=['content'])

def get_stopwords():
    with open('polish', 'r', encoding="utf-8") as f:
        return f.read().split('\n')
STOPWORDS = get_stopwords()

with open('text.txt', 'r', encoding="utf-8") as f:
    c = Counter(word for line in f
                for word in str(line[:-1]).lower().split(' ')
                if len(word)>1
                #and not swearings.search(word)
                # and word not in STOPWORDS)
    for i in c.most_common(10):
        print(i)

mask = np.array(PIL.Image.open("messLogo.png"))
wordcloud1 = WordCloud(background_color="white",
                       mask=mask,
                       contour_width=1,
                       contour_color='steelblue').generate_from_frequencies(c)
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis("off")
plt.show()