import nltk
from nltk.tokenize import word_tokenize

sentences = u"once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversation?'. So she was considering in her own mind."

sentence_words = word_tokenize(sentences)
print(nltk.pos_tag(sentence_words))
