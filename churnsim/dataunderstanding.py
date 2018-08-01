import json
"""
f = open('C:/Users/User/Desktop/MSC Project Work/FailureSimulator/churnsim/routertopology','r')
message = f.read()
d=json.loads(message)
for i in d.keys():
    print(i)
    for k in d[i]:
        print(k)

with open("C:/Users/User/Desktop/MSC Project Work/FailureSimulator/churnsim/routertopology", "r") as fin:
    content = json.load(fin)
"""
g=[]
with open("routerJSON.txt", "r") as f:
    message=f.read()
    d=json.loads(message)
    print(d["nodes"])
    g=[]



f.close()

