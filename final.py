#!/usr/bin/python
#coding=utf-8

#ath00='ath00360.html'
import os
import argparse
from bs4 import BeautifulSoup
import re

parser=argparse.ArgumentParser()
parser.add_argument('identify_file',help='输入identify文件')
parser.add_argument('diffgene_file',help='输入diffgene文件')
parser.add_argument('-r','--reference',help='输入参考物种的缩写，例如：ath')
parser.add_argument('-t','--template',help='输入要插入表格的html文件')


args=parser.parse_args()
template=str(args.template)
diffgene=str(args.diffgene_file)
identify=str(args.identify_file)
pathway=str(args.reference)
pathway='pathway_ori/'+pathway
###################################sheng_cheng_dic_zidian!!!!!!!!!!!!!!!!!!!!!!!

def du(file):
    fh=open(file,'r') 
    for line in fh:
        listt=line.split("\t")
        yield listt        
g=du(identify)
g2=du(diffgene)
hang=os.popen('wc -l '+identify)
hang=hang.read()
hang=int(hang.split()[0])
print hang
def l7(g):
    global bb
    bb=[]
    for i in range(5):
        g.next()
    for i in range(hang-15):
        ll=g.next()
        l7=ll[7].split("|")
        l8=ll[8].split("|")
        l8=l8[:-1]
        bb.append({ll[2]:l8})
        for i in l7:
            yield i
        yield '#'
l7=l7(g)
#l7_存的是bra_geneid信息
#g2存的是vs表的每一条记录
aa=''
cc=[]
dd=[]
for i in l7:
    for j in g2:
        if i == j[0]:
            dd.append(str(i)+'('+str(round(float(j[7]),4))+')')
            if float(j[7]) < -1.0:
                i=2
            elif float(j[7]) > 1.0:
                i=1
            break
    if i == '#':
        cc.append(dd)
        dd=[]
        
    aa=aa+str(i)
    g2=du(diffgene)
aa=aa.split('#')
aa=aa[:-1]
#aa_存的是上下调信息，以1,2表示上下调
#cc_存的是log2fc信息
#bb_存的是字典通过term可找到id列表，即是l7函数的l8列表变量
#dic_存的是term字典可找到一个元组信息（id,上下调，log2fc变化）
#print '$$$$$$$$$$$$$$$$$$$$$$$'
#此处的i变量是1,2,3term循环，k变量是term对应的列表里的循环
for i in range(len(bb)):
    for j in bb[i]:
        for k in range(len(bb[i][j])):
            bb[i][j][k]=(bb[i][j][k][4:],aa[i][k],cc[i][k])

dic={}
for i in bb:
    dic=dict(dic,**i)


#################################################



#######################xx2_de_putout!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def xx2_html_chu_li(dic,ath00):
    #进行xx2的html处理部分的打包，方便下面调用
    data='''<img src="'''+ath00.split('.')[0]+'''.png"  name="pathwayimage" usemap="#mapdata" border="0" /><map name="mapdata">'''
    soup=BeautifulSoup(open(pathway+'/'+ath00),'html.parser')
    #print soup.select('area')
    p=re.compile('\(.*?\)')
    p2=re.compile(r'\s*')
    p3=re.compile(r'/kegg-bin')
    p4=re.compile(r'/dbget-bin')
    p5=re.compile(r'></area>')
    num='0'
    inhao="'"
    for i in soup.map.find_all('area'):
        pi=p3.sub('http://www.kegg.jp/kegg-bin',str(i))
        pi=p4.sub('http://www.kegg.jp/dbget-bin',pi)
        pi=p5.sub("/>",pi)
        href="<a href='http://www.kegg.jp"+str(i['href'])+"'>"
        data=data+pi
        if str(i['shape']) == 'rect' and str(i['title'])[:2] == "AT":
  #          print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            onmouse='''$popupTimer("entry","'''+str(i['title'])+'''", "#ffffff")"'''
            onmouse=onmouse+" title='"+str(i['title'])+"' "
            strtitle=str(i['title'])
 #            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
           # href=str(i['href'])
            coord=str(i['coords']).split(',')
            coords=[]
            for a in coord:
                coords.append(str(int(a)+8))
   #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       
            pp=p.sub('',str(i['title']))
            pp=p2.sub('',pp)
            pp=pp.split(',')
        
            up=''
            down=''
            for i in pp:
                for j in dic[ath00.split('.')[0]]:
                    if str(i) == str(j[0]):
                        if str(j[1]) == '1':
                            up=up+str(j[2])+','
                            break
                        else:
                            down=down+str(j[2])+','
                            break
            #print up,'$',down,"###"



        
            if up != '' and down == '':
                data=data+"<div>"+href+"<div class='tishi2'><img class='maps' src='bg_red.png' style='top:"+coords[1]+"px;left:"+coords[0]+'''px;width:47px;height:18px;position:absolute;' onmouseover="show('Detail'''+num+inhao+''')" /><span class='tishi' style='top:''' +str(int(coords[1])+30)+"px;left:"+str(int(coords[0])+15)+"px;position:absolute;'>" +strtitle+'''</span></div></a><div class='box' id="Detail'''+num+'''" style=' display:none;position: fixed; left: 25%; top: 0px; width: 56%; border: 3px solid rgb(36, 136, 229); background-color: rgb(105, 191, 244); opacity: 0.95; font-size: 12px; padding-right: 20px;'><div style='cursor: pointer; position: absolute;top:0px; right: 15px; color: rgb(12, 100, 200);' onclick="hide('Detail'''+num+inhao+''')" title='close' ><h4>Close</h4> </div><div><span style='display:block;'><ul><ul><li color='red'>up regulated gene</li><ul><font color='red'>'''+up+"</font></ul></ul></span></div></div></div>"
                num=str(int(num)+1)
            if up == '' and down != '':
                data=data+"<div>"+href+"<div class='tishi2'><img class='maps' src='bg_green.png' style='top:"+coords[1]+"px;left:"+coords[0]+'''px;width:47px;height:18px;position:absolute;' onmouseover="show('Detail'''+num+inhao+''')" />  <span class='tishi' style='top:''' +str(int(coords[1])+30)+"px;left:"+str(int(coords[0])+15)+"px;position:absolute;'>" +strtitle+'''</span></div></a><div class='box' id="Detail'''+num+'''" style=' display:none;position: fixed; left: 25%; top: 0px; width: 56%; border: 3px solid rgb(36, 136, 229); background-color: rgb(105, 191, 244); opacity: 0.95; font-size: 12px; padding-right: 20px;'><div style='cursor: pointer; position: absolute;top:0px; right: 15px; color: rgb(12, 100, 200);' onclick="hide('Detail'''+num+inhao+''')" title='close' ><h4>Close</h4> </div><div><span style='display:block;'><ul><ul><li color='red'>down regulated gene</li><ul><font color='green'>'''+down+"</font></ul></ul></span></div></div></div>"
                num=str(int(num)+1)
            if up != '' and down != '':
                data=data+"<div>"+href+"<div class='tishi2'><img class='maps' src='bg_yellow.png' style='top:"+coords[1]+"px;left:"+coords[0]+'''px;width:47px;height:18px;position:absolute;' onmouseover="show('Detail'''+num+inhao+''')" /><span class='tishi' style='top:''' +str(int(coords[1])+30)+"px;left:"+str(int(coords[0])+15)+"px;position:absolute;'>" +strtitle+'''</span></div></a><div class='box' id="Detail'''+num+'''" style=' display:none;position: fixed; left: 25%; top: 0px; width: 56%; border: 3px solid rgb(36, 136, 229); background-color: rgb(105, 191, 244); opacity: 0.95; font-size: 12px; padding-right: 20px;'><div style='cursor: pointer; position: absolute;top:0px; right: 15px; color: rgb(12, 100, 200);' onclick="hide('Detail'''+num+inhao+''')" title='close' ><h4>Close</h4> </div><div><span style='display:block;'><ul><ul><li color='red'>up regulated gene</li><ul><font color='red'>'''+up+"</font></ul></ul><ul><li color='red'>down regulated gene</li><ul><font color='green'>"+down+"</font></ul></ul></ul></span></div></div></div>"
                num=str(int(num)+1)
  
    return data


################################################################


os.system('mkdir -p ./result/src')
os.system('cp ./ziyuan/ath00.* ./result/src/')
for a,b,c in os.walk(pathway):
    l=[]
    ll=[]
    for fil in c:
        if os.path.splitext(fil)[1] == '.html':
            l.append(fil)
        if os.path.splitext(fil)[1] == '.png':
            ll.append(fil)

tail="</map></div></body></html>"


for ath00 in l:
    data=xx2_html_chu_li(dic,ath00)
    fh=open('./result/src/'+ath00,'w')
    head='''
       <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>'''+str(ath00.split('.')[0])+'''</title><link rel="stylesheet" href="ath00.css"><script type="text/javascript" src="jquery.min.js"></script><script type="text/javascript" src="ath00.js"></script></head><body><div >
       '''
    fh.write(head)
    fh.write(data)
    fh.write(tail)
    fh.close
for i in ll:
    os.system('cp '+pathway+'/'+i+' ./result/src/'+i)

#############################xx.py_的内容，test.html的生成
g=du(identify)
g2=du(diffgene)
for i in range(5):
    g.next()
data_xx='''<link rel="stylesheet" href="tablex.css"><div style="width: 1800px"><table class="gy"  width="95%"><tr><th>Term</th><th>Sample number</th><th>Background number</th><th>P-value</th><th>Corrected P-value</th><th style="overflow: hidden">UniGenes</th><th  style="overflow: hidden">KO</th><th>Entrez ID</th><th>Ensembl ID</th><th>Gene name</th></tr>
'''
for i in range(hang-15):
    ll=g.next()
    l7=ll[7].split("|")
#    for i in l7:
#        yield i
    data_xx=data_xx+'<tr><td><a href=src/'+ll[2]+'.html target=_blank>'+ll[0]+'</a></td><td>'+ll[3]+'</td><td>'+ll[4]+'</td><td>'+ll[5]+'</td><td>'+ll[6]+'</td><td style="word-break: break-all">'+ll[7]+'</td><td style="word-break: break-all">'+ll[8]+'</td><td>'+ll[9]+'</td><td></td><td></td></tr>'
    
data_xx=data_xx+'</table></div>'

line=os.popen("awk '/biao_ge_zhu_ti/{print NR}' "+template,'r')
line=line.read()

os.system('head -'+str(int(line)-1)+' '+template+' > ./result/test.html')

fh=open('./result/test.html','a')
fh.write(data_xx)
fh.close()
os.system('tail -n +'+str(int(line)+1)+' '+template+' >> ./result/test.html')

os.system('cp ./ziyuan/tablex.css ./result/')
os.system('cp ./ziyuan/jquery.min.js ./result/')
os.system('cp ./ziyuan/logo.png ./result/')
os.system('cp ./ziyuan/*.png ./result/src')


