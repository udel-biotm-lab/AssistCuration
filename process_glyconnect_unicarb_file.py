from __future__ import division,print_function
import time,re,sys,os,ast,collections
import pandas as pd
import re,csv,codecs,json
from assisting_curation_abstract import read_abstract_from_mongodb, detect_glyco_info_from_abstract

def extract_pmid_and_count_unique_pair(file_input):

    output_file=file_input.split('.')[0]+'_count.csv'
    #use this set to remove the duplicates
    pair_dic={}
    pmid_set=set()
    col_title=['pmid','count','site','Predicted_as_LS_Positive']
    with open(output_file, 'w') as csvfile:
        spamwriter_o = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter_o.writerow(col_title)
        with open(file_input) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

            for row in spamreader:

                col_title=row

                break
            print(col_title)
            ind_xref_key=col_title.index('xref_key')
            ind_uniprotkb_canonical_ac=col_title.index('uniprotkb_canonical_ac')
            ind_glycosylation_site_uniprotkb=col_title.index('glycosylation_site_uniprotkb')
            ind_amino_acid=col_title.index('amino_acid')

            for row in spamreader:
                if row[ind_xref_key]!='protein_xref_pubmed' or row[ind_glycosylation_site_uniprotkb]=='':
                    continue
                pmid=row[ind_xref_key+1]
                pmid_set.add(pmid)
                pair_tuple=tuple([row[ind_uniprotkb_canonical_ac],row[ind_glycosylation_site_uniprotkb],row[ind_amino_acid]])
                amino_acid_pair=tuple([row[ind_glycosylation_site_uniprotkb],row[ind_amino_acid]])

                if pmid in pair_dic:
                    pair_dic[pmid].add(amino_acid_pair)
                else:
                    pair_dic[pmid]=set([amino_acid_pair])

        for ri in pair_dic.keys():
            res_row=['']*len(col_title)
            res_row[0]=ri
            res_row[1]=str(len(pair_dic[ri]))
            res_row[3]='Yes'
            raw_doc=read_abstract_from_mongodb('medline_current','text',ri)

            detected_sent=detect_glyco_info_from_abstract(raw_doc,ri)
            if detected_sent is None or len(detected_sent)==0:
                res_row[3]='No'

            site_list=list(pair_dic[ri])
            site_list=[si[1]+si[0] for si in site_list]
            if len(pair_dic[ri])<=10:
                res_row[2]=','.join(site_list)

            spamwriter_o.writerow(res_row)

    pmid_file=file_input.split('.')[0]+'_pmid.txt'
    with codecs.open(pmid_file, 'w', encoding='utf8') as f:
        for pi in pmid_set:
            f.write(pi)
            f.write('\n')

def simplify_file(file_input):

    output_file=file_input.split('.')[0]+'_simplified.csv'

    uniprot_kb_ac_to_id_file='uniprot_kb_ac_to_id.json'
    with open(uniprot_kb_ac_to_id_file) as bjfile:
        uniprot_kb_ac_to_id_dic=json.load(bjfile)

    with open(output_file, 'w') as csvfile:
        spamwriter_o = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter_o.writerow(['pmid','amino acid','site position','uniprotkb id','protein name'])
        with open(file_input) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')

            for row in spamreader:

                col_title=row

                break
            print(col_title)
            ind_xref_key=col_title.index('xref_key')
            ind_uniprotkb_canonical_ac=col_title.index('uniprotkb_canonical_ac')
            ind_glycosylation_site_uniprotkb=col_title.index('glycosylation_site_uniprotkb')
            ind_amino_acid=col_title.index('amino_acid')
            ind_xref_id=col_title.index('xref_id')


            for row in spamreader:
                if row[ind_xref_key]!='protein_xref_pubmed' or row[ind_glycosylation_site_uniprotkb]=='':
                    continue
                uniprot_kb_ac=row[ind_uniprotkb_canonical_ac].split('-')[0]
                protein_name=''
                if uniprot_kb_ac in uniprot_kb_ac_to_id_dic:
                    protein_name=uniprot_kb_ac_to_id_dic[uniprot_kb_ac]
                    protein_name=protein_name.split('_')[0]
                new_row=[row[ind_xref_id],\
                         row[ind_amino_acid],\
                         row[ind_glycosylation_site_uniprotkb],\
                         row[ind_uniprotkb_canonical_ac],\
                         protein_name]
                spamwriter_o.writerow(new_row)


def generate_pmid_file_for_glyconnect_unicarb(glyconnect_file, unicarb_file):
    glyconnect_set=set()
    for fi in glyconnect_file:
        with codecs.open(fi, encoding='utf8') as f:
            for line in f:
                line=line.strip()
                glyconnect_set.add(line)
    with codecs.open('glyconnect_new.txt', 'w', encoding='utf8') as f:
        for pi in glyconnect_set:
            f.write(pi)
            f.write('\n')

    unicarb_set=set()
    for fi in unicarb_file:
        with codecs.open(fi, encoding='utf8') as f:
            for line in f:
                line=line.strip()
                unicarb_set.add(line)
    with codecs.open('unicarb_new.txt', 'w', encoding='utf8') as f:
        for pi in unicarb_set:
            f.write(pi)
            f.write('\n')

if __name__ == '__main__':
    #test

    file_input_list=['human_proteoform_glycosylation_sites_glyconnect.csv',\
                     'human_proteoform_glycosylation_sites_unicarbkb.csv',\
                     'mouse_proteoform_glycosylation_sites_glyconnect.csv',\
                     'mouse_proteoform_glycosylation_sites_unicarbkb.csv',\
                     'rat_proteoform_glycosylation_sites_glyconnect.csv',\
                     'rat_proteoform_glycosylation_sites_unicarbkb.csv']
    for fi in file_input_list:
        extract_pmid_and_count_unique_pair(fi)
        #simplify_file(fi)

    '''
    glyconnect_file=['human_proteoform_glycosylation_sites_glyconnect_pmid.txt', \
                     'mouse_proteoform_glycosylation_sites_glyconnect_pmid.txt', \
                     'rat_proteoform_glycosylation_sites_glyconnect_pmid.txt']

    unicarb_file=['human_proteoform_glycosylation_sites_unicarbkb_pmid.txt', \
                      'mouse_proteoform_glycosylation_sites_unicarbkb_pmid.txt', \
                     'rat_proteoform_glycosylation_sites_unicarbkb_pmid.txt']

    generate_pmid_file_for_glyconnect_unicarb(glyconnect_file, unicarb_file)
    '''