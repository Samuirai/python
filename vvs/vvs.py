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
info = iso[1:].split('^')

print "\n[Verbundspass Info]"
print "  Prefix           "+info[0]
print "   ?               "+info[1][0:3]
print "  Preisstufe       "+info[1][3:5]
print "  Pass Nr          "+info[1][5:12]+"-"+info[1][12]
print "   ?               "+info[2][0:6]
print "  Gueltig bis      "+info[2][8:10]+"/"+info[2][6:8]
print "   ?               "+info[3]
print "  Verkaufsstelle   "+info[4]
print "  Ausstelldatum    "+info[5][4:6]+"."+info[5][2:4]+"."+info[5][0:2]
print "  Geltungsbereiche "+info[5][6:8]+" "+info[5][8:10]+" "+info[5][10:12]+" "+info[5][12:14]+" "+info[5][14:16]+" "+info[5][16:18]+" "+info[5][18:20]+" "+info[5][20:22]+" "+info[5][22:24]+" "+info[5][24:26]