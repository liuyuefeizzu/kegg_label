import os
#ath00='ath00360.html'




os.system('mkdir -p ./result/src')
os.system('cp ./ziyuan/ath00.* ./result/src/')
for a,b,c in os.walk('./pathway_ori'):
    l=[]
    ll=[]
    for fil in c:
        if os.path.splitext(fil)[1] == '.html':
            l.append(fil)
        if os.path.splitext(fil)[1] == '.png':
            ll.append(fil)

tail="</map></div></body></html>"

for ath00 in l:
    a='python ./xx2.py -i '+ath00
    data=os.popen(a,'r')
    data=data.read()
    fh=open('./result/src/'+ath00,'w')
    head='''
       <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>'''+str(ath00.split('.')[0])+'''</title><link rel="stylesheet" href="ath00.css"><script type="text/javascript" src="jquery.min.js"></script><script type="text/javascript" src="ath00.js"></script></head><body><div >
       '''
    fh.write(head)
    fh.write(data)
    fh.write(tail)
    fh.close
for i in ll:
    os.system('cp ./pathway_ori/'+i+' ./result/src/'+i)

