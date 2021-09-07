# Assisting Curation of Glycosylation

This project includes three modules: 

## Module 1
This module is to use regular expression patterns for detecting useful information in PubMed abstracts. This module takes a pmid txt file as the input and output two tsv files. In this module, we can detect glycosylation information on large-scale abstract. Currently, the pmid list is from this query "(human or mouse or rat) AND glycosylation AND (glycoprotein OR glycopeptide OR glycosite OR site)".

### Prerequisite 

This module needs MongoDB database as the source for PubMed abstract (here we use the table "text" in the database "medline_current")

### How to run
In the file "assisting_curation_abstract.py", change the variable "file_input_list" to your pmid txt file(s). Then run "python assisting_curation_abstract.py".


## Module 2

In this module, we count the site number in the full-length article and use the count number as a indicator for the usefulness of the pmid/article. 

### Prerequisite 

Source file from glygen website: 

GlyConnect: \
human: https://data.glygen.org/GLY_000329 \
mouse: https://data.glygen.org/GLY_000330 \
rat: https://data.glygen.org/GLY_000331

Unicarbkb: \
human: https://data.glygen.org/GLY_000040 \
mouse: https://data.glygen.org/GLY_000041 \
rat: https://data.glygen.org/GLY_000221

### How to run

Run "python process_glyconnect_unicarb_file.py" and the result files will be generated automatically with the name of "input_file_name"+"_count.csv".

## Module 3
This module is to use regular expression patterns for detecting glycosylation informtaion in the full-length articles. This module takes a JSON file (from Julie) as the input and output txt files that contain the sentences with glycosylation information.

### How to run
Step 1: In the file "read_full_length_json_result_discussion.py", change the variable "file_input_list" to your pmid txt file(s). Then run "python read_full_length_json_result_discussion.py". This script will generate a processed JSON file for next step.

Step 2: In the file "detection_supplementary.py", change the input JSON file. Then run "python detection_supplementary.py". This script will generate a set of txt file that contains the sentences with glycosylation information.

