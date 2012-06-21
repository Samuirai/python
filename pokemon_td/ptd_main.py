#                              __  #
#     _____ ________ ______ __/ /  #
#    /  __/  ,  ,  /  _/ _/__  /   #
#   /__  /  /  /  /  /  / /_/ /    #
#  /____/__/__/__/__/__/_____/     #
#  >> I want to write exploits...  #
#  >> Would you teach me?          #
#                                  # 

import ptd_info
from ptd import smrrd_PTD

ptd = smrrd_PTD(email='asdasf@asdga.de',password='asdasd',version='650',aes_key='lkafd8halkf',verbose_lvl=3)
ptd.register(email='asdkujsf@asdga.de',password='asdasd')
ptd.info()
for i in xrange(0,500):
    ptd.catch(num=244,lvl=100,extra=i,nickname="Test "+str(i))
ptd.info()
