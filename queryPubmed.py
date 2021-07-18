#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division,print_function
import time,re,sys,os,ast,codecs
import pandas as pd
import pymongo
from pymongo import MongoClient
import random,operator
from collections import OrderedDict
from bson.son import SON
from bson.codec_options import CodecOptions
import urllib
import json
from xml.dom import minidom
from xml.etree import ElementTree as ET



def queryNCBI(termString,minPmid,maxPmid):
    print(termString)
    # ncbi_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%s&retstart=%s&retmax=%s" %(termString,minPmid,maxPmid)
    # https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer

    '''
    termString is the query string
    '''

    values = { 'db' : "pubmed", 'term' : termString,'retstart' : minPmid, 'retmax' : maxPmid, 'mindate':"1950/01/01", 'maxdate': "2021/03/01"}
    #values = {'term' : termString}
    data = urllib.parse.urlencode(values).encode("utf-8")
    print(data)
    ncbi_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"


    req = urllib.request.Request(ncbi_url, data)




    my_response =urllib.request.urlopen(req)


    # my_response = urllib2.urlopen(ncbi_url)
    htmlResp = my_response.read().decode('utf-8')

    t = ET.fromstring(htmlResp)
    pmidList = []
    for child in t.iter('Id'):
        pmidList.append(child.text)

    countList = []
    for child in t.iter('Count'):
        countList.append(child.text)

    return (pmidList,countList)

if __name__ == "__main__":


    # pmidListMongo is the list of docId from your database

    userquery = "(\"glycosylation site\" OR \"glycan structure\" OR \"N-linked\" OR \"O-linked\") AND (\"Humans\"[Mesh] OR \"Mice\"[Mesh] OR \"Rats\"[Mesh]) NOT proteom* "

    userquery="((glycosylation) AND (sites OR site)) AND (human OR mouse OR rat)"
    userquery="(human OR mouse OR rat) AND glycosylation AND (glycoprotein OR glycopeptide OR glycosite OR site)"
    #userquery="african swine fever"
    query = userquery

    minPmid = 0
    maxPmid = 20000000
    (pmidList,countList) = queryNCBI(query,str(minPmid),str(maxPmid))
    count = int(countList[0])
    print(len(pmidList),count)
    outputfile='glygen_assist_curation.txt'
    with codecs.open(outputfile,'w+',encoding='utf8') as file_object:
        for pi in pmidList:
            file_object.write(pi)
            file_object.write('\n')


