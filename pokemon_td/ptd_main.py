import ptd_info
from ptd import smrrd_PTD

ptd = smrrd_PTD(email='EMAIL',password='PASSWORD',version='650',aes_key='lkafd8halkf',verbose_lvl=1)

ptd.login()

ptd.catch(num=1,lvl=100, shiny=True)
ptd.catch(num=2,lvl=100, m1=123, m2=42)
    
ptd.info()

