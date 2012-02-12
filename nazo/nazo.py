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
	parser.add_option("-r", "--random",  help="randomize BBCode lists", action="store_true", default=False)
	parser.add_option("-u", "--url", 	 help="form action URL", type="str", action="store", default="")
	parser.add_option("-d", "--data", 	 help="HTML input name for request", type="str", action="store", default=None)
	parser.add_option("-v", "--verbose", help="set a verbose level", type="int", action="store", default=1)
	parser.add_option("-e", "--error",   help="set a error level",  action="store_true", default=False)
	parser.add_option("-l", "--logfile", help="create a log file", type="str", action="store", default="log")
	parser.add_option("-p", "--post", 	 help="additional post request variables", type="str", action="store", default=None)
	
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
	
	if not options.url:
		url = helper.input("Form action URL: ")
	else:
		url = options.url
		
	if not options.data:
		data = helper.input("HTML input name for request needed: ")
	else:
		data = options.data
		
	post = {}
	if options.post:
		post = eval(options.post)
		
	inject = nazo(_form=url,_helper=helper,_data=data,_post=post)
	#inject = nazo(_form="http://bbcparser.recgr.com/demo.php",_post={"button": " Parse >>"},_helper=helper,_data='content')
	inject.random = options.random
	#inject = nazo(_form="http://127.0.0.1/~samuirai/bbcode/index.php",_helper=helper,_data='bbcode')
	#
	#inject = nazo(_form="http://bbcparser.recgr.com/demo.php",_post={"button": " Parse >>"},_helper=helper,_data='content')
	inject.print_
	number = None
	while not inject.check_bbcode(number):
		number = int(helper.input("adjust the number of BBCodes to check per request: "))
	inject.learn_bbcode()
	inject.check_bbcode_xss()
	#opener = urllib2.build_opener()
	#login_data = urllib.urlencode({})
	#response = opener.open('http://127.0.0.1/~samuirai/bbcode/index.php', login_data)
	#html = response.read()
	
	#i = re.search(inject.start_hash+"(.*)"+inject.end_hash,html).group(1)
	#html = i
	#print html
	
	#inject.text2dom(html)
	#inject.check_injection()
except KeyboardInterrupt:
	helper.error("nazo exited with CTRL+C")
except EOFError:
	helper.error("nazo exited with CTRL+D")
except SystemExit:
	helper.error("nazo exited with SystemExit call")
except:
	helper.error("unexpected error")
	helper.error(traceback.format_exc())
