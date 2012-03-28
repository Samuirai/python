import ptd_info
from ptd import smrrd_PTD

ptd = smrrd_PTD(version='641',aes_key='aes_key',verbose_lvl=1) # optional login credentials
ptd.register(email='email',pw='password') # register a new account
ptd.info() # login and print information
ptd.settings(Version=1, badges=2, challenge=1, a_story=10, c_story=10, a_story_a=10, nickname='smrrd', money = 12345678,profil=1) # set Profile progress (Chapters, Red/Blue Version, Badges, ...)
ptd.info()
ptd.catch(num=1,lvl=100,m1=1,m2=2,shiny=True) # catch a Pokemon. m1-m4 are attacks
ptd.catch(num=2,lvl=100,m1=3,m2=4,shiny=True) # check ptd_info for the whole list
ptd.catch(num=3,lvl=100,m1=5,m2=6,shiny=True)
ptd.catch(num=131,lvl=100,m1=7,m2=8,shiny=True)
ptd.catch(num=4,lvl=100,m1=1,m2=2,shiny=False)
ptd.catch(num=5,lvl=100,m1=3,m2=4,shiny=False)
ptd.catch(num=6,lvl=100,m1=5,m2=6,shiny=False)
ptd.catch(num=151,lvl=100,m1=9,m2=10,shiny=False)
ptd.login() # login into account to get the new updated information
ptd.check_achieve() # have to be done, otherwise it will not work
ptd.set_achieve(1,'-1') # set an achievement to the values
ptd.set_achieve(1,'-2')
ptd.set_achieve(1,'-3')
ptd.set_achieve(1,'-4')
ptd.get_achieve(1) # get the reward of this achievement
ptd.set_achieve(2)
ptd.get_achieve(2)
ptd.set_achieve(3)
ptd.get_achieve(3)
ptd.set_achieve(4)
ptd.get_achieve(4)
ptd.set_achieve(5)
ptd.get_achieve(5)
ptd.set_achieve(6)
ptd.get_achieve(6)
ptd.set_achieve(7)
ptd.get_achieve(7)
ptd.set_achieve(8)
ptd.get_achieve(8)
ptd.set_achieve(9)
ptd.get_achieve(9)
ptd.set_achieve(10)
ptd.get_achieve(10)
ptd.set_achieve(11)
ptd.get_achieve(11)
ptd.set_achieve(12)
ptd.get_achieve(12)
ptd.set_achieve(13)
ptd.get_achieve(13)
ptd.clean(1) # release all pokemon profile in profile 1
ptd.info() # login and print information
for nr,pok in ptd_info.pokemon_list.items(): # use ptd_info list to catch all pokemon
    try:
        ptd.catch(num=nr,lvl=100,m1=1,extra=pok['extra'][0])
        ptd.catch(num=nr,lvl=100,m1=1,extra=pok['extra'][1])
    except:
        pass
ptd.settings(Version=1, nickname='Ash', badges=2, challenge=1, a_story=10, c_story=10, a_story_a=10, money = 12345678,profil=2) # set stuff for account 2
ptd.info()
ptd.catch(num=1,lvl=100,m1=1,m2=2,shiny=True,profil=2) # catch a Pokemonfor profile 2. m1-m4 are attacks
ptd.catch(num=2,lvl=100,m1=3,m2=4,shiny=True,profil=2) # check ptd_info for the whole list
ptd.catch(num=3,lvl=100,m1=5,m2=6,shiny=True,profil=2)
ptd.catch(num=131,lvl=100,m1=7,m2=8,shiny=True,profil=2)
ptd.catch(num=4,lvl=100,m1=1,m2=2,shiny=False,profil=2)
ptd.catch(num=5,lvl=100,m1=3,m2=4,shiny=False,profil=2)
ptd.catch(num=6,lvl=100,m1=5,m2=6,shiny=False,profil=2)
ptd.catch(num=151,lvl=100,m1=9,m2=10,shiny=False,profil=2)
ptd.info()