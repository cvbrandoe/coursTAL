import spacy

nlp = spacy.load("fr_core_news_sm")
#nlp = spacy.load("fr_core_news_md")
with open ("balzac.txt", "r") as myfile:
    data=myfile.read()
doc = nlp(data)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
