import nltk
from nltk.text import Text
from nltk.corpus import gutenberg

nltk.download('gutenberg')
print(gutenberg.fileids())
alice = Text(gutenberg.words('carroll-alice.txt'))
#print(alice)
alice.concordance("Alice")
print(alice.concordance("Alice", lines=100))
