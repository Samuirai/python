# this is just a test script for a calculation in my TEST04 project.
# nothing special. You can ignore this senseless script.
to = 100
fr = 50
delta = 0
if to>fr:
    delta = to-fr
else:
    delta = fr-to
print "From "+str(fr)+" to "+str(to)+" with delta "+str(delta)
print str(8000/delta)+" clock divider"
# -> 1   = 8000
# -> 2   = 4000
# -> 4   = 2000
# -> 8   = 1000
# -> 16  = 500
# -> 32  = 250
# -> 64  = 125
# -> 128 = 62
