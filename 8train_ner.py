#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
Last tested with: v2.1.0
"""
from __future__ import unicode_literals, print_function

import plac, glob, codecs, ast
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# training data
TRAIN_DATA = []

@plac.annotations(
	model=("Model name. Defaults to blank 'fr' model.", "option", "m", str),
	output_dir=("Optional output directory", "option", "o", Path),
	n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=100):
	"""Load the model, set up the pipeline and train the entity recognizer."""
	if model is not None:
		nlp = spacy.load(model)  # load existing spaCy model
		print("Loaded model '%s'" % model)
	else:
		nlp = spacy.blank("fr")  # create blank Language class
		print("Created blank 'fr' model")

	# create the built-in pipeline components and add them to the pipeline
	# nlp.create_pipe works for built-ins that are registered with spaCy
	if "ner" not in nlp.pipe_names:
		ner = nlp.create_pipe("ner")
		nlp.add_pipe(ner, last=True)
	# otherwise, get it so we can add labels
	else:
		ner = nlp.get_pipe("ner")

	# Load annotations into model
	for x in range(10):
		train_files = glob.glob("../ZolaLVP_1tier_AnnSents/group"+str(x)+"/*.txt")
		for j in train_files:
		#print("reading "+j)
			with codecs.open(j, 'r+', encoding='utf8') as train_f:
				train_l = ast.literal_eval('[{0}]'.format(train_f.read()))
				TRAIN_DATA.extend(train_l[0]) 
	print("nb of sentences in the training dataset: "+str(len(TRAIN_DATA)))
	
	# add labels
	for _, annotations in TRAIN_DATA:
		for ent in annotations.get("entities"):
			ner.add_label(ent[2])

	# get names of other pipes to disable them during training
	other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
	with nlp.disable_pipes(*other_pipes):  # only train NER
		# reset and initialize the weights randomly – but only if we're
		# training a new model
		if model is None:
			nlp.begin_training()
		for itn in range(n_iter):
			random.shuffle(TRAIN_DATA)
			losses = {}
			# batch up the examples using spaCy's minibatch
			batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
			for batch in batches:
				texts, annotations = zip(*batch)
				nlp.update(texts,  # batch of texts
					annotations,  # batch of annotations
					drop=0.5,  # dropout - make it harder to memorise data
					losses=losses,
				)
			print("Losses", losses)

	# test the trained model
	for text, _ in TRAIN_DATA:
		doc = nlp(text)
		#print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
		#print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

	# save model to output directory
	if output_dir is not None:
		output_dir = Path(output_dir)
		if not output_dir.exists():
			output_dir.mkdir()
		nlp.to_disk(output_dir)
		#print("Saved model to", output_dir)
		
		# test the saved model
		print("Loading model from", output_dir)
		nlp2 = spacy.load(output_dir)
		for text, _ in TRAIN_DATA:
			doc = nlp2(text)
			#print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
			#print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
			
		print("annotate new text with the saved model")
		print("Loading model from", output_dir)
		nlp2 = spacy.load(output_dir)
		fnew = open("../le-ventre-de-paris_1-3.txt")
		lines_fnew = fnew.read()
		doc_new = nlp2(lines_fnew)
		print("Entities found in le-ventre-de-paris_1-3.txt")
		for ent in doc_new.ents:
			print(ent.text, ent.start_char, ent.end_char, ent.label_)
		
if __name__ == "__main__":
	plac.call(main)
