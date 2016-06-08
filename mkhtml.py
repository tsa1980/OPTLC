#!/usr/bin/env python
# -*- coding: CP866 -*-
# (c) Токарев С.А. 2009-2016

import string
import os
import sys

files = os.listdir(".")
print files

tlcs   = []
svgs   = [] 
txts   = [] 
for i in files:
    if i[-4:] == ".tlc" :
        tlcs.append(i)
        svgs.append(i[:-4] + ".svg")
        txts.append(i[:-4] + ".txt")

tlcs.sort()
svgs.sort() 
txts.sort()


htm = open("index.htm", "w")

print >>htm, """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML><HEAD><TITLE>OPTLC v.1.0</TITLE>
<META http-equiv=Content-Type content="text/html; charset=cp866">
<BODY>
<OL>""" 

for i in xrange(len(tlcs)):
    os.system("python optlc.py \"" + tlcs[i] + "\" > \"" + txts[i] + "\"")
    os.system("python tlc2svg.py \"" + tlcs[i] + "\" > \"" + svgs[i] + "\"")
    print >>htm, "<LI><A HREF=\"%s\">%s</A>(<A HREF=\"%s\">Рисунок</A>)" %(unicode(txts[i], "CP1251").encode("CP866"), unicode(txts[i][:-4], "CP1251").encode("CP866"), unicode(svgs[i], "CP1251").encode("CP866"))



print >>htm, "</OL></BODY></HTML>"




