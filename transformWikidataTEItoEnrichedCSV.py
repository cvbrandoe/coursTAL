#!/usr/bin/python 
# -*- coding: utf-8 -*- 

# Author: Carmen Brando
# Creation date : 14/12/2018

# Prerequirements: an internet connection and the wikidata Python module (pip install wikidata)
# input: XML TEI file containing place mentions tagged with <placeName> and the corresponding Wikidata IRI specified by the ref attribute
# output: a CSV file in which each entry corresponds to a place, the geographic coordinates (lat, long) and the number of occurrences of the place in the text

import sys, csv, re
from wikidata.client import Client
from lxml import etree

if len(sys.argv) != 2:
	print("usage: python transform.py <TEIfile>")
	
else:
	print("Reading TEI and extracting tagged place references") 	
	tree = etree.parse(str(sys.argv[1]))
	tab = []
	uris = set()
	for p in tree.xpath(".//s:placeName", namespaces={'s': 'http://www.tei-c.org/ns/1.0'}):
		if p.attrib['ref'] != '':
			tab.append([p.attrib['ref'], p.text]);
			uris.add(p.attrib['ref'])
	print("Done")	
	#print(uris)
	
	print("Retrieving RDF data from IRIs and capturing coordinates")
	print("This may take a while..")	
	coordsByUri = {}
	namesByUri = {}
	client = Client()
	for uri in uris:
		print(uri+" - graph parsed")
		ent_id = uri.split('/')
		entity = client.get(ent_id[len(ent_id)-1], load=True)
		
		geo_prop = client.get('P625')
		if entity.attributes['claims'].get(geo_prop.id):
			coordsByUri[uri] = str(entity.attributes['claims'][geo_prop.id][0]['mainsnak']['datavalue']['value']['latitude']) + "|" + str(entity.attributes['claims'][geo_prop.id][0]['mainsnak']['datavalue']['value']['longitude'])
		else:
			coordsByUri[uri] = "-|-"
		namesByUri[uri] = entity.label
		
	print("Done")
	#print(coordsByUri)
	#print(namesByUri)
	
	print("Writing data to CSV file")
	with open("places.csv", 'w') as csvfile:
		fieldnames = ['src', 'IRI', 'placeMention', 'lat', 'long', 'placeName']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for t in tab:
			#print(t[0])
			#print(coordsByUri[t[0]])
			x,y = coordsByUri[t[0]].split("|")
			src_file = sys.argv[1].split("/")
			writer.writerow({'src' : src_file[len(src_file)-1], 'IRI': t[0], 'placeMention': t[1], 'lat': y.strip(), 'long': x.strip(), 'placeName': namesByUri[t[0]]})
			
