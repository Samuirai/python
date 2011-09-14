#!/usr/bin/python2.7
import sys
from subprocess import call

call("djtgcfg enum", shell=True)
call("djtgcfg prog -d Nexys3 -i 0 -f "+sys.argv[1],shell=True)