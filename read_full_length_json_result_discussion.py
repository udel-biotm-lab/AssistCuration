import json,re

with open('./Glygen/glygen_pmc/for_vijay_20210430.json') as f:
  data = json.load(f)

for di in data:
  doc_id=di['docId']
  doc_id=doc_id.split('-')[0]
  output_file='./Glygen/glygen_pmc/processed/'+doc_id+'.txt'
  with open(output_file, 'w') as fo:
    fo.write('docId: '+doc_id)
    fo.write('\n')

section_num=1
subsection_num=1
figure_num=1
previous_sec=''
previous_doc=''

#create a dictionary to store the sentences in a list
#the key is docid--->section--->subsection
section_dic={}
section_with_id_dic={}
current_key=''
current_section=''
current_subsection=''
for di in data:
  doc_id=di['docId']
  doc_id=doc_id.split('-')[0]
  output_file='./Glygen/glygen_pmc/processed/'+doc_id+'.txt'
  if previous_doc!=doc_id:
    
    section_num=1
    subsection_num=1
    figure_num=1
  previous_doc=doc_id
  with open(output_file, 'a') as fo:
    
    if not (di['sec_type']=='results' or di['sec_type']=='discussion' or di['sec_type']=='abstract'):
        continue
    
    if di['type']=='SEC':
      if len(di['parent'])==0:
        section_id=doc_id+'-'+str(section_num)
        sub_section_id=section_id
        fo.write(section_id)
        fo.write('\n')
        section_num+=1
        subsection_num=1
        current_section=di['text']
        current_subsection=' '
      else:
        sub_section_id=section_id+'-'+str(subsection_num)
        fo.write(sub_section_id)
        fo.write('\n')
        subsection_num+=1
        current_subsection=di['text']
        for si in di['sentence']:
            fo.write(re.sub('[\r\n]+',' ',di['text'][si['charStart']:si['charEnd']+1]))
            fo.write('\n')

        #write the sentences into a dictionary with subsection_id
        if sub_section_id not in section_with_id_dic:
          section_with_id_dic[sub_section_id]=[]
        for si in di['sentence']:
          section_with_id_dic[sub_section_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
      previous_sec='SEC'

    elif di['type']=='ABS':
      current_sentence_id=doc_id+'<|> <|> <|>Abstract'
      if current_sentence_id in section_dic:
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
          
      else:
        section_dic[current_sentence_id]=[]
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
          

    elif di['type']=='FIG':
      current_sentence_id=doc_id+'<|>'+current_section+'<|>'+current_subsection+'<|>Fig '+di['fig_id']
      if current_sentence_id in section_dic:
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
          #only keep the figure title
          break
      else:
        section_dic[current_sentence_id]=[]
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
          #only keep the figure title
          break
          
      fig_id=section_id+'-fig'+str(figure_num)
      fo.write(fig_id)
      fo.write('\n')
      #current_subsection='FIG: '+di['text']
      for si in di['sentence']:
        fo.write(di['text'][si['charStart']:si['charEnd']+1])
        fo.write('\n')

      #write the sentences into a dictionary with fig id
      if fig_id not in section_with_id_dic:
        section_with_id_dic[fig_id]=[]
      for si in di['sentence']:
        section_with_id_dic[fig_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
      
      previous_sec='FIG'
      figure_num+=1
    
    elif di['type']=='TBL':
      current_sentence_id=doc_id+'<|>'+current_section+'<|>'+current_subsection+'<|>Table'+di['table_id'][1:]
      if current_sentence_id in section_dic:
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
          #only keep the figure title
          break
      else:
        section_dic[current_sentence_id]=[]
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
          #only keep the figure title
          break

    elif di['type']=='P':
      current_sentence_id=doc_id+'<|>'+current_section+'<|>'+current_subsection
      if current_sentence_id in section_dic:
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
      else:
        section_dic[current_sentence_id]=[]
        for si in di['sentence']:
          section_dic[current_sentence_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))
      
      #write the sentences into a dictionary with subsection_id
      if sub_section_id not in section_with_id_dic:
        section_with_id_dic[sub_section_id]=[]
      for si in di['sentence']:
        section_with_id_dic[sub_section_id].append(re.sub('[\r\n]+','',di['text'][si['charStart']:si['charEnd']+1]))

      if previous_sec=='P':
        fo.write('\n')
        for si in di['sentence']:
          fo.write(re.sub('[\r\n]+',' ',di['text'][si['charStart']:si['charEnd']+1]))
          fo.write('\n')
      else:
        for si in di['sentence']:
          fo.write(re.sub('[\r\n]+',' ',di['text'][si['charStart']:si['charEnd']+1]))
          fo.write('\n')
      previous_sec='P'


json_file='./Glygen/glygen_pmc/section_dic_05022021.json'
with open(json_file,'w') as outfile:
    json.dump(section_dic,outfile,ensure_ascii=False)


json_file='./Glygen/glygen_pmc/section_with_id_dic_05022021.json'
with open(json_file,'w') as outfile:
    json.dump(section_with_id_dic,outfile,ensure_ascii=False)