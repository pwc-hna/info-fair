from subprocess import call

def hello(text=None):
    print ("Executing script")
    ret = call(["python", "ml_named_entity_recognition.py", "text"])
    return ret
    if text is None:
        return "-1"


    import spacy
    # from spacy import displacy
    # import HTMLParser
    # import io

    nlp = spacy.load('en') # install 'en' model (python3 -m spacy download en)
    print ("Analyzing text ..." + text)
    doc = nlp(text)
    money_labels = []
    for ent in doc.ents:
        if ent.label_ == 'MONEY':
            print [(ent.text, ent.label)] 
            money_labels.append(ent.text)
    if len(money_labels) > 0:
        # Invoice
        return '1'
    # CV
    return '0'

def fib(n):
    if n==1 or n==2:
        return 1
    return fib(n-1)+fib(n-2)
	
def arr(length, value=None):
    return [value] * length

import sys
if __name__ == '__main__':
    hello(sys.argv[1])

# from datetime import datetime
# now = datetime.now()
# mm = str(now.month)
# dd = str(now.day)
# yyyy = str(now.year)
# hour = str(now.hour)
# mi = str(now.minute)
# ss = str(now.second)
# data = mm + "/" + dd + "/" + yyyy + " " + hour + ":" + mi + ":" + ss
# import ctypes
# ctypes.windll.user32.MessageBoxW(0, str(data), "DATA", 3)
