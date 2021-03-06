#!/usr/bin/env python
# -*- coding: CP866 -*-
# (c) ����ॢ �.�. 2009-2020
# �ணࠬ�� ��� �����
# ��ࠬ��஢ �奬 ����饭�� ����� 
# - � �⠫�묨 ��ᠬ�
# - � ���⮬ ����������樨

import pyexpat
import sys
import math
import string

VERSION = "1.1"

if len(sys.argv) == 1 :
    print "OPTLC v." + VERSION, "(c) ����ॢ �.�."
    print "�ᯮ���� : [python] ./optlc.py <xml-file>"
    sys.exit()


xmlfile = open(sys.argv[1], "r")

###########################
# ��ࠬ���� �����(����) #
###########################
ro   = 1134.05428945	# ����쭮� ᮯ�⨢����� ����� �� 㬮�砭��, ��*� 
		        # �� ⠪�� ���祭�� Dearth = 1000 �


###############
# ����� ����� #
###############
length = 1.			# ����� ����� �� 㬮�砭��, 1 �� 


############################
# ����� ��६������ ⮪� #
############################
freq   = 50.			     # ����� ��६������ ⮪�, ��


###################
# ��ࠬ���� 楯�� #
###################
line = []



##################################
# ��ࠬ���� �஧������� ��ᮢ #
# ��������� �� ���栬          #
##################################
wire = []


##################################
# ��ࠬ���� �஧������� ��ᮢ #
# ��������� c ������ ����     #
##################################
rope = []


############################
# �ᯮ����⥫�� ����稭� #
############################
item = {}
X    = []
Y    = []
pcdata = ""



#############################
# ����䥩� ��ࠡ��稪� XML #
#############################
def end_element(name):
    global line, wire, rope, item, X, Y, pcdata, ro, length, freq
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
    elif name == 'freq':
	freq = string.atof(pcdata)
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
# ��ࠬ���� ���ᨢ�� � ���稪��  #
###################################
l = len(line)	# ������⢮ �����/楯��
w = len(wire)	# ������⢮ ��ᮢ ��������� �� ���栬
r = len(rope)	# ������⢮ ��ᮢ ��������� c ������ ����
n = l + w + r	# ��饥 ������⢮ �����/楯�� � ��ᮢ 



###################################
# ������塞 ���祭�� �� 㬮�砭�� #
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
              

###########################
# ��ࠬ���� �����(����) #
###########################
lmbd   = 1./ro/10		        # ����쭠� �஢�������� ����� [���� �11], 1/(��*�)]
Dearth = 66.4 / math.sqrt(freq * lmbd)  # ���������⭠� ��㡨�� ���⭮�� �஢��� [���� �11, (2-64)], �
Rearth = math.pi*math.pi*freq/1E4       # ����⨢����� ���뢠�饥 ���� ��⨢��� ��魮�� � ����� [���� �11, (2-66)], ��/��


####################
# ����� � ����� #
####################
def matrix(n):
    mat = []
    for i in xrange(n):
        mat.append([])
        for j in xrange(n):
            mat[i].append(0.0)
    return mat

# ������ ��㣮�쭠� �����
def ltmatrix(n):
    mat = []
    for i in xrange(n):
        mat.append([])
        for j in xrange(i+1):
            mat[i].append(0.0)
    return mat

def vector(n):
    vec = []
    for i in xrange(n):
        vec.append(0.0)
    return vec

#####################################################################################################
#####################################################################################################
####                                                                                             ####
####   � � � � � �   � � � � � � � � � �   � � � � � � � � � �   � � � � �   � � � � � � � � �   ####
####                                                                                             ####
#####################################################################################################
#####################################################################################################


#######################################
# ����������� ࠤ��� �஢���(���) #
#######################################
ROeq = vector(n)

for i in xrange(l):
    ROeq[i] = line[i]['k'] * line[i]['d'] / 2000.
    if line[i]['n'] > 1:
        ROeq[i] = math.pow(ROeq[i] * math.pow( line[i]['a'], line[i]['n']-1), 1./line[i]['n'])

for i in xrange(l, l+w):
    if 'k' in wire[i-l]:
        ROeq[i] = wire[i-l]['k'] * wire[i-l]['d'] / 2000.
    else:
        ROeq[i] = wire[i-l]['d']/2000. / math.pow(10., wire[i-l]['x']/0.145)



###################################
# �।����������᪨� ����ﭨ� #
###################################

# ������뢠�� �।����������᪨� ����ﭨ�
# ����� �஢����� � ��ᠬ�, � ⠪�� �� ��ࠦ���ﬨ 
def gavg(ii, jj, prm):
    p = []
    pi = getitem(ii)
    pj = getitem(jj)
    for i in xrange(len(pi['X'])):
	xi = pi['X'][i] + pi['dX']
	yi = pi['Y'][i] + pi['dY'] - pi['l'] - 2./3.*pi['f']
        for j in xrange(len(pj['X'])):
	    xj = pj['X'][j] + pj['dX']
	    yj = pj['Y'][j] + pj['dY'] - pj['l'] - 2./3.*pj['f']
            d = math.hypot(xi - xj, yi - yj)
            if prm == "S":
                d = math.hypot(xi - xj, yi + yj)
            elif prm == "SL":
                if d <= 0.001 :  
                    d = 2*yi
                else:
                    d = 0.0  
            elif prm == "SM" :
                if d > 0.001 :  
                    d = math.hypot(xi - xj, yi + yj)
	    if d > 0.001:
	        p.append(d)
    if len(p) == 0:
	return 0
    pp = 1.0
    for i in p:
	pp = pp * i
    return pp**(1./len(p))	
    
Davg = ltmatrix(n)
for i in xrange(n):
    for j in xrange(i+1):
	Davg[i][j] = gavg(i,j,"D")

##################################################################
# �த���� ��ࠬ���� �奬� ����饭�� ��אַ� ��᫥����⥫쭮�� #
##################################################################
Z1 = vector(l)
for i in xrange(l):
    Z1[i] = line[i]['r'] / line[i]['n'] + 0.002894j*freq * math.log10(Davg[i][i] / ROeq[i])


###################################################################
# �த���� ��ࠬ���� �奬� ����饭�� �㫥��� ��᫥����⥫쭮�� #
###################################################################
Z0 = matrix(l+w)

# ����⢥��� ᮯ�⨢����� �����
for i in xrange(l):
    Z0[i][i] = line[i]['r'] / line[i]['n'] + 3*Rearth + 0.008682j*freq * math.log10(Dearth / pow(Davg[i][i]**2 * ROeq[i], 1./3.) )

# ������� ᮯ�⨢����� �����
for i in xrange(l):
    for j in xrange(i):
	Z0[j][i] = Z0[i][j] = 3*Rearth + 0.008682j*freq * math.log10(Dearth / Davg[i][j])

# ����⢥��� ᮯ�⨢����� ��ᮢ
for i in xrange(l,l+w):
    Z0[i][i] = 3*wire[i-l]['r'] + 3*Rearth + 0.008682j*freq * math.log10(Dearth / ROeq[i])

# ������� ᮯ�⨢����� ��ᮢ � �����
for i in xrange(l,l+w):
    for j in xrange(i):
        if j < l :
            msign = -1
        else:
            msign = 1
	Z0[j][i] = Z0[i][j] = msign*(3*Rearth + 0.008682j*freq * math.log10(Dearth / Davg[i][j])) 

# �����塞 ����
for k in xrange(l+w-1,l-1,-1):
    major = Z0[k][k]
    for j in xrange(l+w):
        Z0[k][j] /= major
    for i in xrange(l+w):     
	minor = Z0[i][k]
	for j in xrange(l+w):
	    Z0[i][j] -= minor*Z0[k][j]


#####################################################################################################
#####################################################################################################
####                                                                                             ####
####   � � � � � �   � � � � � � � � � �   � � � � � � � � � �   � � � � �   � � � � � � � � �   ####
####                                                                                             ####
#####################################################################################################
#####################################################################################################


#######################################
# ����������� ࠤ��� �஢���(���) #
#######################################
for i in xrange(l):
    ROeq[i] = line[i]['d'] / 2000.
    if line[i]['n'] > 1:
        ROeq[i] = (ROeq[i] * line[i]['a']**(line[i]['n']-1))** (1./line[i]['n'])

for i in xrange(l, l+w):
    ROeq[i] = wire[i-l]['d'] / 2000. 

for i in xrange(l+w, n):
    ROeq[i] = rope[i-l-w]['d']/2000.


###################################
# �।����������᪨� ����ﭨ� #
###################################
Savg  = ltmatrix(n)
for i in xrange(n):
    for j in xrange(i+1):
	Savg[i][j] = gavg(i,j,"S")

SLavg = vector(l)
SMavg = vector(l)
for i in xrange(l):
    SLavg[i]  = gavg(i,i,"SL")
    SMavg[i]  = gavg(i,i,"SM")


##################################################################
# ������� ��ࠬ���� �奬� ����饭�� ��אַ� ��᫥����⥫쭮�� #
##################################################################
Y1 = vector(l)
for i in xrange(l):
    Y1[i] = 2*math.pi*freq / (41.389E6 * math.log10(Davg[i][i] * SLavg[i] / ROeq[i] / SMavg[i]))


###################################################################
# ������� ��ࠬ���� �奬� ����饭�� �㫥��� ��᫥����⥫쭮�� #
###################################################################
A0 = matrix( max(n,2*l) )

# ����⢥��� �����樥��� �����
for i in xrange(l):
    A0[i][i] = 124.17E6 * math.log10(Savg[i][i] / pow(Davg[i][i]**2 * ROeq[i], 1./3.) )

# ������� �����樥��� �����
for i in xrange(l):
    for j in xrange(i):
	A0[j][i] = A0[i][j] = 124.17E6 * math.log10(Savg[i][j] / Davg[i][j])

# ����⢥��� �����樥��� ��ᮢ
for i in xrange(l,n):
    A0[i][i] = 41.389E6 * math.log10(Savg[i][i] / ROeq[i])

# ������� �����樥��� ��ᮢ
for i in xrange(l,n):
    for j in xrange(l,i):
	A0[j][i] = A0[i][j] = 41.389E6 * math.log10(Savg[i][j] / Davg[i][j])


# ������� �����樥��� ����� ����ﬨ � ��ᠬ�
for i in xrange(l,n):
    for j in xrange(l):
	A0[j][i] = 41.389E6 * math.log10(Savg[i][j] / Davg[i][j])
	A0[i][j] = 3 * A0[j][i]

# �����塞 ����
for k in xrange(n-1,l-1,-1):
    major = A0[k][k]
    for j in xrange(n):
        A0[k][j] /= major
    for i in xrange(n):     
	minor = A0[i][k]
	for j in xrange(n):
	    A0[i][j] -= minor*A0[k][j]


# ���頥� ������ ��⮤�� �����
# �� �ᯮ�짮����� NumPy ��� SciPy ����� �������
# Y0 = 2*math.pi*freq * numpy.linalg.inv(A0[:l,:l])
for k in xrange(l):
    A0[k][k+l] = 1.0

for k in xrange(l):
    major = A0[k][k];
    for j  in xrange(k+l+1):
        A0[k][j] /= major 	
    for i in xrange(k+1, k+l):
        major = A0[i][k]
	for j in xrange(k+l+1):
            A0[i][j] -= A0[k][j]*major


for k in xrange(l):
    for i in xrange(l-1, -1, -1):
        A0[i+l][k] = A0[i][k+l] 
        for j in xrange (l-1, i, -1):
            A0[i+l][k] -= A0[i][j]*A0[j+l][k]

# ������塞 ������ �஢������⥩
Y0 = ltmatrix(l)
for i in xrange(l):
    Y0[i][i] = 2*math.pi*freq * A0[i+l][i] 
    for j in xrange(i):
        Y0[i][j] = -2*math.pi*freq * A0[i+l][j]



#################################################
#################################################
####                                         ####
####   � � � � � �   � � � � � � � � � � �   ####
####                                         ####
#################################################
#################################################

print "OPTLC v." + VERSION, "- \"" + unicode(sys.argv[1], "CP1251").encode("CP866")  + "\""
print "����� -", l
print "�஧������� ��ᮢ -", w, "+", r 
print "����� �����(���⪠ �����) -", round(length,2), "��" 
print "����� ��६������ ⮪� -", round(freq,1), "��" 
print "����쭮� ᮯ�⨢����� ���� -", round(ro,1), "��*�" 
print "���������⭠� ��㡨�� �ᯮ������� ���⭮�� �஢��� � ����� -", int(Dearth), "�" 
print 
print "������������������������������������������������������������������������������Ŀ"
print "� ��ࠬ���� �奬� ����饭�� ��אַ�(���⭮�) ��᫥����⥫쭮��                �"
print "������������������������������������������������������������������������������Ĵ"
print "�  R, ��  �  X, ��  � B, ���� � ������������                                   �"
print "������������������������������������������������������������������������������Ĵ"
for i in xrange(l):
    print "�%9.3f�%9.3f�%9.3f� %-47s�" % (Z1[i].real*length, Z1[i].imag*length, Y1[i]*1E6*length, line[i]['name'])
print "��������������������������������������������������������������������������������"
print
print "������������������������������������������������������������������������������Ŀ"
print "� ��ࠬ���� �奬� ����饭�� �㫥��� ��᫥����⥫쭮�� (ᮡ�⢥���)           �"
print "������������������������������������������������������������������������������Ĵ"
print "�  R, ��  �  X, ��  � B, ���� � ������������                                   �"
print "������������������������������������������������������������������������������Ĵ"
for i in xrange(l):
    print "�%9.3f�%9.3f�%9.3f� %-47s�" % (Z0[i][i].real*length, Z0[i][i].imag*length, Y0[i][i]*1E6*length, line[i]['name'])
print "��������������������������������������������������������������������������������"
print
print "������������������������������������������������������������������������������Ŀ"
print "� ��ࠬ���� �奬� ����饭�� �㫥��� ��᫥����⥫쭮�� (�������)              �"
print "������������������������������������������������������������������������������Ĵ"
print "�  R, ��  �  X, ��  � B, ���� � ������������                                   �"
print "������������������������������������������������������������������������������Ĵ"
for i in xrange(l):
    for j in xrange(i):
        print "�%9.3f�%9.3f�%9.3f� %-47s�" % (Z0[i][j].real*length, Z0[i][j].imag*length, Y0[i][j]*1E6*length,"�> "+line[j]['name'])
        print "�         �         �         � %-47s�" % ( "�> "+line[i]['name'])
        if j < l-2:
            print "������������������������������������������������������������������������������Ĵ"

print "��������������������������������������������������������������������������������"
print
print
print "                                   * * *"
print
print "������������������������������������������������������������������������������Ŀ"
print "� ��室�� ��ࠬ���� �����                                                     �"
print "������������������������������������������������������������������������������Ĵ"
print "�   r,  �  k  �  d, � n �  a, � ������������                                   �"
print "� ��/�� �     �  �� �   �  �  �                                                �"
print "������������������������������������������������������������������������������Ĵ"
for i in xrange(l):
    if line[i]['n'] > 1:
        print "�%7.4f�%5.2f�%5.1f� %1d �%5.2f� %-47s�" % (line[i]['r'], line[i]['k'], line[i]['d'], line[i]['n'], line[i]['a'], line[i]['name'])
    else:
        print "�%7.4f�%5.2f�%5.1f� %1d �  -  � %-47s�" % (line[i]['r'], line[i]['k'], line[i]['d'], line[i]['n'],               line[i]['name'])
print "������������������������������������������������������������������������������Ĵ"
print "������������������������������������������������������������������������������Ĵ"
print "�   l,  �   f,  �  dX, �  dY, � ������������                                   �"
print "�   �   �   �   �   �  �   �  �                                                �"
print "������������������������������������������������������������������������������Ĵ"
for i in xrange(l):
    print "�%7.2f�%7.2f�%6.1f�%6.1f� %-47s�" % (line[i]['l'], line[i]['f'], line[i]['dX'], line[i]['dY'], line[i]['name'])
print "������������������������������������������������������������������������������Ĵ"
print "������������������������������������������������������������������������������Ĵ"
print "�  Xa, �  �  Xb, �  �  Xc, �  � ������������                                   �"
print "�  Ya, �  �  Yb, �  �  Yc, �  �                                                �"
print "������������������������������������������������������������������������������Ĵ"
for i in xrange(l):
    print "�%9.2f�%9.2f�%9.2f� %-47s�" % (line[i]['X'][0], line[i]['X'][1], line[i]['X'][2], line[i]['name'])
    print "�%9.2f�%9.2f�%9.2f� %-47s�" % (line[i]['Y'][0], line[i]['Y'][1], line[i]['Y'][2], "")
    if i < l-1:
        print "������������������������������������������������������������������������������Ĵ"
print "��������������������������������������������������������������������������������"
print
if w != 0 or r != 0:
    print "������������������������������������������������������������������������������Ŀ"
    print "� ��室�� ��ࠬ���� �஧������� ��ᮢ                                      �"
    print "������������������������������������������������������������������������������Ĵ"
    print "�  r, �*k;x,�  d, �  l, �  f, � ������������                                   �"
    print "���/�����/���  �� �  �  �  �  �                                                �"
    print "������������������������������������������������������������������������������Ĵ"
    for i in xrange(w):
        if 'k' in wire[i]:
            print "�%5.2f�*%4.2f�%5.1f�%5.1f�%5.1f� %-47s�" % (wire[i]['r'], wire[i]['k'], wire[i]['d'], wire[i]['l'], wire[i]['f'], "��� � " + str(i+1))
        else:
            print "�%5.2f�%5.2f�%5.1f�%5.1f�%5.1f� %-47s�" % (wire[i]['r'], wire[i]['x'], wire[i]['d'], wire[i]['l'], wire[i]['f'], "��� � " + str(i+1))
    for i in xrange(r):
        print "�  -  �  -  �%5.1f�%5.1f�%5.1f� %-47s�" % (rope[i]['d'], rope[i]['l'], rope[i]['f'], "��� � " + str(w+i+1))
    print "������������������������������������������������������������������������������Ĵ"
    print "������������������������������������������������������������������������������Ĵ"
    print "�   X,  �   Y,  �  dX, �  dY, � ������������                                   �"
    print "�   �   �   �   �   �  �   �  �                                                �"
    print "������������������������������������������������������������������������������Ĵ"
    for i in xrange(w):
        print "�%7.2f�%7.2f�%6.1f�%6.1f� %-47s�" % (wire[i]['X'][0], wire[i]['Y'][0], wire[i]['dX'], wire[i]['dY'], "��� � " + str(i+1))
    for i in xrange(r):
        print "�%7.2f�%7.2f�%6.1f�%6.1f� %-47s�" % (rope[i]['X'][0], rope[i]['Y'][0], rope[i]['dX'], rope[i]['dY'], "��� � " + str(w+i+1))
    print "��������������������������������������������������������������������������������"
