import threading, urllib, urllib2, cookielib, re, html5lib, random, hashlib, class_helper,sys,traceback
from html5lib import treebuilders, treewalkers
from optparse import OptionParser
from class_nazo import nazo

helper = class_helper.helper()
helper.print_nazo()
try:
	_version = "0.1.0"
	
	# Option Parser stuff
	parser = OptionParser()
	parser.add_option("-V", "--version", help="shows version number", action="store_true", default=False)
	parser.add_option("-v", "--verbose", help="set a verbose level", type="int", action="store", default=1)
	parser.add_option("-e", "--error",   help="set a error level",  action="store_true", default=False)
	parser.add_option("-l", "--logfile", help="create a log file", type="str", action="store", default="log")
	
	(options, args) = parser.parse_args()
	
	#print options
	
	if options.version == True:
		helper.print_version(_version)
		exit(1)
					
	#cj = cookielib.CookieJar()
	#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))	
	
	
	helper.verbose_lvl = options.verbose
	helper.logfile = options.logfile
	helper.error_lvl = options.error
	
	inject = nazo(_form="http://127.0.0.1/~samuirai/bbcode/index.php",_helper=helper,_data='bbcode')
	inject.check_bbcode()
	#opener = urllib2.build_opener()
	#login_data = urllib.urlencode({})
	#response = opener.open('http://127.0.0.1/~samuirai/bbcode/index.php', login_data)
	#html = response.read()
	
	#i = re.search(inject.start_hash+"(.*)"+inject.end_hash,html).group(1)
	#html = i
	#print html
	
	#inject.text2dom(html)
	#inject.check_injection()
except:
	helper.error("nazo.py CRITICAL!")
	helper.error(traceback.format_exc())
