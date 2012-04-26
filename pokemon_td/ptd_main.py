import ptd_info
from ptd import smrrd_PTD


ptd = smrrd_PTD(email='pokemon@smrrd.de',password='password',version='650',aes_key='lkafd8halkf',verbose_lvl=1)
ptd.register(email='gahsdkf@dgjas.de',password='fgajs')
ptd.info()

ptd.catch(num=1,lvl=100, shiny=True)
ptd.catch(num=2,lvl=100, m1=123, m2=42)
    
ptd.info()

