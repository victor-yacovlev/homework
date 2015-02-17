#-*- coding: utf-8 -*-
import sys
import time
import xml.etree.ElementTree as getXml

def getdata(path):
    data = getXml.parse(path).getroot()
    nets = 0
    threads = []
    for child in data:
        if (child.tag == 'net'):
            nets += 1
        #                                   BUG HERE ──────┐
        #                                                  │
        #                                                  │
        elif (child.tag == 'resistor' or child.tag == 'capator'):
            threads.append({'net_to':int(child.attrib['net_to']) - 1,
                            'net_from':int(child.attrib['net_from']) - 1,
                            'resistance':float(child.attrib['resistance'])})
            threads.append({'net_to':int(child.attrib['net_from']) - 1,
                            'net_from':int(child.attrib['net_to']) - 1,
                            'resistance':float(child.attrib['resistance'])})
        elif (child.tag == 'diode'):
            threads.append({'net_to':int(child.attrib['net_to']) - 1,
                            'net_from':int(child.attrib['net_from']) - 1,
                            'resistance':float(child.attrib['resistance'])})
            threads.append({'net_to':int(child.attrib['net_from']) - 1,
                            'net_from':int(child.attrib['net_to']) - 1,
                            'resistance':float(child.attrib['reverse_resistance'])})
    return({'nets':nets,'threads':threads})

def divis(a,b):
    try:
        r = a/b
    except ZeroDivisionError:
        r = float('inf')
    return r
        
def Uorsh(data):
    N = data['nets']
    d = []
    for i in range(N):
        d.append([float('inf')]*N)
    for i in range(N):
        d[i][i] = 0
    for i in data['threads']:
        d[i['net_from']][i['net_to']] = divis(1,(divis(1,d[i['net_from']][i['net_to']]) + divis(1,i['resistance'])))
    for k in range(N):
        for i in range(N):
            for j in range(N):
                d[i][j] = divis(1,(divis(1,d[i][j]) + divis(1,(d[i][k] + d[k][j]))))
    for i in range(N):
            for j in range(N):
                # Still a bug here. 
                # str(round()) is not the same as ".6f" formatted print 
                # Example: 
                #          19.5822 is a result of str(round()), but
                #          expected 19.582200
                d[i][j] = str(round(d[i][j],6))
    return(d)

def out(elems,path):
    f = open(path,'w')
    for i in elems:
        f.write(','.join(i) + '\n')

if __name__ == '__main__':
    now = time.time()
    path = str(sys.argv[1])
    pathout = str(sys.argv[2])
    out(Uorsh(getdata(path)),pathout)
    now = time.time() - now
    print(now*1000)
