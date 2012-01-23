from magneticcard import *

verbose = 0
t1_h = "A30F39335E8D7CC2"            #  ASDLOL?#
t1_h = "A3461E7266BD1AF987E2C0"      #  %ASDLOL?#?:
t1_h = "A3468C3CE4CD7A35F30FC59F16"  #  %%ASDLOL?#?:?:
t1_h = "A2DDBE77DD4204C8972154B52A040895F0408122F51B16284C8F92B42B312BE268E2D402FA2848A102158A11284020408102040810204081F950"

t2_i =     "70032342550020001781103=26492=101004"
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
print "  Preisstufe       "+info[1][3:5]
print "  Pass Nr          "+chr(int(info[1][0:2]))+" "+info[1][5:12]+"-"+info[1][12]
print "   ?               "+info[2][0:6]
print "  Gueltig bis      "+info[2][8:10]+"/"+info[2][6:8]
print "   ?               "+info[3]
print "  Verkaufsstelle   "+info[4]
print "  Ausstelldatum    "+info[5][4:6]+"."+info[5][2:4]+"."+info[5][0:2]
print "  Geltungsbereiche "+info[5][6:8]+" "+info[5][8:10]+" "+info[5][10:12]+" "+info[5][12:14]+" "+info[5][14:16]+" "+info[5][16:18]+" "+info[5][18:20]+" "+info[5][20:22]
print "   ?               "+info[5][22:]


track2 = {
		"FABI": "D7021CA324456A10A0210C38284039B21A49A2D00C02127F80",
		"MOMO": "D3441CE602AB7226F0210C09580433B4328E22C19860887CE0",
		"SAIJ": "D36A18211C2048DCF0210C32D08421B66799CEC1106B0CFE",
		"MARL": "D70816CF350CDA8990210C39382208B4E0815AD0806B0E7EC0"
	}

for key in track2:
	t2_h = track2[key]
	#print "\nTRACK 2 ("+key+"):\n[HEX String]\n  "+t2_h+"\n"
	bits = create_h2b(t2_h)
	#print "[Bit String]\n  "+bits+"\n"
	bytes = create_5bits(bits)
	#print "[Splitted]\n  "+str(bytes)+"\n"
	iso,left = create_5bit2a(bytes)
	#print "[ASCII String]\n  "+iso+"\n  bits left: "+left
	info = iso[1:].split('=')
	#print info
	print "\n[ "+key+" ]"
	print "  Preisstufe       "+info[0][3:5]
	print "  Pass Nr          "+chr(int(info[0][0:2]))+" "+info[0][5:12]+"-"+info[0][12]
	print "   ?               "+info[0][13:19]
	print "  Gueltig bis      "+info[0][21:23]+"/"+info[0][19:21]
	print "   ?               "+info[1]
	print "  Ausstelldatum    "+info[2][4:6]+"."+info[2][2:4]+"."+info[2][0:2]
	print "   ?               "+info[2][6:]