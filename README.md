# Assisting Curation of Glycosylation
This project is to use regular expression patterns for detecting useful information in PubMed abstracts. This program takes a pmid txt file as the input and output two tsv files.

## Prerequisite 

1. Source file from glygen website: 
GlyConnect: \
human: https://data.glygen.org/GLY_000329 \
mouse: https://data.glygen.org/GLY_000330 \
rat: https://data.glygen.org/GLY_000331

Unicarbkb: \
human: https://data.glygen.org/GLY_000040 \
mouse: https://data.glygen.org/GLY_000041 \
rat: https://data.glygen.org/GLY_000221

2. MongoDB database as the source for PubMed abstract (here we use the table "text" in the database "medline_current")

## How to run
In the file "assisting_curation_abstract.py", change the variable "file_input_list" to your pmid txt file(s). Then run "python assisting_curation_abstract.py".

