# KeyGen for 8bec KeygenMe 2
# keygenme_8bec_2.exe
# usage: python keygenme_8bec_2.py <username>

import sys

a,b = 0,0
for c in sys.argv[1]:
    print c+" : "+str(hex(ord(c)))
    a = ord(c)+ord(c)+ord(c)
    a = a<<2
    a = a+ord(c)
    a = a | 0
    b = b + a
    
d = 0x55555556*b
d = 0xffffffff00000000&d
d = d>>32
b = b>>0x1f
d = d-b
print d
