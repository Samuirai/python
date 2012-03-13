import sys
"""
1. check length
This is the first important asm part.
The function smrrd_strlen calculates the len of the string and continues if it is >=7

0040123E   .  68 98314000   PUSH 00403198                            ;  ASCII "samuirai"
00401243   .  E8 7AFFFFFF   CALL 004011C2                            ;  smrrd_strlen
00401248   .  83F9 07       CMP ECX,7
0040124B   .  73 02         JNB SHORT 0040124F
0040124D   .  C9            LEAVE
0040124E   .  C3            RET
0040124F   >  8D05 CD314000 LEA EAX,DWORD PTR DS:[4031CD]
00401255   .  8908          MOV DWORD PTR DS:[EAX],ECX
00401257   .  68 B0314000   PUSH 004031B0                            ;  ASCII "1234567"
0040125C   .  E8 61FFFFFF   CALL 004011C2                            ;  smrrd_strlen
00401261   .  83F9 07       CMP ECX,7
00401264   .  73 02         JNB SHORT 00401268
00401266   .  C9            LEAVE
00401267   .  C3            RET

"""
name = sys.argv[1]
if(len(name)<7):
    exit(-1)

"""

2. username scramble

The next Part is a loop over the username string 

00401268   > \33C9          XOR ECX,ECX                              ;  after len check set ECX = 0
....
00401271   > /8D45 FC       LEA EAX,DWORD PTR SS:[EBP-4]
00401274   . |33DB          XOR EBX,EBX
00401276   . |8D05 98314000 LEA EAX,DWORD PTR DS:[403198]            ;  ASCII "samuirai"
0040127C   . |8B1C01        MOV EBX,DWORD PTR DS:[ECX+EAX]           ;  EBX = *"samuirai" + ECX
0040127F   . |33D9          XOR EBX,ECX                              ;  BL = ascii nr of EBX (momentan charater) and XOR with ECX
00401281   . |03C1          ADD EAX,ECX                              ;  shift string to change momentan character
00401283   . |8818          MOV BYTE PTR DS:[EAX],BL                 ;  change the momentan character to the BL
00401285   . |8D05 98314000 LEA EAX,DWORD PTR DS:[403198]
0040128B   . |8B45 FC       MOV EAX,DWORD PTR SS:[EBP-4]
0040128E   . |41            INC ECX                                  ;  ECX++
0040128F   . |3B0A          CMP ECX,DWORD PTR DS:[EDX]
00401291   .^\7E DE         JLE SHORT 00401271

"""
ecx = 0
scrambled_name = ""
for c in name:
    ebx = ord(c) ^ ecx # XOR momentan character with ECX
    ecx +=1
    scrambled_name += chr(ebx)
    
print scrambled_name

"""

3. the virtual machine

This is the beginning of the virtual machine. It loads the next opcode from DWORD PTR DS:[ECX+403000]

00401357   > /8305 FF354000>ADD DWORD PTR DS:[4035FF],2     \__ ECX (Instruction Pointer) + 2
0040135E   $ |8B0D FF354000 MOV ECX,DWORD PTR DS:[4035FF]   /       
00401364   . |FFB1 00304000 PUSH DWORD PTR DS:[ECX+403000] |
0040136A   . |8F05 C8314000 POP DWORD PTR DS:[4031C8]       \__ Get and Start checking OP Code
00401370   . |803D C8314000>CMP BYTE PTR DS:[4031C8],0A     / 
....

which looks in the memory like this

00403000  0A 05 09 98  0C 03 0A 04
00403008  1C 01 11 00  0C 08 B0 00
00403010  1D 03 0B 02  0C 01 0D 02
00403018  88 00 1C 01  09 00 1B 01
00403020  FF FF 1D 01  0F 04 0F 04
00403028  0A 04 0E 01  0B 03 0F 01
00403030  0F 01 0A 05  BA 00 0B 02
00403038  0E 02 0E 02  0E 02 0F 02
00403040  1D 01 0B 03  1D 02 1C 01
00403048  22 00 0A 03  0B 02 1D 01
00403050  FF 


00403000  0A 05 09 98  0C 03 0A 04 
00403008  1C 01 11 00  0C 08 B0 00 
00403010  1D 03 0B 02  0C 01 0D 02 
00403018  88 00 1C 01  09 00 1B 01 
00403020  FF FF 1D 01  0F 04 0F 04 
00403028  0A 04 0E 01  0B 03 0F 01 
00403030  0F 01 0A 05  BA 00 0B 02
00403038  0E 02 0E 02  0E 02 0F 02  
00403040  1D 01 0B 03  1D 02 1C 01
00403048  22 00 0A 03  0B 02 1D 01
00403050  FF 



ECX is used as the IP (DWORD PTR DS:[ECX+403000])
If an Opcode is read and recognized ECX is Incremented

Here the beginning of the OP Code decoding 0A
00401370   .  803D C8314000> CMP BYTE PTR DS:[4031C8],0A     ; check if opcode is 0x0A
00401377   .  75 76          JNZ SHORT 004013EF
00401379   .  41             INC ECX                         ; ECX++ -> points to parameter now
0040137A   .  FFB1 00304000  PUSH DWORD PTR DS:[ECX+403000]  
00401380   .  8F05 C8314000  POP DWORD PTR DS:[4031C8]
00401386   .  803D C8314000> CMP BYTE PTR DS:[4031C8],1      ; Check if Parameter is 0x01
0040138D   .  75 0C          JNZ SHORT 0040139B
0040138F   .  68 CF354000    PUSH 004035CF                   ; Push some stuff
00401394   .  E8 79040000    CALL 00401812                   ; Call the Function for 0x0A
00401399   .  EB 4F          JMP SHORT 004013EA
0040139B   >  803D C8314000> CMP BYTE PTR DS:[4031C8],2      ; Check if Parameter is 0x02
004013A2   .  75 0C          JNZ SHORT 004013B0
004013A4   .  68 D7354000    PUSH 004035D7                   ; Push some stuff
004013A9   .  E8 64040000    CALL 00401812                   ; Call the Function for 0x0A
004013AE   .  EB 3A          JMP SHORT 004013EA              ; Jump back to beginning of OP Code Decoding
...

extractet is vm code this:



00401370   .  803D C8314000> CMP BYTE PTR DS:[4031C8],0A     ; check if opcode is 0x0A
00401377   .  75 76          JNZ SHORT 004013EF
00401379   .  41             INC ECX                         ; ECX++ -> points to parameter now
0040137A   .  FFB1 00304000  PUSH DWORD PTR DS:[ECX+403000]  
00401380   .  8F05 C8314000  POP DWORD PTR DS:[4031C8]
00401386   .  803D C8314000> CMP BYTE PTR DS:[4031C8],1      ; Check if Parameter is 0x01
0040138D   .  75 0C          JNZ SHORT 0040139B
0040138F   .  68 CF354000    PUSH 004035CF                   ; Push some stuff

---------------------------------------------------------------------

[4031C8] :=                                 |  OP_CODE
[4031CF] := REGISTER_1 (?) 0x00 start Wert
[4035EF] := REGISTER_2 (?) 0x2E start Wert
[4035FF] := REGISTER_3 (?) 0x00 start Wert  |  Instruction Pointer
[4031C9] := REGISTER_4 (?) 0x09 start Wert

"""

smrrd = dict()
smrrd[0x4031C8] = 0x0A # OP Code
smrrd[0x4031C9] = 0x05
smrrd[0x4031CF] = 0x00
smrrd[0x4031F5] = 0x00
smrrd[0x4031F9] = 0x00
smrrd[0x4035CF] = 0x00
smrrd[0x4035D7] = 0x00
smrrd[0x4035E7] = 0x00
smrrd[0x4035EF] = 0x32
smrrd[0x4035FF] = 0x00 # ip
eax = 0x00
ebx = 0x00
ecx = 0x00
edx = 0x00

"""

---------------------------------------------------------------------

0x0A:

00401812  /$  55            PUSH EBP
00401813  |.  8BEC          MOV EBP,ESP
00401815  |.  832D EF354000>SUB DWORD PTR DS:[4035EF],4     ; [4035EF]-4
0040181C  |.  8D1D CF314000 LEA EBX,DWORD PTR DS:[4031CF]
00401822  |.  031D EF354000 ADD EBX,DWORD PTR DS:[4035EF]
00401828  |.  8B4D 08       MOV ECX,DWORD PTR SS:[EBP+8]    ; get the earlier pushed Parameter
0040182B  |.  0BC9          OR ECX,ECX                      ; OR Parameter
0040182D  |.  75 0F         JNZ SHORT 0040183E              ; Jump if OR Test was not zero
0040182F  |.  8B0D C9314000 MOV ECX,DWORD PTR DS:[4031C9]   
00401835  |.  8305 FF354000>ADD DWORD PTR DS:[4035FF],2     ; [4035FF]+2 | Instruction Pointer
0040183C  |.  EB 05         JMP SHORT 00401843
0040183E  |>  8B55 08       MOV EDX,DWORD PTR SS:[EBP+8]
00401841  |.  8B0A          MOV ECX,DWORD PTR DS:[EDX]
00401843  |>  66:890B       MOV WORD PTR DS:[EBX],CX
00401846  |.  C9            LEAVE
00401847  \.  C2 0400       RET 4
"""


def smrrd_0x0A(param):
    smrrd[0x4035EF] -= 4
    ebx = smrrd[0x4031CF]
    ebx += smrrd[0x4035EF]
    ecx = param
    if not ecx:
        ecx = smrrd[0x4031C9]
        smrrd[0x4035FF] += 0x02
    else:
        edx = param
        ecx = smrrd[edx]
        smrrd[ebx] = ecx

"""

0X0B:

0040184A  /$  55            PUSH EBP
0040184B  |.  8BEC          MOV EBP,ESP
0040184D  |.  33C9          XOR ECX,ECX
0040184F  |.  8D1D CF314000 LEA EBX,DWORD PTR DS:[4031CF]
00401855  |.  031D EF354000 ADD EBX,DWORD PTR DS:[4035EF]
0040185B  |.  8B45 08       MOV EAX,DWORD PTR SS:[EBP+8]
0040185E  |.  FF33          PUSH DWORD PTR DS:[EBX]
00401860  |.  8F00          POP DWORD PTR DS:[EAX]
00401862  |.  890B          MOV DWORD PTR DS:[EBX],ECX
00401864  |.  8305 EF354000>ADD DWORD PTR DS:[4035EF],4
0040186B  |.  F7E1          MUL ECX
0040186D  |.  C9            LEAVE
0040186E  \.  C2 0400       RET 4

"""

def smrrd_0x0B(param):
    ecx = 0x00
    ebx = 0x4031CF # smrrd[0x4031CF]
    ebx += smrrd[0x4035EF]
    eax = param
    smrrd[eax] = smrrd[ebx]
    smrrd[ebx] = ecx
    smrrd[0x4035EF] += 4
    eax *= ecx
    

"""

0x0C:

00401871  /$  55             PUSH EBP
00401872  |.  8BEC           MOV EBP,ESP
00401874  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
00401877  |.  8B55 0C        MOV EDX,DWORD PTR SS:[EBP+C]
0040187A  |.  837D 0C 00     CMP DWORD PTR SS:[EBP+C],0
0040187E  |.  75 0F          JNZ SHORT 0040188F
00401880  |.  8B1D C9314000  MOV EBX,DWORD PTR DS:[4031C9]
00401886  |.  8305 FF354000 >ADD DWORD PTR DS:[4035FF],2
0040188D  |.  EB 02          JMP SHORT 00401891
0040188F  |>  8B1A           MOV EBX,DWORD PTR DS:[EDX]
00401891  |>  66:8918        MOV WORD PTR DS:[EAX],BX
00401894  |.  C9             LEAVE
00401895  \.  C2 0800        RET 8

"""

def smrrd_0x0C(param2,param1):
    eax = param1
    edx = param2
    if param2 == 0x00:
        ebx = smrrd[0x4031C9]
        smrrd[0x4035FF] += 0x02
    else:
        ebx = smrrd[edx]
    smrrd[eax] = ebx

"""


0x0D:

00401A03  /$  55             PUSH EBP
00401A04  |.  8BEC           MOV EBP,ESP
00401A06  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
00401A09  |.  8B5D 0C        MOV EBX,DWORD PTR SS:[EBP+C]
00401A0C  |.  837D 0C 00     CMP DWORD PTR SS:[EBP+C],0
00401A10  |.  75 1C          JNZ SHORT 00401A2E
00401A12  |.  33DB           XOR EBX,EBX
00401A14  |.  8B0D FF354000  MOV ECX,DWORD PTR DS:[4035FF] --
00401A1A  |.  8B1D C9314000  MOV EBX,DWORD PTR DS:[4031C9]
00401A20  |.  8305 FF354000 >ADD DWORD PTR DS:[4035FF],1
00401A27  |.  8305 FF354000 >ADD DWORD PTR DS:[4035FF],1
00401A2E  |>  66:3BC3        CMP AX,BX
00401A31  |.  7C 04          JL SHORT 00401A37
00401A33  |.  7F 14          JG SHORT 00401A49
00401A35  |.  74 24          JE SHORT 00401A5B
00401A37  |>  C605 0F364000 >MOV BYTE PTR DS:[40360F],1
00401A3E  |.  C605 10364000 >MOV BYTE PTR DS:[403610],0
00401A45  |.  C9             LEAVE
00401A46  |.  C2 0800        RET 8
00401A49  |>  C605 0F364000 >MOV BYTE PTR DS:[40360F],0
00401A50  |.  C605 10364000 >MOV BYTE PTR DS:[403610],0
00401A57  |.  C9             LEAVE
00401A58  |.  C2 0800        RET 8
00401A5B  |>  C605 0F364000 >MOV BYTE PTR DS:[40360F],0
00401A62  |.  C605 10364000 >MOV BYTE PTR DS:[403610],1
00401A69  |.  C9             LEAVE
00401A6A  \.  C2 0800        RET 8


"""

def smrrd_0x0D(param2,param1):
    eax = param1
    ebx = param2
    if param2 == 0:
        ebx = 0x00
        ecx = smrrd[0x4035FF]
        ebx = smrrd[0x4031C9]
        smrrd[0x4035FF] += 1
        smrrd[0x4035FF] += 1
    if eax < ebx:
        smrrd[0x40360F] = 1
        smrrd[0x403610] = 0
    if eax > ebx:
        smrrd[0x40360F] = 1
        smrrd[0x403610] = 0
    if eax == ebx:
        smrrd[0x40360F] = 1
        smrrd[0x403610] = 0

"""

0x0E:

00401898  /$  55             PUSH EBP
00401899  |.  8BEC           MOV EBP,ESP
0040189B  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
0040189E  |.  8B18           MOV EBX,DWORD PTR DS:[EAX]
004018A0  |.  43             INC EBX
004018A1  |.  8918           MOV DWORD PTR DS:[EAX],EBX
004018A3  |.  C9             LEAVE
004018A4  \.  C2 0400        RET 4

"""

def smrrd_0x0E(param1):
    eax = param1
    ebx = smrrd[eax]
    ebx += 1
    smrrd[eax] = ebx
    
"""

0x0F

004018A7  /$  55             PUSH EBP
004018A8  |.  8BEC           MOV EBP,ESP
004018AA  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
004018AD  |.  8B18           MOV EBX,DWORD PTR DS:[EAX]
004018AF  |.  4B             DEC EBX
004018B0  |.  8918           MOV DWORD PTR DS:[EAX],EBX
004018B2  |.  C9             LEAVE
004018B3  \.  C2 0400        RET 4

"""

def smrrd_0x0F(param1):
    eax = param1
    ebx = smrrd[eax]
    ebx -= 1
    smrrd[eax] = ebx

"""

0x1B

004018B6  /$  55             PUSH EBP
004018B7  |.  8BEC           MOV EBP,ESP
004018B9  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
004018BC  |.  8B18           MOV EBX,DWORD PTR DS:[EAX]
004018BE  |.  8B0D C9314000  MOV ECX,DWORD PTR DS:[4031C9]
004018C4  |.  8305 FF354000 >ADD DWORD PTR DS:[4035FF],2
004018CB  |.  66:23D9        AND BX,CX
004018CE  |.  66:8918        MOV WORD PTR DS:[EAX],BX
004018D1  |.  C9             LEAVE
004018D2  \.  C2 0800        RET 8

"""

def smrrd_0x1B(param1):
    eax = param1
    ebx = smrrd[eax]
    ecx = smrrd[0x4031C9]
    smrrd[0x4035FF] += 2
    ebx &= ecx
    smrrd[eax] = ebx

"""

0x1C

004018D5  /$  55             PUSH EBP
004018D6  |.  8BEC           MOV EBP,ESP
004018D8  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
004018DB  |.  8B18           MOV EBX,DWORD PTR DS:[EAX]
004018DD  |.  8B0D C9314000  MOV ECX,DWORD PTR DS:[4031C9]
004018E3  |.  8305 FF354000 >ADD DWORD PTR DS:[4035FF],2
004018EA  |.  66:0BD9        OR BX,CX
004018ED  |.  8918           MOV DWORD PTR DS:[EAX],EBX
004018EF  |.  C9             LEAVE
004018F0  \.  C2 0800        RET 8

"""

def smrrd_0x1C(param1):
    eax = param1
    ebx = smrrd[eax]
    ecx = smrrd[0x4031C9]
    smrrd[0x4035FF] += 2
    ebx |= ecx
    smrrd[eax] = ebx

"""

0x1D

004018F3  /$  55             PUSH EBP
004018F4  |.  8BEC           MOV EBP,ESP
004018F6  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
004018F9  |.  8B5D 0C        MOV EBX,DWORD PTR SS:[EBP+C]
004018FC  |.  837D 0C 00     CMP DWORD PTR SS:[EBP+C],0
00401900  |.  75 0D          JNZ SHORT 0040190F
00401902  |.  8B1D C9314000  MOV EBX,DWORD PTR DS:[4031C9]
00401908  |.  8305 FF354000 >ADD DWORD PTR DS:[4035FF],2
0040190F  |>  33C3           XOR EAX,EBX
00401911  |.  8705 CF354000  XCHG DWORD PTR DS:[4035CF],EAX
00401917  |.  C9             LEAVE
00401918  \.  C2 0800        RET 8

"""

def smrrd_0x1D(param2,param1):
    eax = param1
    ebx = param2
    if param2 == 0:
        ebx = smrrd[0x4031C9]
        smrrd[0x4035FF] += 2
    eax ^= ebx
    smrrd[0x4035CF],eax = eax,smrrd[0x4035CF]

"""

0x1E

00401981  /$  55             PUSH EBP
00401982  |.  8BEC           MOV EBP,ESP
00401984  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
00401987  |.  0105 FF354000  ADD DWORD PTR DS:[4035FF],EAX
0040198D  |.  C9             LEAVE
0040198E  \.  C2 0400        RET 4

00401991  /$  55             PUSH EBP
00401992  |.  8BEC           MOV EBP,ESP
00401994  |.  803D 10364000 >CMP BYTE PTR DS:[403610],1
0040199B  |.  75 09          JNZ SHORT 004019A6
0040199D  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
004019A0  |.  0105 FF354000  ADD DWORD PTR DS:[4035FF],EAX
004019A6  |>  8305 FF354000 >ADD DWORD PTR DS:[4035FF],1
004019AD  |.  C9             LEAVE
004019AE  \.  C2 0400        RET 4

004019B1  /$  55             PUSH EBP
004019B2  |.  8BEC           MOV EBP,ESP
004019B4  |.  803D 10364000 >CMP BYTE PTR DS:[403610],0
004019BB  |.  75 12          JNZ SHORT 004019CF
004019BD  |.  803D 0F364000 >CMP BYTE PTR DS:[40360F],1
004019C4  |.  75 09          JNZ SHORT 004019CF
004019C6  |.  8B45 08        MOV EAX,DWORD PTR SS:[EBP+8]
004019C9  |.  0105 FF354000  ADD DWORD PTR DS:[4035FF],EAX
004019CF  |>  8305 FF354000 >ADD DWORD PTR DS:[4035FF],1
004019D6  |.  C9             LEAVE
004019D7  \.  C2 0400        RET 4

"""

def smrrd_0x1E(param1):
    pass

"""
0xFF: 

ENDE

"""

def info_registers():
    #print 'eax',hex(eax)
    #print 'ebx',hex(ebx)
    #print 'ecx:',hex(ecx)
    #print hex(0x4031C8),hex(smrrd[0x4031C8])
    #print hex(0x4031CF),hex(smrrd[0x4031CF])
    #print hex(0x4035EF),hex(smrrd[0x4035EF])
    #print hex(0x4035FF),hex(smrrd[0x4035FF])
    #print hex(0x4031C9),hex(smrrd[0x4031C9])
    #print hex(0x4035D7),hex(smrrd[0x4035D7])
    print hex(0x4035CF),hex(smrrd[0x4035CF])
    print hex(0x4035DF),hex(smrrd[0x4035DF])
    print hex(0x4035EF),hex(smrrd[0x4035EF])
    #print 'memory:\n',smrrd


info_registers()

code = "0A 05 09 98 0C 03 0A 04 1C 01 11 00 0C 08 B0 00 1D 03 0B 02 0C 01 0D 02 88 00 1C 01 09 00 1B 01 FF FF 1D 01 0F 04 0F 04 0A 04 0E 01 0B 03 0F 01 0F 01 0A 05 BA 00 0B 02 0E 02 0E 02 0E 02 0F 02 1D 01 0B 03 1D 02 1C 01 22 00 0A 03 0B 02 1D 01 FF".split(' ')
print code,len(code)
c = code[smrrd[0x4035FF]]



while c!='FF':
    
    
    c = code[smrrd[0x4035FF]]
    print smrrd[0x4035FF],'(',c,')'
    print "-----------------"
    info_registers()
    print '\n'
    #print c,smrrd[0x4035FF],hex(smrrd[0x4035EF])
    smrrd[0x4031C8] = int(code[smrrd[0x4035FF]],16)
    
    if c=='0A':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x0A(0x004035CF)
        elif smrrd[0x4031C8] == 0x02:
            smrrd_0x0A(0x004035D7)
        elif smrrd[0x4031C8] == 0x03:
            smrrd_0x0A(0x004035DF)
        elif smrrd[0x4031C8] == 0x04:
            smrrd_0x0A(0x004035E7)
        elif smrrd[0x4031C8] == 0x05:
            smrrd_0x0A(0x00000000)        
            
            
    elif c=='0B':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x0B(0x004035CF)
        elif smrrd[0x4031C8] == 0x02:
            smrrd_0x0B(0x004035D7)
        elif smrrd[0x4031C8] == 0x03:
            smrrd_0x0B(0x004035DF)
        elif smrrd[0x4031C8] == 0x04:
            smrrd_0x0B(0x004035E7)
            
            
    elif c=='0C':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x0C(0x004035D7,0x004035CF)
        elif smrrd[0x4031C8] == 0x02:
            smrrd_0x0C(0x004035DF,0x004035CF)
        elif smrrd[0x4031C8] == 0x03:
            smrrd_0x0C(0x004035E7,0x004035CF)
        elif smrrd[0x4031C8] == 0x06:
            smrrd_0x0C(0x00000000,0x004035CF)
        elif smrrd[0x4031C8] == 0x07:
            smrrd_0x0C(0x00000000,0x004035D7)
        elif smrrd[0x4031C8] == 0x08:
            smrrd_0x0C(0x00000000,0x004035DF)
            

    elif c=='0D':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x0D(smrrd[0x004035D7],smrrd[0x004035CF])
        elif smrrd[0x4031C8] == 0x02:
            smrrd_0x0D(0x00000000,smrrd[0x004035CF])
        elif smrrd[0x4031C8] == 0x03:
            smrrd_0x0D(0x00000000,smrrd[0x004035D7])
        elif smrrd[0x4031C8] == 0x04:
            smrrd_0x0D(0x00000000,smrrd[0x004035DF])
        elif smrrd[0x4031C8] == 0x05:
            smrrd_0x0D(0x00000000,smrrd[0x004035E7])
            
            
    elif c=='0E':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x0E(0x004035CF)
        elif smrrd[0x4031C8] == 0x02:
            smrrd_0x0E(0x004035D7)
        elif smrrd[0x4031C8] == 0x03:
            smrrd_0x0E(0x004035DF)
        elif smrrd[0x4031C8] == 0x04:
            smrrd_0x0E(0x004035E7)


            
    elif c=='0F':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x0F(0x004035CF)
        elif smrrd[0x4031C8] == 0x02:
            smrrd_0x0F(0x004035D7)
        elif smrrd[0x4031C8] == 0x03:
            smrrd_0x0F(0x004035DF)
        elif smrrd[0x4031C8] == 0x04:
            smrrd_0x0F(0x004035E7)
            


    elif c=='1B':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x1B(0x004035CF)
        
        
        
    elif c=='1C':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x1C(0x004035CF)
        
        
    elif c=='1D':
        smrrd[0x4031C8] = int(code[smrrd[0x4035FF]+1],16)
        if smrrd[0x4031C8] == 0x01:
            smrrd_0x1D(smrrd[0x004035D7],smrrd[0x004035CF])
        elif smrrd[0x4031C8] == 0x02:
            smrrd_0x1D(smrrd[0x004035D7],smrrd[0x004035CF])
        elif smrrd[0x4031C8] == 0x03:
            smrrd_0x1D(smrrd[0x004035D7],smrrd[0x004035CF])
        elif smrrd[0x4031C8] == 0x04:
            smrrd_0x1D(smrrd[0x004035D7],smrrd[0x004035CF])
        
        
    else:
        print "unknown OP Code"
    smrrd[0x4035FF] += 2
    

info_registers()

"""

4. The compare

0040191B  /$  A1 CF354000    MOV EAX,DWORD PTR DS:[4035CF]
00401920  |.  3C 21          CMP AL,21
00401922  |.  73 02          JNB SHORT 00401926
00401924  |.  04 21          ADD AL,21
00401926  |>  8D1D B0314000  LEA EBX,DWORD PTR DS:[4031B0]
0040192C  |.  8A0D CC314000  MOV CL,BYTE PTR DS:[4031CC]
00401932  |.  8A1419         MOV DL,BYTE PTR DS:[ECX+EBX]
00401935  |.  38D0           CMP AL,DL
00401937  |.  74 19          JE SHORT 00401952

[4035CF] 
[4031B0]
[4031CC]

"""