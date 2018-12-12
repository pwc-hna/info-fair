import spacy
from spacy import displacy
import json
import os
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

FILE_DIR = os.getcwd() + "\\documents\\validated\\"
JSON_DIR = FILE_DIR + "json\\"

nlp = spacy.load('en', disable=['parser', 'tagger','textcat'])
doc = None
aggregatedContent = ""

def run_spacy_named_entity_recognizer(fileContent):
    global doc
    print ("Analyzing text ...")
    doc = nlp(fileContent.decode('utf-8'))
    money_labels = []
    for ent in doc.ents:
        if ent.label_ == 'MONEY':
            money_labels.append(ent.text)
    if len(money_labels) > 3:
        print "INVOICE!"
        # Invoice
        return 1
    print "CV"
    # CV
    return 0

def write_result_to_file(fileName, fileContent, textAnalysisResult):
    extensionlessFileName, file_extension = os.path.splitext(fileName)
    data = {}
    data['file_name'] = extensionlessFileName
    data['text_analysis'] = str(textAnalysisResult)
    json_data = json.dumps(data,indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outFileName = JSON_DIR + extensionlessFileName + '.json'
    with io.open(outFileName, 'w', encoding='utf-8') as outfile:
        outfile.write(to_unicode(json_data))

    # with open(outFileName) as data_file:
    #     data_loaded = json.load(data_file)
    # print("is my data equal? "+ str(json_data == data_loaded))
    # print("data_loaded = "+ str(data_loaded))
    # print("json_data = "+ str(json_data))

# TXT_FILE1 = FILE_DIR+"8268312456.txt"
# f = open(TXT_FILE1, 'r')
# content = f.read()
# aggregatedContent += content
# aggregatedContent += "\n\n"
# print ("For filename = "+TXT_FILE1)
# textAnalysisResult = run_spacy_named_entity_recognizer(content)
# write_result_to_file(TXT_FILE1, content, textAnalysisResult)

for filename in os.listdir(FILE_DIR):
    if os.path.isdir(FILE_DIR + filename):
        continue
    f = open(FILE_DIR + filename, 'r')
    content = f.read()
    aggregatedContent += content
    aggregatedContent += "\n\n"
    print ("For filename = "+filename)
    textAnalysisResult = run_spacy_named_entity_recognizer(content)
    write_result_to_file(filename, content, textAnalysisResult)

doc = nlp(aggregatedContent.decode('utf-8'))
displacy.serve(doc, style='ent')


