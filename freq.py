#Loading NLTK
import nltk
from nltk import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

text="""Hello Mr. Smith, how are you doing today? The weather is great, and city is awesome.
The sky is pinkish-blue. You shouldn't eat cardboard"""

with open('user.txt', 'r') as f:
    data = f.read()

from nltk.tokenize import word_tokenize
tokenized_word=word_tokenize(text)  

from nltk.probability import FreqDist
fdist = FreqDist(tokenized_word)

stop_words=set(stopwords.words("english"))
print(stop_words)

filtered_sent=[]
for w in tokenized_word:
    if w not in stop_words:
        filtered_sent.append(w)
print("Tokenized Sentence:",tokenized_word)
print("Filterd Sentence:",filtered_sent)


#print(fdist.most_common(25))