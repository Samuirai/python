# KeyGen for 8bec KeygenMe 3
# Maths.exe
# usage: python keygenme_8bec_3.py <username>

import sys

name = sys.argv[1]

def smrrd_char_fun(c):
    ebp_c = 0x00
    ebp_8 = 0x20
    eax,edx = 0,0
    while ebp_8 < 0x176F:
        ebp_c = 0x00
        add = 0x01
        eax = 0
        while ebp_c < 0x176F:
            eax += add
            add += 2
            edx = ord(c)**2
            edx += ebp_8**2
            if eax==edx:
                #print hex(edx),"==",hex(eax)
                eax = ebp_c
                ebp_10 = eax
                return (eax + 0x01)
            else:
                ebp_c += 0x01
        ebp_8 += 0x01
        
smrrd_char_fun('s')
print "start calculating pythagoras triangle"
smrrd_erg = [0x115,0x1261,0x1735,0x7d,0x6f,0xbe,0x1261,0x6f]
smrrd_erg = []
for c in name:
    x = smrrd_char_fun(c)
    smrrd_erg.append(x)

print "start calculating password"
smrrd_sum = 0x00
smrrd_counter = 0x00
for erg in smrrd_erg:
    if smrrd_counter%2==0:
        eax = int(smrrd_erg[smrrd_counter])+int(smrrd_erg[smrrd_counter+1])
        smrrd_sum += eax
    else:
        smrrd_sum *= 2
        smrrd_sum += 0x13 + 0x0b + 0x0d
    smrrd_counter += 1
    print ""
    
print "password: "+str(smrrd_sum)