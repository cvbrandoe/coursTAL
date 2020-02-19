# -*- coding: utf-8 -*-

import pandas as pd
import glob, os

data_folder="../eltec-fra-conll"

os.chdir(data_folder)
li = []
for f in glob.glob("*.tsv"):
	print(f)
	df = pd.read_csv(f,sep="\t",encoding="utf-8",engine="python",error_bad_lines=False)
	li.append(df)
df_data = pd.concat(li, axis=0, ignore_index=True)

print(df_data)
# Have a look at the dataset
#print(df_data.head(n=2000))

# Have a look TAG cat
print(df_data.Tag.unique())

# Analyse the Tag distribution
print(df_data.Tag.value_counts())