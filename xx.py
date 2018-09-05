#!/usr/bin/python
#coding=utf-8
import os
import argparse
os.system('python zonghe2.py')

parser=argparse.ArgumentParser()
parser.add_argument('-i','--input',help='输入模板html文件')
args=parser.parse_args()
template=str(args.input)


def du(file):
    fh=open(file,'r') 
    for line in fh:
        listt=line.split("\t")
        yield listt        
g=du('add.T5VST1.identify.xls')
g2=du('T5VST1.diffgene.xls')
for i in range(5):
    g.next()
data='''<link rel="stylesheet" href="tablex.css"><div style="width: 1800px"><table class="gy"  width="95%"><tr><th>Term</th><th>Sample number</th><th>Background number</th><th>P-value</th><th>Corrected P-value</th><th style="overflow: hidden">UniGenes</th><th  style="overflow: hidden">KO</th><th>Entrez ID</th><th>Ensembl ID</th><th>Gene name</th></tr>
'''
for i in range(3):
    ll=g.next()
    l7=ll[7].split("|")
#    for i in l7:
#        yield i
    data=data+'<tr><td><a href=src/'+ll[2]+'.html target=_blank>'+ll[0]+'</a></td><td>'+ll[3]+'</td><td>'+ll[4]+'</td><td>'+ll[5]+'</td><td>'+ll[6]+'</td><td style="word-break: break-all">'+ll[7]+'</td><td style="word-break: break-all">'+ll[8]+'</td><td>'+ll[9]+'</td><td></td><td></td>'
    
data=data+'</table></div>'

line=os.popen("awk '/biao_ge_zhu_ti/{print NR}' "+template,'r')
line=line.read()

os.system('head -'+str(int(line)-1)+' '+template+' > ./result/test.html')

fh=open('./result/test.html','a')
fh.write(data)
fh.close()
os.system('tail -n +'+str(int(line)+1)+' '+template+' >> ./result/test.html')

os.system('cp ./ziyuan/tablex.css ./result/')
os.system('cp ./ziyuan/jquery.min.js ./result/')
os.system('cp ./ziyuan/logo.png ./result/')
os.system('cp ./ziyuan/*.png ./result/src')

