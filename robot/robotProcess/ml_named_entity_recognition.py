import sys


def analyzeText(text=None):
    if text is None:
        return 100

    import spacy
    # from spacy import displacy
    # import HTMLParser
    # import io

    nlp = spacy.load('en') # install 'en' model (python3 -m spacy download en)
    # print ("Analyzing text ...")
    doc = nlp(text)
    money_labels = []
    for ent in doc.ents:
        if ent.label_ == 'MONEY':
            print [(ent.text, ent.label)] 
            money_labels.append(ent.text)
    if len(money_labels) > 3:
        # Invoice
        return 1
    # CV
    return 0

# file_name = io.open("documents/text_versions/1262192561.txt", mode="r", encoding="utf-8")
# raw_text = file_name.read()
# print "raw text = " + raw_text.encode("utf-8")
# utext = unicode(raw_text, "utf-8")
# text = HTMLParser.HTMLParser().unescape(raw_text)
# print "text = " + utext
# doc = nlp(raw_text)
# displacy.serve(doc, style='ent')

# print('Name Entity: {0}'.format(doc.ents))
# print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
# print "MONEY ents"
# money_labels = []
# for ent in doc.ents:
#     if ent.label_ == 'MONEY':
#         print [(ent.text, ent.label)] 
#         money_labels.append(ent.text)
# print (doc.ents)



if __name__ == '__main__':
    rc = analyzeText(sys.argv[1])
    exit(rc)
