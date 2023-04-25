#!/usr/bin/env python
# -*- coding: CP866 -*-
# (c) ����ॢ �.�. 2022
# �ணࠬ�� ��� �����
# �����筮� ���ᨬ��ਨ
# �� �� 34.20.179
# (�� 34-70-070-87) 

import pyexpat
import sys
import math
import string

VERSION = "1.0"

if len(sys.argv) == 1 :
    print "ONTLC v." + VERSION, "(c) ����ॢ �.�."
    print "�ᯮ���� : [python] ./ontlc.py <xml-file>"
    sys.exit()


xmlfile = open(sys.argv[1], "r")

############################
# �������᪠� ����ﭭ�� #
############################
eps0 = 8.85418781762039E-12
a    = -0.5+math.sqrt(3.)*0.5j

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
m = 3*l + w + r # ��饥 ������⢮ �஢���� � ��ᮢ



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

def LUM(M, L, U, a=None, b=None):
    m = len(M)
    n = m
    if a != None and b != None:
        n -= 1
    for i in xrange(n):
        for j in xrange(i+1,n):
            L[i][j] = 0.0
            U[i][j] = 0.0
        U[i][i] = 1.0
    for i in xrange(n):
        ii = i + (0,1)[i>=a and a != None]
        for j in xrange(n):
            jj = j + (0,1)[j>=b and b != None]
            s = 0
            if i >= j:
                for k in xrange(j):
                    s = s + L[i][k]*U[k][j]
                L[i][j] = M[ii][jj] - s
            else:
                for k in xrange(i):
                    s = s + L[i][k] * U[k][j]
                U[i][j] = (1/L[i][i]) * (M[ii][jj] - s)
    return

def det(L, U, n):
    dotL = 1
    dotU = 1
    for i in xrange(n):
        dotL = dotL*L[i][i]
        dotU = dotU*U[i][i]
    return (dotL*dotU)


#######################################################################
#######################################################################
####                                                               ####
####   � � � � � �   � � � � � � � � � �   � � � � � � � � � � �   ####
####                                                               ####
#######################################################################
#######################################################################

#######################################
# ����������� ࠤ��� �஢���(���) #
#######################################
R = vector(m)
for i in xrange(l):
    li = line[i]
    Rp = li['d'] / 2000.
    if li['n'] > 1:
        Rp = (Rp * li['a']**(li['n']-1))** (1./li['n'])
    for j in xrange(3):
        R[3*i+j] = Rp

for i in xrange(3*l, 3*l+w):
    R[i] = wire[i-3*l]['d'] / 2000. 

for i in xrange(3*l+w, m):
    R[i] = rope[i-3*l-w]['d']/2000.


###############################
# ���न���� �஢����(��ᮢ) #
###############################
X = vector(m)
Y = vector(m)
for i in xrange(l):
    li = line[i]
    for j in xrange(3): 
        X[3*i+j] = li['X'][j] + li['dX']
        Y[3*i+j] = li['Y'][j] + li['dY'] - li['l'] - 2./3.*li['f']

for i in xrange(3*l, 3*l+w):
    wi = wire[i-3*l]
    X[i] = wi['X'][0] + wi['dX'] 
    Y[i] = wi['Y'][0] + wi['dY'] - wi['l'] - 2./3.*wi['f']

for i in xrange(3*l+w, m):
    ri = rope[i-3*l-w]
    X[i] = ri['X'][0] + ri['dX'] 
    Y[i] = ri['Y'][0] + ri['dY'] - ri['l'] - 2./3.*ri['f']
 

#################################
# ������������ �஢����(��ᮢ) #
#################################
color = [" (�)", " (�)", " (�)"]
N = vector(m)
for i in xrange(l):
    li = line[i]
    for j in xrange(3): 
        N[3*i+j] = "   C"+str(3*i+j+1) + color[j]

for i in xrange(3*l, 3*l+w):
    N[i] = "�-"+str(i-3*l+1)

for i in xrange(3*l+w, m):
    N[i] = "�-"+str(i-3*l+1)

#######################################
# ����� ��⥭樠���� �����樥�⮢ #
#######################################
A = matrix(m)
K = 1 / (2.0 * math.pi * eps0)
for i in xrange(m):
    A[i][i] = K * math.log( 2.0*Y[i] / R[i] )
    for j in xrange(i+1,m):
        h   = math.sqrt( (X[i]-X[j])**2 + (Y[i]+Y[j])**2 )
        hyp = math.sqrt( (X[i]-X[j])**2 + (Y[i]-Y[j])**2 )
        A[i][j] = K * math.log( h / hyp )
        A[j][i] = A[i][j]


####################################################
# ��।���⥫� ������ ��⥭樠���� �����樥�⮢ #
# � ����� ᮡᢥ���� � ������� 񬪮�⥩          #
####################################################
L = matrix(m)
U = matrix(m)
C = matrix(m)

LUM(A, L, U)
detA = det(L, U, m)

for i in xrange(m):
    for j in xrange(m):
        LUM(A, L, U, i, j)
        C[i][j] = (-1)**(i+j) * det(L, U, m-1) / detA


###########################
# ������ �஢����/��ᮢ #
###########################
CF = vector(m)
for i in xrange(m):
    for j in xrange(m):
        CF[i] += C[i][j]

#################################################
#################################################
####                                         ####
####   � � � � � �   � � � � � � � � � � �   ####
####                                         ####
#################################################
#################################################

print "ONTLC v." + VERSION, "- \"" + unicode(sys.argv[1], "CP1251").encode("CP866")  + "\""
print "����� -", l
print "�஧������� ��ᮢ -", w, "+", r 
print 
print "������������������������������������������������������������������������������Ŀ"
print "�   �⥯��� ���ᨬ���ਨ � 㤥��� 񬪮�⭮� ⮪ �� 䠧��� ����殮��� 1 ��   �"
print "������������������������������������������������������������������������������Ĵ"
print "� ������祭�� � �o, ���/�� � ������������     �    U��/�,�    � Ic=3wC��, �/�� �"
print "������������������������������������������������������������������������������Ĵ"
for i in xrange(l):                                     
    print "�%-13s�%10.6f  � %-50s�" % (N[3*i  ], CF[3*i  ]*1E9, ""             )
    print "�%-13s�%10.6f  � %-50s�" % (N[3*i+1], CF[3*i+1]*1E9, line[i]['name'])
    print "�%-13s�%10.6f  � %-50s�" % (N[3*i+2], CF[3*i+2]*1E9, ""             )
    print "� � � � � � � � � � � � � ��� � � � � � � � � � � � � � � � � �� � � � � � � � �"
    Csum = 0.0
    for j in xrange(3):
        Csum += CF[3*i+j]                             
    Cavg  = Csum/3.
    Uns   = (CF[3*i] + a*(a*CF[3*i+1]+CF[3*i+2]))/Csum
    PHIns = math.atan2(Uns.imag, Uns.real)/math.pi*180.
    if PHIns < 0.0:
       PHIns += 360.0
    Ic = 6.0*freq*math.pi*Cavg
    print "�%-13s�%10.6f  �                  �%7.4f/%-6.2f �%12.6f    � " % ("    ���", Cavg*1E9, abs(Uns), PHIns, Ic*1E6)
    if i < l-1:
        print "������������������������������������������������������������������������������Ĵ"
print "��������������������������������������������������������������������������������"
print
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
