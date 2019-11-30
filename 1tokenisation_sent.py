import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

sentences = u"once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversation?'. So she was considering in her own mind."
sent_tokenize_list = sent_tokenize(sentences)
print(sent_tokenize_list)

sentence_words = word_tokenize(sentences)
print(sentence_words)
