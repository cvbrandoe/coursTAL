import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

sentences = u"once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversation?'. So she was considering in her own mind."

ps = PorterStemmer()
stemmed_words=[]
punctuations="?:!.,;’"
sentence_words = word_tokenize(sentences)
for word in sentence_words:
    if word in punctuations:
        sentence_words.remove(word)

for w in sentence_words:
    stemmed_words.append(ps.stem(w))

print("Filtered Sentence:", sentences)
print("Stemmed Sentence:", stemmed_words)

