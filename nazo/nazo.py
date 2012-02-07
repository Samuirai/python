import threading, urllib, urllib2, cookielib, re, html5lib, random, hashlib, class_helper
from html5lib import treebuilders, treewalkers
from optparse import OptionParser
from class_nazo import nazo

_version = "0.1.0"

# Option Parser stuff
parser = OptionParser()
parser.add_option("-V", "--version", help="shows version number", action="store_true", default=False)
parser.add_option("-v", "--vebose", help="set a verbose level", type="int", action="store", default=0)

(options, args) = parser.parse_args()


if options.version == True:
	class_helper.print_version(_version)
	exit(1)

class_helper.print_disclaimer()
				
#cj = cookielib.CookieJar()
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))		
inject = nazo()
opener = urllib2.build_opener()
login_data = urllib.urlencode({'bbcode' : inject.start_hash+'[img][color=#ff0000 onerror="eval('+inject.random+')"][/color][/img][url=asd.de]link[/url][url=javascript:eval('+inject.random+')]link[/url]'+inject.end_hash})
response = opener.open('http://127.0.0.1/~samuirai/bbcode/index.php', login_data)
html = response.read()

i = re.search(inject.start_hash+"(.*)"+inject.end_hash,html).group(1)
html = i
print html

inject.text2dom(html)
inject.check_injection()