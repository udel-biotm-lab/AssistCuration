import json,re

json_file='./Glygen/glygen_pmc/section_dic.json'
with open(json_file) as jfile:
    section_dic=json.load(jfile)

suppl_pattern='(Table\sS?\d{1,3}|\(.*[Ss]uppl.*\)|Figure\sS?\d{1,3}|Fig\sS?\d{1,3})'
com_suppl=re.compile(suppl_pattern)

glyco_pattern_1='(^|\s)(\d{2,}|\d+[,\d]+\d+)\s(?!(kDa|Da|pmol|mol))(\w*-?\w*\s){0,4}\w*-?[Gg]lyco\w*(sites?|peptides?|proteins?|proteomes?|glycans?)'
com_glyco_1=re.compile(glyco_pattern_1)

glyco_pattern_2_1='(^|\s)(\d{2,}|\d+[,\d]+\d+)\s(?!(kDa|Da|pmol|mol))(\w*-?\w*\s){0,4}(sites?|proteins?)'
com_glyco_2_1=re.compile(glyco_pattern_2_1)

glyco_pattern_2_2='([Gg]lycosylat|GlcNAc|GlcNac|GalNAc|GalNac)'
com_glyco_2_2=re.compile(glyco_pattern_2_2)

glyco_pattern_3='(^|\s)(\d{2,}|\d+[,\d]+\d+)\s(?!(kDa|Da|pmol|mol))(\w*-?\w*\s){0,4}\w*-?([Gg]lycosylat\w*|[Gg]lycans?)'
com_glyco_3=re.compile(glyco_pattern_3)

#patterns of no number (nn) in detection
glyco_pattern_nn_1='[Gg]lyco\w*(sites?|peptides?|proteins?|proteomes?|glycans?)'
com_glyco_nn_1=re.compile(glyco_pattern_nn_1)

glyco_pattern_nn_2_1='(sites?|proteins?)'
com_glyco_nn_2_1=re.compile(glyco_pattern_nn_2_1)

glyco_pattern_nn_2_2='([Gg]lycosylat|GlcNAc|GlcNac|GalNAc|GalNac)'
com_glyco_nn_2_2=re.compile(glyco_pattern_nn_2_2)

glyco_pattern_nn_3='([Gg]lycosylat\w*|[Gg]lycans?)'
com_glyco_nn_3=re.compile(glyco_pattern_nn_3)

#detection of suppl.*
detection_suppl_dic={}
for ki in section_dic.keys():
    id_split=ki.split('<|>')
    doc_id=id_split[0]
    section_id=id_split[1]
    subsection_id=id_split[2]
    for si in range(len(section_dic[ki])):
        sr=com_suppl.search(section_dic[ki][si])
        if sr:
            three_sentences=[]
            #print(id_split)
            if si>0:
                three_sentences.append(section_dic[ki][si-1])
                #print(section_dic[ki][si-1])
            three_sentences.append(section_dic[ki][si])
            #print(section_dic[ki][si])
            if si<len(section_dic[ki])-1:
                three_sentences.append(section_dic[ki][si+1])
                #print(section_dic[ki][si+1])
            if ki in detection_suppl_dic:
                detection_suppl_dic[ki].append(three_sentences)
            else:
                detection_suppl_dic[ki]=[three_sentences]

doc_id_filter=['PMC3938046', 'PMC3942810', 'PMC5795011', 'PMC7124471', 'PMC6243375']
#detection of glyco.* site etc
detection_glyco_dic={}
for ki in section_dic.keys():
    id_split=ki.split('<|>')
    doc_id=id_split[0]
    section_id=id_split[1]
    subsection_id=id_split[2]
    print(doc_id)
    if len(doc_id_filter)>0:
        if doc_id not in doc_id_filter:
            continue
    for si in range(len(section_dic[ki])):
        sr=com_suppl.search(section_dic[ki][si])
        
        if sr:
            #print(section_dic[ki][si])
            sentence_center=[]
            sentences_before_after=[]
            #print(id_split)
            if si>0:
                sentences_before_after.append(section_dic[ki][si-1])
                #print(section_dic[ki][si-1])
            sentence_center.append(section_dic[ki][si])
            #print(section_dic[ki][si])
            if si<len(section_dic[ki])-1:
                sentences_before_after.append(section_dic[ki][si+1])
                #print(section_dic[ki][si+1])


            for si in sentence_center:
                sr_glyco_nn_1=com_glyco_nn_1.search(si)
                sr_glyco_nn_2_1=com_glyco_nn_2_1.search(si)
                sr_glyco_nn_2_2=com_glyco_nn_2_2.search(si)
                sr_glyco_nn_3=com_glyco_nn_3.search(si)

                if sr_glyco_nn_1 or (sr_glyco_nn_2_1 and sr_glyco_nn_2_2) or sr_glyco_nn_3:

                    if ki in detection_glyco_dic:
                        detection_glyco_dic[ki].append(si)
                    else:
                        detection_glyco_dic[ki]=[si]
            
            for si in sentences_before_after:
                sr_glyco_1=com_glyco_1.search(si)
                sr_glyco_2_1=com_glyco_2_1.search(si)
                sr_glyco_2_2=com_glyco_2_2.search(si)
                sr_glyco_3=com_glyco_3.search(si)

                if sr_glyco_1 or (sr_glyco_2_1 and sr_glyco_2_2) or sr_glyco_3:

                    if ki in detection_glyco_dic:
                        detection_glyco_dic[ki].append(si)
                    else:
                        detection_glyco_dic[ki]=[si]
    
    #for the figure and table
    if id_split[-1].startswith('Table') or id_split[-1].startswith('Fig'):
        sr_glyco_nn_1=com_glyco_nn_1.search(section_dic[ki][0])
        sr_glyco_nn_2_1=com_glyco_nn_2_1.search(section_dic[ki][0])
        sr_glyco_nn_2_2=com_glyco_nn_2_2.search(section_dic[ki][0])
        sr_glyco_nn_3=com_glyco_nn_3.search(section_dic[ki][0])

        if sr_glyco_nn_1 or (sr_glyco_nn_2_1 and sr_glyco_nn_2_2) or sr_glyco_nn_3:

            if ki in detection_glyco_dic:
                detection_glyco_dic[ki].append(section_dic[ki][0])
            else:
                detection_glyco_dic[ki]=[section_dic[ki][0]]

    #for the abstract
    if id_split[-1].startswith('Abstract'):
        for si in section_dic[ki]:
            sr_glyco_1=com_glyco_1.search(si)
            sr_glyco_2_1=com_glyco_2_1.search(si)
            sr_glyco_2_2=com_glyco_2_2.search(si)
            sr_glyco_3=com_glyco_3.search(si)

            if sr_glyco_1 or (sr_glyco_2_1 and sr_glyco_2_2) or sr_glyco_3:

                if ki in detection_glyco_dic:
                    detection_glyco_dic[ki].append(si)
                else:
                    detection_glyco_dic[ki]=[si]

output_folder='./Glygen/glygen_pmc/Assisting_curation/'
#overwrite the previous results
for ki in detection_glyco_dic.keys():
    detection_glyco_dic[ki]=list(set(detection_glyco_dic[ki]))
    id_split=ki.split('<|>')
    doc_id=id_split[0]
    output_file=output_folder+doc_id+'.txt'
    with open(output_file, 'w') as fo:
        fo.write('docId: '+doc_id)
        fo.write('\n')

output_dic={}
for ki in detection_glyco_dic.keys():
        id_split=ki.split('<|>')
        doc_id=id_split[0]
        section_id=id_split[1]
        subsection_id=id_split[2]
        output_file=output_folder+doc_id+'.txt'
        with open(output_file, 'a') as fo:
            if id_split[-1].startswith('Table') or id_split[-1].startswith('Fig') \
                or id_split[-1].startswith('Abstract'):
                fo.write('Section: '+id_split[-1])
            else:
                fo.write('Section: '+subsection_id)
            fo.write('\n')
            detection_num=1
            for si in detection_glyco_dic[ki]:
                fo.write(str(detection_num)+'. ')
                fo.write(si)
                fo.write('\n')
                detection_num+=1
            fo.write('\n')
            fo.write('\n')
            fo.write('\n')
                

'''
#write the results into a text file
output_file='./Glygen/PMC/detection_suppl.txt'
with open(output_file, 'w') as fo:
    for ki in detection_suppl_dic.keys():
        fo.write(ki)
        fo.write('\n')
        detection_num=1
        for di in detection_suppl_dic[ki]:
            fo.write('Detection '+str(detection_num)+':')
            fo.write('\n')
            for si in di:
                fo.write(si)
                fo.write('\n')
            fo.write('\n')
            detection_num+=1


            
'''
            
