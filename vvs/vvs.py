from magneticcard import *

verbose = 0

t1_h = "A2DDBE77DD4204C8972154B52A040895F0408122F51B16284C8F92B42B312BE268E2D402FA2848A102158A11284020408102040810204081F950"
t1_i = "VVS^7003234255002^0001781103^26492^DB15 ^1010041020"


print "\n[VVS Verbundspass Tool]\n  v0.1 - smrrd & momo\n  decoding magnetic card\n\n"
print "[HEX String]\n  "+t1_h+"\n"
bits = create_h2b(t1_h)
print "[Bit String]\n  "+bits+"\n"
bytes = create_7bits(bits)
print "[Splitted]\n  "+str(bytes)+"\n"
iso,left = create_7bit2a(bytes)
print "[ASCII String]\n  "+iso+"\n  bits left: "+left
