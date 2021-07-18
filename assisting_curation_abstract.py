from __future__ import division, print_function
import time, re, sys, os, ast,csv
import pandas as pd
import pymongo
from pymongo import MongoClient
import random, operator
from collections import OrderedDict
from bson.son import SON
from bson.codec_options import CodecOptions

def read_abstract_from_mongodb(dbF,colF,pmid):
    # --- create database instances---
    # Environment variables
    mongodb_host = os.environ.get("MONGODB_HOST", "0.0.0.0")  # change to biotm2.cis.udel.edu before dockerizing
    mongodb_port = os.environ.get("MONGODB_PORT", "27017")
    db_name_from = os.environ.get("DBNAME_FROM", dbF)  # change database name for your own dbName


    fromCollectionName = os.environ.get("COLLECTION_FROM", colF)

    # Database URI
    MONGODB_URI = 'mongodb://' + mongodb_host + ':' + mongodb_port + '/'

    # Database object
    client = MongoClient(MONGODB_URI)
    opts = CodecOptions(document_class=SON)

    # Database
    dbNameFrom = client[db_name_from]  # medline

    # Collection
    fromDBCollection = dbNameFrom[fromCollectionName].with_options(codec_options=opts)

    raw_doc = fromDBCollection.find_one({"docId":str(pmid)})


    return raw_doc


def detect_glyco_info_from_abstract(raw_doc,pmid):
    if not raw_doc:
        return None

    glyco_pattern_1='(^|\s)(\d{2,}|\d+[,\d]+\d+)\s(?!(kDa|Da|pmol|mol))(\w*-?\w*\s){0,4}\w*-?[Gg]lyco\w*(sites?|peptides?|proteins?|proteomes?|glycans?)'
    com_glyco_1=re.compile(glyco_pattern_1)

    glyco_pattern_2_1='(^|\s)(\d{2,}|\d+[,\d]+\d+)\s(?!(kDa|Da|pmol|mol))(\w*-?\w*\s){0,4}(sites?|proteins?)'
    com_glyco_2_1=re.compile(glyco_pattern_2_1)

    glyco_pattern_2_2='([Gg]lycosylat|GlcNAc|GlcNac|GalNAc|GalNac)'
    com_glyco_2_2=re.compile(glyco_pattern_2_2)

    glyco_pattern_3='(^|\s)(\d{2,}|\d+[,\d]+\d+)\s(?!(kDa|Da|pmol|mol))(\w*-?\w*\s){0,4}\w*-?([Gg]lycosylat\w*|[Gg]lycans?)'
    com_glyco_3=re.compile(glyco_pattern_3)

    abstract_text=raw_doc["text"]
    sentence = raw_doc["sentence"]

    detected_sent=[]
    for senInfo in sentence:
        this_sentence=abstract_text[int(senInfo["charStart"]):int(senInfo["charEnd"])+1]

        sr_glyco_1=com_glyco_1.search(this_sentence)
        sr_glyco_2_1=com_glyco_2_1.search(this_sentence)
        sr_glyco_2_2=com_glyco_2_2.search(this_sentence)
        sr_glyco_3=com_glyco_3.search(this_sentence)
        '''
        if str(pmid) =='10764840':
            print('this_sentence',this_sentence)
            print('sr_glyco_1',sr_glyco_1)
            print('sr_glyco_2_1',sr_glyco_2_1)
            print('sr_glyco_2_2',sr_glyco_2_2)
            print('sr_glyco_3',sr_glyco_3)
        '''
        if sr_glyco_1:
            detected_sent.append(this_sentence)
        elif sr_glyco_2_1 and sr_glyco_2_2:
            detected_sent.append(this_sentence)
        elif sr_glyco_3:
            detected_sent.append(this_sentence)


    return detected_sent


if __name__ == '__main__':
    '''
    output_txt='glyco_abstract.txt'
    output_txt_empty='glyco_abstract_empty.txt'
    pmidFile='pmid-Largescale-set.txt'
    pmidList = pd.read_csv(pmidFile, header=None).iloc[:, 0].tolist()
    with open(output_txt, 'w') as fo:
        with open(output_txt_empty, 'w') as fe:
            for pi in pmidList:
                raw_doc=read_abstract_from_mongodb('medline_current','text',pi)

                detected_sent=detect_glyco_info_from_abstract(raw_doc)
                if detected_sent is None or len(detected_sent)==0:
                    fe.write(str(pi))
                    fe.write('\n')
                else:
                    fo.write(str(pi))
                    fo.write('\n')
                    for si in detected_sent:
                        sii=si.encode('utf-8')
                        fo.write(sii)
                        fo.write('\n')
                    fo.write('\n')
    '''
    file_input_list=['human_proteoform_glycosylation_sites_glyconnect_pmid.txt', \
                     'human_proteoform_glycosylation_sites_unicarbkb_pmid.txt', \
                     'mouse_proteoform_glycosylation_sites_glyconnect_pmid.txt', \
                     'mouse_proteoform_glycosylation_sites_unicarbkb_pmid.txt', \
                     'rat_proteoform_glycosylation_sites_glyconnect_pmid.txt', \
                     'rat_proteoform_glycosylation_sites_unicarbkb_pmid.txt','large_scale_95_pmid.txt']
    #output_txt='./glyconnect_unicarb/detect_glyco_human_proteoform_glycosylation_sites_glyconnect.txt'
    #output_txt_empty='./glyconnect_unicarb/detect_glyco_human_proteoform_glycosylation_sites_glyconnect_empty.txt'
    #pmidFile='./glyconnect_unicarb/human_proteoform_glycosylation_sites_glyconnect_pmid.txt'
    '''
    for pmidFile in file_input_list:
        output_txt='detect_glyco_'+pmidFile.split('.')[0][:-5]+'.txt'
        output_txt_empty='detect_glyco_'+pmidFile.split('.')[0][:-5]+'_empty.txt'
        pmidList = pd.read_csv('./glyconnect_unicarb/'+pmidFile, header=None).iloc[:, 0].tolist()
        with open('./glyconnect_unicarb/'+output_txt, 'w') as fo:
            with open('./glyconnect_unicarb/'+output_txt_empty, 'w') as fe:
                for pi in pmidList:
                    raw_doc=read_abstract_from_mongodb('medline_current','text',pi)

                    detected_sent=detect_glyco_info_from_abstract(raw_doc)
                    if detected_sent is None or len(detected_sent)==0:
                        fe.write(str(pi))
                        fe.write('\n')
                    else:
                        fo.write(str(pi))
                        fo.write('\n')
                        for si in detected_sent:
                            sii=si.encode('utf-8')
                            fo.write(sii)
                            fo.write('\n')
                        fo.write('\n')

    '''
    for pmidFile in file_input_list:
        output_csv='detect_glyco_'+pmidFile.split('.')[0][:-5]+'.tsv'
        output_txt_empty='detect_glyco_'+pmidFile.split('.')[0][:-5]+'_empty.txt'
        pmidList = pd.read_csv('./glyconnect_unicarb/'+pmidFile, header=None).iloc[:, 0].tolist()

        with open('./glyconnect_unicarb/'+output_csv, 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            spamwriter.writerow(['pmid','sentence'])
            with open('./glyconnect_unicarb/'+output_txt_empty, 'w') as fe:
                for pi in pmidList:
                    raw_doc=read_abstract_from_mongodb('medline_current','text',pi)

                    detected_sent=detect_glyco_info_from_abstract(raw_doc,pi)
                    if detected_sent is None or len(detected_sent)==0:
                        fe.write(str(pi))
                        fe.write('\n')
                    else:

                        for si in detected_sent:
                            row=[str(pi),si]
                            row=[ri.encode('utf-8') for ri in row ]
                            spamwriter.writerow(row)


