import sys, random
import socket 
import string 
import time
import os #not necassary but later on I am going to use a few features from this
import ptd_info
from ptd import smrrd_PTD
charset = "abcdefghijklmnopqrstuvwxyz"
nick = ''
for i in xrange(0,random.randint(3,10)):
    
    nick += charset[random.randint(0,len(charset))]
    
#nick = "poke_god"
HOST='irc.nixtrixirc.net' #The server we want to connect to 
PORT=6667 #The connection port which is usually 6667 
NICK=nick  #The bot's nickname 
IDENT=nick 
REALNAME='smrrd bot' 
OWNER='smrrd' #The bot owner's nick 
CHANNELINIT='#sdc-poketd' #  sdc-poketd  The default channel for the bot 
readbuffer='' #Here we store all the messages from server 

s=socket.socket( )
s.connect((HOST, PORT))

s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
#s.send('JOIN '+CHANNELINIT+'n') #Join a channel 

joined=False
last_anounce = 0

wishes = 100

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        
        if len(line)>0:
            print line

        if(line[0]=="PING"):
            s.send("PONG %s\r\n" % line[1])
        if(line[1]=="MODE" and line[2]==NICK):
            print "LOGGED IN"
            s.send('JOIN '+CHANNELINIT+'\r\n') #Join a channel
            joined = True
            
        if joined and last_anounce<time.time()-60:
            s.send('PRIVMSG '+CHANNELINIT+' Hello Trainer! I\'m the god of all Pokemon... You have '+str(wishes)+' wishes left. Write "help me god of all pokemon" if you want to know more. (.)(.)\n\r')
            last_anounce = time.time()
        # [':smrrd!M...', 'PRIVMSG', 'smrrd_bot', ':info', 'poke1@smrrd.e', 'asd']
        
        if len(line)>8:
            if line[1]=='PRIVMSG' and line[3]==':help' and line[4]=='me' and line[5]=='god' and line[6]=='of' and line[7]=='all' and line[8]=='pokemon':
                s.send('PRIVMSG '+CHANNELINIT+' Hello Trainer! I\'m the Pokemon god and I you have '+str(wishes)+' wishes left...\n\r')
                s.send('PRIVMSG '+CHANNELINIT+' write /msg '+nick+' catch <pokemon num> <level> <reg|shiny> <email> <pw>\n\r')
                s.send('PRIVMSG '+CHANNELINIT+' for example: /msg '+nick+' catch 1 100 reg asd@asd.de mypass\n\r')
                s.send('PRIVMSG '+CHANNELINIT+' to check your account you can write /msg '+nick+' acc <email> <pw>\n\r')
        # [':smrrd!Mibbit@Nix-FBC765F2.informatik.ba-stuttgart.de', 'PRIVMSG', 'pokemon_god', ':catch', '1', '2', 'reg', 'less@asd.de', 'asd']
        if wishes>0:
            if len(line)>8:
                if line[3]==':catch':
                    s.send('PRIVMSG '+CHANNELINIT+' Ok. Let me check your wish...\n\r')
                    num = int(line[4])
                    lvl = int(line[5])
                    shiny = line[6]
                    email = line[7]
                    pw = line [8]
                    ptd = smrrd_PTD(email=email,password=pw,version='650',aes_key='lkafd8halkf',verbose_lvl=1)
                    if len(ptd.login())>100:
                        s.send('PRIVMSG '+CHANNELINIT+' Good news! I found your account int the Hall of Pokemon TD Trainers! Give me just a second...\n\r')
                        msg = ''
                        if shiny == 'reg' or shiny == 'regular':
                            msg = ptd.catch(num=num,lvl=lvl, shiny=False)
                        if shiny == 'shiny' or shiny == 'shine':
                            msg = ptd.catch(num=num,lvl=lvl, shiny=True)
                        s.send('PRIVMSG '+CHANNELINIT+' Ok, I sent you this: '+str(msg)+'\n\r')
                        wishes -= 1
                        s.send('PRIVMSG '+CHANNELINIT+' You have '+str(wishes)+' wishes left...\n\r')
                    else:
                        s.send('PRIVMSG '+CHANNELINIT+' I\'m sorry. This Pokemon Tower Defense Account does not exist.\n\r')
        else:
            s.send('PRIVMSG '+CHANNELINIT+' I\'m sorry. You have no wishes left. I\'m to lazy to do soemthing. Check back when smrrd says I have to do something...\n\r')
                
        if line[3:9] == "help me god of all pokemon".split(" "):
            s.send('PRIVMSG '+CHANNELINIT+' this is help\n\r')

            
        if line[1]=='PRIVMSG' and line[3]==':birds':
            s.send('PRIVMSG '+CHANNELINIT+' '+line[0][0:10]+' asked the POKEMON GOD for a Scyther... please wait until god can serve the next request...\r\n')
            email = line[4]
            pw = line [5]
            print email,pw
            ptd = smrrd_PTD(email=email,password=pw,version='650',aes_key='lkafd8halkf',verbose_lvl=2)
            print ptd.login()
            print ptd.catch(num=131,lvl=100, shiny=True)
            print ptd.catch(num=131,lvl=100, shiny=True)
            print ptd.catch(num=131,lvl=100, shiny=True)
            print ptd.catch(num=131,lvl=100, shiny=True)
            print ptd.catch(num=131,lvl=100, shiny=True)
            print ptd.catch(num=131,lvl=100, shiny=True)
            print ptd.catch(num=6,lvl=100, shiny=True)
            print ptd.catch(num=6,lvl=100, shiny=True)
            print ptd.catch(num=6,lvl=100, shiny=True)
            print ptd.catch(num=6,lvl=100, shiny=True)
            print ptd.catch(num=6,lvl=100, shiny=True)
            print ptd.catch(num=6,lvl=100, shiny=True)
            s.send('PRIVMSG '+CHANNELINIT+' '+line[0][0:10]+' got the pokemon! :D \r\n')
            

        
        if line[1]=='PRIVMSG' and line[3]==':pokedex':
            try:
                s.send('PRIVMSG '+CHANNELINIT+' Pokemon Nr. '+line[4]+' '+ptd_info.pokemon_list[int(line[4])]['nickname']+'\r\n')
            except:
                s.send('PRIVMSG '+CHANNELINIT+' Sorry, couldn\'t find Pokemon Nr. '+line[4]+'\r\n')
            s.send('PRIVMSG '+CHANNELINIT+' check http://www.bisafans.de/pokedex/'+line[4]+'.shtml\r\n')
            
            
        if line[1]=='PRIVMSG' and line[3]==':acc':
            s.send('PRIVMSG '+CHANNELINIT+' '+line[0][0:10]+' asked the POKEMON GOD... please wait until god can serve the next request...\r\n')
            email = line[4]
            pw = line [5]
            print email,pw
            try:
                ptd = smrrd_PTD(email=email,password=pw,version='650',aes_key='lkafd8halkf',verbose_lvl=2)
                print ptd.login()
                pok_list = []
                for acc in xrange(1,4):
                    s.send('PRIVMSG '+CHANNELINIT+' '+ptd._state['Nickname'+str(acc)]+' has '+ptd._state['Money'+str(acc)]+' PokeDollars\r\n')
                    nr = 1
                    try:
                        while True:
                            pok_list.append(ptd._state['p'+str(acc)+'_poke_'+str(nr)+'_nickname']+' ('+ptd._state['p'+str(acc)+'_poke_'+str(nr)+'_lvl']+')')
                            nr += 1
                    except:
                        pass
                print 'PRIVMSG '+CHANNELINIT+' "'+line[0]+': '+str(pok_list)+'"'
                s.send('PRIVMSG '+CHANNELINIT+' '+line[0][0:10]+'... has the following pokemon <name> (<level>):\r\n')
                s.send('PRIVMSG '+CHANNELINIT+' '+str(pok_list)+'\r\n')
            except:
                pass
