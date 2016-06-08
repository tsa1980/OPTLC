#!/usr/bin/env python
# -*- coding: CP866 -*-
# (c) Токарев С.А. 2009-2016

import pyexpat
import sys
import math
import string
import os.path


if len(sys.argv) == 1 :
    print "TLC2SVG v.1.0. (c) Токарев С.А."
    print "Используйте : [python] ./TLC2SVG.py <xml-file>"
    sys.exit()


xmlfile = open(sys.argv[1], "r")


###################
# Параметры цепей #
###################
line = []



##################################
# Параметры грозозащитных тросов #
# заземлённых по концам          #
##################################
wire = []


##################################
# Параметры грозозащитных тросов #
# заземлённых c одного конца     #
##################################
rope = []


############################
# Вспомогательные величины #
############################
item = {}
X    = []
Y    = []
pcdata = ""



#############################
# Интерфейс обработчика XML #
#############################
def end_element(name):
    global line, wire, rope, item, X, Y, pcdata, ro, length
    if name == 'data':
        pass
    elif name == 'line':
	item['X'] = X
	item['Y'] = Y
	X = []
	Y = []
	line.append(item)
	item = {}
    elif name == 'wire':
	item['X'] = X
	item['Y'] = Y
	X = []
	Y = []
	wire.append(item)
	item = {}
    elif name == 'rope':
	item['X'] = X
	item['Y'] = Y
	X = []
	Y = []
	rope.append(item)
	item = {}
    elif name == 'ro':
	ro = string.atof(pcdata)
    elif name == 'length':
	length = string.atof(pcdata)
    elif name == 'X':
	X.append(string.atof(pcdata))
    elif name == 'Y':
	Y.append(string.atof(pcdata))
    elif name == 'name':
	item[name.encode("CP866")] = pcdata
    else:
	item[name.encode("CP866")] = string.atof(pcdata)
     

def char_data(data):
    global pcdata
    pcdata = data.encode("CP866")


xmldata = pyexpat.ParserCreate()
xmldata.returns_unicode = 1
xmldata.EndElementHandler = end_element
xmldata.CharacterDataHandler = char_data

xmldata.ParseFile(xmlfile)

xmlfile.close()


###################################
# Параметры массивов и счетчиков  #
###################################
l = len(line)	# Количество линий/цепей
w = len(wire)	# Количество тросов заземлённых тросов по концам
r = len(rope)	# Количество тросов заземлённых тросов по концам
n = l + w + r	# Общее количество линий/цепей и тросов 


###################################
# Заполняем значения по умолчанию #
###################################
itemdefvals = {'n':1, 'l':0.0, 'f':0.0, 'dX':0.0, 'dY':0.0}

def getitem(index):
    if index < l:
	return line[index]
    elif index < l+w:
	return wire[index-l]
    return rope[index-l-w]

for i in xrange(n):
    item = getitem(i)
    for j in itemdefvals.keys():
        if not item.has_key(j):
            item[j] = itemdefvals[j]
              

#####################
# Печатаем SVG файл #
#####################
print """<?xml version="1.0" encoding="cp866" standalone="yes"?>
<svg version = "1.1"
     baseProfile="full"
     xmlns = "http://www.w3.org/2000/svg" 
     xmlns:xlink = "http://www.w3.org/1999/xlink"
     xmlns:ev = "http://www.w3.org/2001/xml-events" """


###########
# Размеры #
###########
xmin =  1.e10
xmax = -1.e10
ymin =  1.e10
ymax = -1.e10

for i in xrange(n):
    item = getitem(i)
    for j in xrange(len(item['X'])):
        x = item['X'][j] + item['dX']
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        y = item['Y'][j] + item['dY'] - item['l'] - 2./3.*item['f']
        ymin = min(ymin, y)
        ymax = max(ymax, y)

xmin -= 8
xmax += 8
ymin -= 8
ymax += 8


print "     height = \"%dpx\"  width = \"%dpx\">" % (ymax*10+25*(l+1), max((xmax-xmin)*10, 500))
print "     <line x1=\"%dpx\" y1=\"%dpx\" x2=\"%dpx\" y2=\"%dpx\" stroke=\"black\" stroke-width=\"2\" />" % (10, 10, 60, 10)
print "     <line x1=\"%dpx\" y1=\"%dpx\" x2=\"%dpx\" y2=\"%dpx\" stroke=\"black\" stroke-width=\"1\" />" % (10, 6, 10, 14)
print "     <line x1=\"%dpx\" y1=\"%dpx\" x2=\"%dpx\" y2=\"%dpx\" stroke=\"black\" stroke-width=\"1\" />" % (60, 6, 60, 14)
print "     <text x =\"35px\" y =\"25px\" text-anchor=\"middle\" fill=\"black\">5 м</text>"

#########
# Линии #
#########
color = ["yellow", "green", "red"]
for i in xrange(l):
    li = line[i]
    sx = 0
    my = ymax
    for j in xrange(len(li['X'])):
        x = li['X'][j] + li['dX']
        y = li['Y'][j] + li['dY'] - li['l'] - 2./3.*li['f']
        sx += x
        my = min(my, y)
        print "     <circle cx=\"%dpx\" cy=\"%dpx\" r=\"4px\" fill=\"%s\" />" % ((x-xmin)*10, (ymax-y)*10, color[j])
        print "     <text x=\"%dpx\" y=\"%dpx\" fill=\"black\">Л-%d</text>" % ((x-xmin)*10+6, (ymax-y)*10+6, i+1)
    sx /= 3.
    print "     <text x=\"%dpx\" y=\"%dpx\" fill=\"black\">Л-%d : %s</text>" % (10, ymax*10+25*(i+1)+5, i+1, line[i]['name'])

#   print "     <text x=\"%dpx\" y=\"%dpx\" text-anchor=\"middle\" fill=\"black\">Л-%d : %s</text>" % ((sx-xmin)*10+6, ymax*10+30, i+1, line[i]['name'])

#########
# Тросы #
#########
for i in xrange(l, n):
    wri = getitem(i)
    x = wri['X'][0] + wri['dX']
    y = wri['Y'][0] + wri['dY'] - wri['l'] - 2./3.*wri['f']
    print "     <circle cx=\"%dpx\" cy=\"%dpx\" r=\"4px\" fill=\"black\" />" % ((x-xmin)*10, (ymax-y)*10)
    print "     <text x=\"%dpx\" y=\"%dpx\" fill=\"black\">Т-%d</text>" % ((x-xmin)*10+6, (ymax-y)*10+6, i-l+1)


#########
# Земля #
#########
print "     <line x1=\"%dpx\" y1=\"%dpx\" x2=\"%dpx\" y2=\"%dpx\" stroke=\"black\" stroke-width=\"2\" />" % (10, (ymax)*10, (xmax-xmin-1)*10, (ymax)*10)
for i in xrange(18, int((xmax-xmin-1)*10), 8):
    print "     <line x1=\"%dpx\" y1=\"%dpx\" x2=\"%dpx\" y2=\"%dpx\" stroke=\"black\" stroke-width=\"1\" />" % (i, (ymax)*10, i-8, (ymax)*10+8)
       
print "</svg>"
