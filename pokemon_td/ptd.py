#                              __  #
#     _____ ________ ______ __/ /  #
#    /  __/  ,  ,  /  _/ _/__  /   #
#   /__  /  /  /  /  /  / /_/ /    #
#  /____/__/__/__/__/__/_____/     #
#  >> I want to write exploits...  #
#  >> May you teach me?            #
#                                  # 

import aes, urllib,urllib2, time, cookielib, re
import ptd_info
import random

class smrrd_PTD(object):

    class ansi:
        END 	= '\033[0m'
        BOLD 	= '\033[1m'
        RED 	= '\033[31m'
        GREEN 	= '\033[32m'
        YELLOW 	= '\033[33m'
        BLUE 	= '\033[34m'
        CLEAR 	= '\033[2J'
        @staticmethod
        def POS(_x=0,_y=0):
           return '\033['+str(_x)+';'+str(_y)+'H'

    def log(self,level, message):
        if level <= self._verbose_lvl:
            print "\r"+self.ansi.YELLOW+"["+str(level)+"]"+self.ansi.END+" "+message

    def __init__(self, email="", password="", version="", aes_key="",verbose_lvl=1):
        self.update_url = None
        self._password = password
        self._email = email
        self._version = version
        self._aes_key = aes_key
        self._verbose_lvl = verbose_lvl
        self._state = {}
        self._save = None
        self.center = None
        self.logged = False

    def url(self,prefix="http://www.sndgames.com/php/newPoke6.php?Date="):
        # obfuscating the time with random values
        _url = prefix+str(int(time.time())-random.randint(0,10000))
        self.log(3,"URL: "+_url)
        return _url


    def login(self, silent=False):
        if not silent: self.log(1,"Login "+self._email+":"+self._password)
        response = self.request({
        'Action': 'loadAccount', 
        'Pass': self._password, 
        'Email': self._email,
        'ver': self._version
        })
        self.logged = False
        try:
            if not silent: self.log(2,"Login response: "+str(self.decrypt(response)))
            self.update_state(self.data(self.decrypt(response)))
            self._save = self._state['CurrentSave']
        except:
            pass
        return response

    def login2(self):

        cj = cookielib.CookieJar()
        self.center = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_data = urllib.urlencode({
                'Email': self._email,
                'Pass': self._password
            })
        f = self.center.open('http://www.sndgames.com/games/ptd/trading_account.php', login_data)

        return f.read()

    def check_snd_coins(self):
        try:
            f = self.center.open('http://www.sndgames.com/games/ptd/dailyCode.php?whichProfile=1&whichDaily=Rare')
            m = re.search('<p>Congratulation(.*)</p><p>(.*)</p><p>.*', f.read())
            self.log(1,'Daily Gift: '+m.group(2))
        except:
            self.log(1,'Daily Gift Error')


    def register(self,email,password,pos='-1'):
        self._email = email
        self._password = password
        self.log(1,"Register Account "+self._email+":"+self._password)
        _post = {
            'Action': 'createAccount', 
            'Pass': password, 
            'Email': email,
            'ver': self._version
        }
        self.logged = False
        response = self.request(_post)
        self.log(2,"Register response: "+str(response))
        return response

    def set_achieve(self,nr,pos='-1'):
        self.log(1,"set Achievements Nr. "+str(nr)+"="+pos)
        _post = {
            'Action': 'updateAccount', 
            'Pass': self._password, 
            'Email': self._email,
            'type': nr,
            'pos': pos
        }
        response = self.request(_post,self.url("http://www.sndgames.com/php/newAchieve.php?Date="))
        self.log(2,"set Achievement response: "+str(response))
        return response

    def check_achieve(self):
        self.log(1,"check Achievements")
        _post = {
            'Action': 'checkAccount', 
            'Pass': self._password, 
            'Email': self._email
        }
        response = self.request(_post,self.url("http://www.sndgames.com/php/newAchieve.php?Date="))
        self.log(2,"check Achievements response: "+str(response))
        return response

    def get_achieve(self,nr):
        self.log(1,"get Achievements reward Nr. "+str(nr))
        _prize = ['None','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen']
        _post = {
            'Action': 'get_Reward_'+_prize[nr], 
            'Pass': self._password, 
            'Email': self._email
        }
        response = self.request(_post,self.url("http://www.sndgames.com/php/newAchieve.php?Date="))
        self.log(2,"get Achievement response: "+str(response))
        return response


    def save(self,post,profile):

        self.log(2,"save Account Profile Nr. "+str(profile))
        self.log(2," > "+str(post))

        _post = {
                'Action': 'saveAccount', 
                'Pass': self._password, 
                'Email': self._email,
                'ver': self._version
            }

        _save = {
                'currentSave': self._save,
                'whichProfile': profile,
                'ShinyHunt': self._state['shinyHunt'+str(profile)],
                'Avatar': 'b_42',
                'Nickname': self._state['Nickname'+str(profile)],
                'Money': self._state['Money'+str(profile)],
                'badges': self._state['Badges'+str(profile)], 
                'Version': self._state['Version'+str(profile)],
                'challenge': self._state['Challenge'+str(profile)], 
                'a_story': self._state['Advanced'+str(profile)],
                'c_story': self._state['Classic'+str(profile)],
                'a_story_a': self._state['Advanced'+str(profile)+'_a']
            }
        _save.update(post)
        
        params = urllib.urlencode(_save)
            
        _post['saveString'] = self.encrypt(params)

        response = self.request(_post)
        self.log(2,"save Account Response: "+str(response))
        response = self.data(response)
        try:
            self._save = response['newSave']
        except:
            pass
        return response


    def data(self,msg):
        return dict(item.split("=") for item in msg.split("&"))

    def update_state(self,new):
        self._state.update(new)

    def request(self,post, url=None):
        params = urllib.urlencode(post)

        if not url:
            url = self.url()
        f = urllib.urlopen(url, params)
        try: 
            if not self.logged: 
                self.logged = True
            
        except: pass
        return f.read()

    def decrypt(self,msg):
        return aes.decrypt(msg, self._aes_key, 256)

    def settings(self,Version=1, badges=0, challenge=1, a_story=10, c_story=10, a_story_a=10, money=1,nickname='hacked',profil=1,silent=False):
        if not silent: self.log(1,"set Account Settings")
        response =  self.save({'Version': Version,
                        'badges': badges,
                        'challenge': challenge,
                        'a_story': a_story,
                        'c_story': c_story,
                        'a_story_a': a_story_a,
                        'Money':money,
                        'Nickname': nickname},profil)
        if not silent: self.log(2,"set Account Settings response: "+str(response))
        return response

    def encrypt(self,msg):
        self.log(3,"encrypt string: "+str(msg))
        return aes.encrypt(msg, self._aes_key, 256)

    def catch(self,num=1,lvl=1,m1=1,m2=0,m3=0,m4=0,mSel=1,tag='n',ability=0,item=0,profil=1,shiny=False,nickname=None,extra=None,shadow=False):

        result = None
        if not nickname:
            nickname = ptd_info.pokemon_list[num]['nickname']

        try:
            if not extra:
                if shiny:
                    extra = ptd_info.pokemon_list[num]['extra'][1]
                    self.log(1,"catch Pokemon "+str(nickname)+" ("+str(num)+") shiny")
                elif shadow:
                    extra = ptd_info.pokemon_list[num]['extra'][2]
                    self.log(1,"catch Pokemon "+str(nickname)+" ("+str(num)+") shadow")
                else:
                    extra = ptd_info.pokemon_list[num]['extra'][0]
                    self.log(1,"catch Pokemon "+str(nickname)+" ("+str(num)+")")
            else:
                self.log(1,"catch Pokemon "+str(nickname)+" ("+str(num)+") extra")

            result = self.save({'poke1_exp': 0,
            'poke1_lvl': lvl,
            'poke1_reason': 'cap',
            'poke1_myID': 0,
            'poke1_ability': ability,
            'poke1_item': item,
            'poke1_owner': 0,
            'poke1_extra': extra,
            'poke1_pos': 1,
            'poke1_m1': m1,
            'poke1_m2': m2,
            'poke1_m3': m3,
            'poke1_m4': m4,
            'poke1_mSel': mSel,
            'poke1_num': num,
            'poke1_targetType': 1,
            'poke1_tag': tag,
            'poke1_nickname': nickname,
            'HMP':1
            },profil)

            self.log(2,"catch Pokemon response: "+str(result))
        except:
            pass
        try:
            if result['newPokePos_1']:
                return [nickname,lvl, ptd_info.attack_list[m1], ptd_info.attack_list[m2], ptd_info.attack_list[m3],
                        ptd_info.attack_list[m4]]
        except:
            pass
        return result

    def clean(self,acc):
        self.log(1,"release all Pokemon in profile Nr. "+str(acc))
        delete = ""
        try:
            nr = 1
            while True:

                if nr==1:
                    delete += self._state['p'+str(acc)+'_poke_'+str(nr)+'_myID']
                else:
                    delete += '|'+self._state['p'+str(acc)+'_poke_'+str(nr)+'_myID']
                nr += 1
        except:
            pass
        print delete
        return self.save({'releasePoke': delete},acc)

    def get_state(self):
        return self._state
        
    def get_pokemon_ids(self):
        pokes = []
        for acc in xrange(1,4):
            try:
                nr = 1
                while True:
                    pokes.append(self._state['p'+str(acc)+'_poke_'+str(nr)+'_myID'])
                    nr += 1
            except:
                pass
        return pokes

    def info(self):
        self.login()

        if self._state:

            print self.ansi.BOLD+'[ Pokemon TD -'+self.ansi.GREEN+' smrrd ]\n'+self.ansi.END
            print self.ansi.BLUE+'ProfileID    '+self.ansi.END+self._state['ProfileID']
            print self.ansi.BLUE+'CurrentSave  '+self.ansi.END+self._state['CurrentSave']
            print self.ansi.BLUE+'dex1         '+self.ansi.END+self._state['dex1']
            print self.ansi.BLUE+'dex1Shiny    '+self.ansi.END+self._state['dex1Shiny']
            print self.ansi.BLUE+'dex1Shadow   '+self.ansi.END+self._state['dex1Shadow']



            for acc in xrange(1,4):

                print self.ansi.RED+'\n[ '+str(acc)+' | '+self._state['Nickname'+str(acc)]+' | '+\
                                           self._state['Money'+str(acc)]+' Eur | '+self._state['Version'+str(acc)]+' ]'+self.ansi.END
                print ''
                print self.ansi.YELLOW+' [*]'+self.ansi.END+' ShinyHunt'.ljust(15)+self._state['shinyHunt'+str(acc)]
                print self.ansi.YELLOW+' [*]'+self.ansi.END+' Badges'.ljust(15)+self._state['Badges'+str(acc)]
                print self.ansi.YELLOW+' [*]'+self.ansi.END+' Classic'.ljust(15)+self._state['Classic'+str(acc)]
                print self.ansi.YELLOW+' [*]'+self.ansi.END+' Challenge'.ljust(15)+self._state['Challenge'+str(acc)]
                print self.ansi.YELLOW+' [*]'+self.ansi.END+' Advanced'.ljust(15)+self._state['Advanced'+str(acc)]
                print self.ansi.YELLOW+' [*]'+self.ansi.END+' Advanced_a'.ljust(15)+self._state['Advanced'+str(acc)+'_a']
                print self.ansi.YELLOW+' [*]'+self.ansi.END+' Items:'.ljust(15),
                for itemnr in xrange(1,int(self._state['p'+str(acc)+'_numItem'])+1):
                    print self._state['p'+str(acc)+'_item_'+str(itemnr)+'_num']+',',

                print "\n"
                print self.ansi.BLUE+'  |-----|----------------------|------|----------|------|--------|---------------------------------------------------|'
                try:
                    nr = 1
                    print self.ansi.BLUE+' '+' | '+'nr'.rjust(3)+\
                                             ' | '+'nickname'.rjust(20)+\
                                             ' | '+'lvl'.rjust(4)+\
                                             ' | '+'myID'.rjust(8)+\
                                             ' | '+'tag'.rjust(4)+\
                                             ' | '+'shiny'.rjust(6)+\
                                             ' | '+'skill list'.ljust(50)+'|'+self.ansi.END
                    print self.ansi.BLUE+'  |-----|----------------------|------|----------|------|--------|---------------------------------------------------|'+self.ansi.END
                    while True:
                        print ' '+' | '+self._state['p'+str(acc)+'_poke_'+str(nr)+'_num'].rjust(3)+\
                                  ' | '+self._state['p'+str(acc)+'_poke_'+str(nr)+'_nickname'].rjust(20)+\
                                  ' | '+self._state['p'+str(acc)+'_poke_'+str(nr)+'_lvl'].rjust(4)+\
                                  ' | '+self._state['p'+str(acc)+'_poke_'+str(nr)+'_myID'].rjust(8)+\
                                  ' | '+self._state['p'+str(acc)+'_poke_'+str(nr)+'_tag'].rjust(4)+\
                                  ' | '+self._state['p'+str(acc)+'_poke_'+str(nr)+'_noWay'].rjust(6)+\
                                  ' | '+(ptd_info.attack_list[int(self._state['p'+str(acc)+'_poke_'+str(nr)+'_m1'])]+', '+\
                                  ' '+ ptd_info.attack_list[int(self._state['p'+str(acc)+'_poke_'+str(nr)+'_m2'])]+', '+\
                                  ' '+ ptd_info.attack_list[int(self._state['p'+str(acc)+'_poke_'+str(nr)+'_m3'])]+', '+\
                                  ' '+ ptd_info.attack_list[int(self._state['p'+str(acc)+'_poke_'+str(nr)+'_m4'])]).ljust(50)+'|'
                        nr += 1

                except:
                    pass
                print '  |-----|----------------------|------|----------|------|--------|---------------------------------------------------|'
        self.log(0,"Press [Enter] to close the hack")
        raw_input()
        return self._state