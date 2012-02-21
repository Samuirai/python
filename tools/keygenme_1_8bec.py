# KeyGen for 8bec KeygenMe 1
# keygenme_8bec.exe

import sys

username = sys.argv[1]
name = username+username[0:2]

def fluttershy(b):
   d = b+0x2-0x21+0x2C
   d = d << 1
   return d
   
def reversed_fluttershy(b):
   d = b >> 1
   d = d-0x2+0x21-0x2C
   return d

a = len(username) * 0x778
b = len(name)
a = a + 0xb - 0x3 - 0x3 - 0x3 + 0x6 + 0x6 - 0x1 - 0x1
a = fluttershy(a)
a = a << 1

for c in name:
   a -= 1
   c = ord(c)+a+b
   b = c

print username+": "+str(reversed_fluttershy(fluttershy(b)))