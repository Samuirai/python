import threading, urllib, urllib2, cookielib, re, html5lib, random, hashlib, sys, traceback
import class_helper, class_bbcode
from html5lib import treebuilders, treewalkers

class nazo:

	def __init__(self,_form,_resulturl=None,_post=[],_data="",_helper=class_helper.helper()):
		try:
			_helper.print_disclaimer()
			self.helper = _helper
			self.stream = None
			self.bbcode = class_bbcode.bbcode(_helper)
			self.bbcode.create_bbcode_list()
			self.post = _post
			self.data = _data
			self.start_hash = str(hashlib.sha1(str(random.randint(0,10000))).hexdigest());
			self.end_hash = str(hashlib.sha1(str(random.randint(0,10000))).hexdigest());
			self.random = str(random.randint(11111111,99999999))
			#self.helper.verbose(1,self.helper.ansi.BLUE+"Welcome to nazo - the BBCode XSS Vulnerability scanner"+self.helper.ansi.END)
		except:
			_helper.error("nazo.__init__()")
			_helper.error(traceback.format_exc())
		
	def text2dom(self,_text):
		parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
		walker = treewalkers.getTreeWalker("dom")
		dom = parser.parse(_text)
		stream = walker(dom)
		self.stream = stream
	
	def check_bbcode(self):
		data = ""
		for bbcode in self.bbcode.bbcode_list:
			data += str(bbcode[0])
		(html,result) = self.get_result({self.data: self.start_hash+data+self.end_hash})
		if result:
			self.bbcode.check_bbcode_list(result,self.bbcode.bbcode_list)
		else:
			self.bbcode.check_bbcode_list(html,self.bbcode.bbcode_list)
		
	def get_result(self,_post):
		opener = urllib2.build_opener()
		login_data = urllib.urlencode(_post)
		response = opener.open('http://127.0.0.1/~samuirai/bbcode/index.php', login_data)
		html = response.read()
		try:
			result = re.search(self.start_hash+"(.*)"+self.end_hash,html).group(1)
		except:
			result = None
		return (html,result)
		
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
								self.helper.verbose(1,"<img> onerror eval() injection")
								self.helper.verbose(2," "+str(element))
							else:
								self.helper.verbose(1,"<img> onerror injection")
								self.helper.verbose(2," "+str(element))
			except KeyError:
				pass
			except:
				self.helper.error(traceback.format_exc())
				#repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
			
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
						self.helper.verbose(1,"<script> eval injection")
						self.helper.verbose(2," "+str(element))
					else:
						self.helper.verbose(1,"<script>")
						self.helper.verbose(2," "+str(element))
			except KeyError:
				pass
			except:
				self.helper.error(traceback.format_exc())
				
			# search for url tags with javascript
			# [url=javascript:eval(123)]link[/url]
			# [url=javajavascriptscript:eval(123)]link[/url]
			# [url=javascript:eval(123)]link[/url]
			try:
				if element['name'] == u'a':
					for attr in element['data']:
						if attr[0] == u'href':
							if u'javascript:eval('+self.random+')' in attr[1]:
								self.helper.verbose(1,"<a href=...> javascript:eval() injection")
								self.helper.verbose(2," "+str(element))
			except KeyError:
				pass
			except:
				self.helper.error(traceback.format_exc())
				
				
				