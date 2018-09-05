#!/usr/bin/python
#coding=utf-8
from bs4 import BeautifulSoup
import re
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('-i','--input')
args=parser.parse_args()
argu=args.input
argu=str(argu)
#argu='ath00360.html'
ath00=argu.split('.')[0]

print '''<img src="'''+ath00+'''.png"  name="pathwayimage" usemap="#mapdata" border="0" /><map name="mapdata">'''

def du(file):
    fh=open(file,'r') 
    for line in fh:
        listt=line.split("\t")
        yield listt        
g=du('add.T5VST1.identify.xls')
g2=du('T5VST1.diffgene.xls')
def l7(g):
    global bb
    bb=[]
    for i in range(5):
        g.next()
    for i in range(3):
        ll=g.next()
        l7=ll[7].split("|")
        l8=ll[8].split("|")
        l8=l8[:-1]
        bb.append({ll[2]:l8})
        for i in l7:
            yield i
        yield '#'
l7=l7(g)
#l7_存的是bra_gengid信息
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
    g2=du('T5VST1.diffgene.xls')
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
#print dic
#print "##################"
################################################
soup=BeautifulSoup(open('./pathway_ori/'+argu),'html.parser')
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
    print pi
    if str(i['shape']) == 'rect' and str(i['title'])[:2] == "AT":
  #      print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
        onmouse='''$popupTimer("entry","'''+str(i['title'])+'''", "#ffffff")"'''
        onmouse=onmouse+" title='"+str(i['title'])+"' "
        strtitle=str(i['title'])
 #        print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
       # href=str(i['href'])
        coord=str(i['coords']).split(',')
        coords=[]
        for a in coord:
            coords.append(str(int(a)+8))
   ######################         
        pp=p.sub('',str(i['title']))
        pp=p2.sub('',pp)
        pp=pp.split(',')
        
        up=''
        down=''
        for i in pp:
            for j in dic[ath00]:
                if str(i) == str(j[0]):
                    if str(j[1]) == '1':
                        up=up+str(j[2])+','
                        break
                    else:
                        down=down+str(j[2])+','
                        break
        #print up,'$',down,"###"



        
        if up != '' and down == '':
            print "<div>"+href+"<div class='tishi2'><img class='maps' src='bg_red.png' style='top:"+coords[1]+"px;left:"+coords[0]+'''px;width:47px;height:18px;position:absolute;' onmouseover="show('Detail'''+num+inhao+''')" /><span class='tishi' style='top:''' +str(int(coords[1])+30)+"px;left:"+str(int(coords[0])+15)+"px;position:absolute;'>" +strtitle+'''</span></div></a><div class='box' id="Detail'''+num+'''" style=' display:none;position: fixed; left: 25%; top: 0px; width: 56%; border: 3px solid rgb(36, 136, 229); background-color: rgb(105, 191, 244); opacity: 0.95; font-size: 12px; padding-right: 20px;'><div style='cursor: pointer; position: absolute;top:0px; right: 15px; color: rgb(12, 100, 200);' onclick="hide('Detail'''+num+inhao+''')" title='close' ><h4>Close</h4> </div><div><span style='display:block;'><ul><ul><li color='red'>up regulated gene KEGG_ID/KO</li><ul><font color='red'>'''+up+"</font></ul></ul></span></div></div></div>"
            num=str(int(num)+1)
        if up == '' and down != '':
            print "<div>"+href+"<div class='tishi2'><img class='maps' src='bg_green.png' style='top:"+coords[1]+"px;left:"+coords[0]+'''px;width:47px;height:18px;position:absolute;' onmouseover="show('Detail'''+num+inhao+''')" />  <span class='tishi' style='top:''' +str(int(coords[1])+30)+"px;left:"+str(int(coords[0])+15)+"px;position:absolute;'>" +strtitle+'''</span></div></a><div class='box' id="Detail'''+num+'''" style=' display:none;position: fixed; left: 25%; top: 0px; width: 56%; border: 3px solid rgb(36, 136, 229); background-color: rgb(105, 191, 244); opacity: 0.95; font-size: 12px; padding-right: 20px;'><div style='cursor: pointer; position: absolute;top:0px; right: 15px; color: rgb(12, 100, 200);' onclick="hide('Detail'''+num+inhao+''')" title='close' ><h4>Close</h4> </div><div><span style='display:block;'><ul><ul><li color='red'>down regulated gene KEGG_ID/KO</li><ul><font color='green'>'''+down+"</font></ul></ul></span></div></div></div>"
            num=str(int(num)+1)
        if up != '' and down != '':
            print "<div>"+href+"<div class='tishi2'><img class='maps' src='bg_yellow.png' style='top:"+coords[1]+"px;left:"+coords[0]+'''px;width:47px;height:18px;position:absolute;' onmouseover="show('Detail'''+num+inhao+''')" /><span class='tishi' style='top:''' +str(int(coords[1])+30)+"px;left:"+str(int(coords[0])+15)+"px;position:absolute;'>" +strtitle+'''</span></div></a><div class='box' id="Detail'''+num+'''" style=' display:none;position: fixed; left: 25%; top: 0px; width: 56%; border: 3px solid rgb(36, 136, 229); background-color: rgb(105, 191, 244); opacity: 0.95; font-size: 12px; padding-right: 20px;'><div style='cursor: pointer; position: absolute;top:0px; right: 15px; color: rgb(12, 100, 200);' onclick="hide('Detail'''+num+inhao+''')" title='close' ><h4>Close</h4> </div><div><span style='display:block;'><ul><ul><li color='red'>up regulated gene KEGG_ID/KO</li><ul><font color='red'>'''+up+"</font></ul></ul><ul><li color='red'>down regulated gene KEGG_ID/KO</li><ul><font color='green'>"+down+"</font></ul></ul></ul></span></div></div></div>"
            num=str(int(num)+1)


'''           
pb=pb+'0'
        if '1' in pb:
            if '2' in pb:
                print 'up_and_down'
            else:
                print 'up'
        elif '2' in pb:
            print 'down'
        else:
            print 'none'
        print '####',pb'''
