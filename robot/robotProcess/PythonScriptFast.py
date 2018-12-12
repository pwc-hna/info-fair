import os
import json
# import simplejson
JSON_DIR = "C:\\Work\\python-info-fair-wrapper\\documents\\validated\\json\\"

def mapNameToDocType(currentWindowTitle=None):
    currentWindowTitle = currentWindowTitle.split('.')[0]
    for filename in os.listdir(JSON_DIR):
        f = open(JSON_DIR + filename, 'rb')
        content = f.read()
        print("file content = "+str(content))
        json_data = json.loads(content.decode('utf-8'))
        if (json_data['file_name'] == currentWindowTitle):
            return str(json_data['text_analysis'])
    return '-1'

if __name__ == '__main__':
    print ("ret = " + mapNameToDocType('1262192561'))