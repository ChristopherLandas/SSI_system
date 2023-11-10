import os
import re

def get_ip():
    file=os.popen("ipconfig")
    data=file.read()
    file.close()
    bits=[s.strip() for s in data.strip().split('\n')]
    
    for i in range(len(bits)):
        if 'Default' in bits[i]:
            li1 = re.search(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$', bits[i][bits[i].index(': ')+2:])
            li2 = re.search(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$', bits[i+1])
            if li1 is not None:
                return li1[0]
            if li2 is not None:
                return bits[i+1]
print(get_ip())