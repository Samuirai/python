import threading, urllib, urllib2, cookielib, re, html5lib, random, hashlib
from html5lib import treebuilders, treewalkers

class nazo:

	def __init__(self):
		self.stream = None
		self.start_hash = str(hashlib.sha1(str(random.randint(0,10000))).hexdigest());
		self.end_hash = str(hashlib.sha1(str(random.randint(0,10000))).hexdigest());
		self.random = str(random.randint(11111111,99999999))
		
	def text2dom(self,_text):
		parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
		walker = treewalkers.getTreeWalker("dom")
		dom = parser.parse(_text)
		stream = walker(dom)
		self.stream = stream
		
	def check_injection(self,stream=None):
		script_tag_open = False
		if not stream:
			stream = self.stream
		for element in stream:
			# check img tags for onerror
			#       url
			#       size
			# [img][color=#ff0000 onerror='eval(123)'][/color][/img]
			# [img][color=#ff0000 onerror="eval(123)"][/color][/img]
			# [img][color=#ff0000 ononerrorerror='eval(123)'][/color][/img] ... onerror replace
			# [img][color=#ff0000 ononerrorerror="eval(123)"][/color][/img]
			# [img]pic" onerror="eval(123)"][/img]
			# [img]pic" onerror="eval(123)" .png][/img]
			# [img]http://www.pic.png" onerror="eval(123)"][/img]
			# [img]http://www.pic.png" onerror="eval(123)" .png][/img]
			try:
				if element['name'] == u'img':
					for attr in element['data']:
						if attr[0] == u'onerror':
							if attr[1] == u'eval('+self.random+')':
								print element
			except:
				pass
			
			# search for script tags
			# <script>eval(123)</script>
			# <scr<script>ipt>eval(123)</script>
			# <script>eval(123)</scr</script>ipt>
			# <scr<script>ipt>eval(123)</scr</script>ipt>
			try:
				
				if element['type'] == 'StartTag' and element['name'] == u'script':
					script_tag_open = True;
				elif element['type'] == 'EndTag' and element['name'] == u'script':
					script_tag_open = False;
				elif script_tag_open:
					if u'eval('+self.random+')' in element['data']:
						print element
			except:
				pass
				
			# search for url tags with javascript
			# [url=javascript:eval(123)]link[/url]
			# [url=javajavascriptscript:eval(123)]link[/url]
			# [url=javascript:eval(123)]link[/url]
			try:
				if element['name'] == u'a':
					for attr in element['data']:
						if attr[0] == u'href':
							if u'javascript:eval('+self.random+')' in attr[1]:
								print element
			except:
				pass