import json

data = []
with open('test-1.json') as f:
    for line in f:
        data = json.loads(line)
        print data['key-1']
