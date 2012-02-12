import class_helper,sys,traceback

class bbcode:
	def __init__(self,_helper=class_helper.helper()):
		try:
			self.helper = _helper
			self.helper.verbose(2,"init BBCode Class")
			self._supported = 0
			self.tag_in_img = False
			# FORMAT: (tag name, typ, useable, valid data list)
			# tag - Tag name (b,u,i,...)
			# typ -
			#  1: [b][/b]
			#  2: [b=a][/b]
			# usable is 1 if tag is recognized
			#  -1 if unsure
			# list with special valid data
			self.bbcode_list = []
			self.bbcode_list_injection = []
			self.bbcodes = [
				("b",			0,[]),
				("i",			0,[]),
				("u",			0,[]),
				("left",		0,[]),
				("right",		0,[]),
				("center",		0,[]),
				("img",			0,["test.png","http://www.asd.com/test.png"]),
				("code",		0,[]),
				("php",			0,[]),
				("html",		0,[]),
				("highlight",	0,[]),
				("noparse",		0,[]),
				("attach",		0,[]),
				("bug",			0,[]),
				("pgn3",		0,[]),
				
				("email",		0,["test@test.com"]),
				("url",			0,["test.com","www.test.com","http://www.test.com"]),
				("thread",		0,[]),
				("post",		0,[]),
				("thread",		0,[]),
				("video",		0,["6GAD9pmYqXQ","http://www.youtube.com/watch?v=6GAD9pmYqXQ","www.youtube.com/watch?v=6GAD9pmYqXQ"]),
				("thread",		0,[]),
				("quote",		0,[]),
				("pgn2",		0,[]),
				
				("email",		1,["test@test.com"]),
				("url",			1,["test.com","www.test.com","http://www.test.com"]),
				("thread",		1,[]),
				("post",		1,[]),
				("thread",		1,[]),
				("video",		1,["6GAD9pmYqXQ","http://www.youtube.com/watch?v=6GAD9pmYqXQ","www.youtube.com/watch?v=6GAD9pmYqXQ"]),
				("thread",		1,[]),
				("quote",		1,[]),
				("pgn2",		1,[]),
				
				("threadvb",	1,[]),
				("wiki",		1,[]),
				("color",		1,["green","#ff0000"]),
				("size",		1,["+2","big","12pt","1.5em"]),
				("font",		1,["courier","arial"])
			]
		except:
			_helper.error("bbcode.__init__()")
			_helper.error(traceback.format_exc())
			
	def get_valid_data(self,_tag):
		for tag in self.bbcodes:
			if tag[0] == _tag:
				return tag[2]
	
	def create(self,_tag,_data="",_value=None):
		try:
			# _value is sth. like [color=#COLOR] [/color]
			if _value:
				return ("["+_tag+"="+_value+"]"+_data+"[/"+_tag+"]",_tag,_data,_value)
			else:
				return ("["+_tag+"]"           +_data+"[/"+_tag+"]",_tag,_data)
		except:
			self.helper.error("bbcode.create()")
			self.helper.error(traceback.format_exc())
	
	def create_bbcode_list(self):
		# create all possible mutations with bbcode tags and possible valid data values
		try:
			for code in self.bbcodes:
				for valid_data in code[2]:
					if code[1]==1:
						self.bbcode_list.append([self.create(code[0],"data",valid_data),False])
						self.bbcode_list.append([self.create(code[0],"",valid_data),False])
						#self.bbcode_list.append([self.create(code[0],valid_data,valid_data),False])
					elif code[1]==0:
						self.bbcode_list.append([self.create(code[0],valid_data),False])
				if code[1]==1:
					self.bbcode_list.append([self.create(code[0],"test","value"),False])
					self.bbcode_list.append([self.create(code[0],"test",""),False])
					self.bbcode_list.append([self.create(code[0],"","value"),False])
					self.bbcode_list.append([self.create(code[0],"",""),False])
				elif code[1]==0:
					self.bbcode_list.append([self.create(code[0]),False])
					self.bbcode_list.append([self.create(code[0],"test"),False])
			for bbcode in self.bbcode_list:
				self.helper.verbose(4,"added to BBCode test: "+self.helper.ansi.BLUE+str(bbcode[0][0])+self.helper.ansi.END)
			self.helper.verbose(1,"created a list with "+str(len(self.bbcode_list))+" BBCodes to test if they exist")
		except:
			self.helper.error("bbcode.test_bbcodes()")
			self.helper.error(traceback.format_exc())
			
	def get_supported_bbcodes(self):
		tag_list = []
		for tag in self.bbcode_list:
			if tag[0][1] not in tag_list and tag[1]:
				for t in self.bbcodes:
					if t[0] == tag[0][1]:
						tag_list.append(t)
		return tag_list
		
	def create_bbcode_list_injection(self):
		
		if self.tag_in_img:
			self.helper.verbose(1,"Tag inside [img] tag is possible. Will create injection List for this")
		
		if self._supported == 0:
			self.helper.verbose(1,"no BBCodes are supported? Check your settings again.")
		else:
			for bbcode in self.bbcode_list:
				if bbcode[1]:
					if self.tag_in_img:
						if bbcode[0][1] == "img":
							# direct image tag injection
							onerror=[
									" onerror=eval()",
									" onerror=eval()",
									" onerror=\"eval()\"",
									" onerror=\"eval()\"",
									" onerror=\'eval()\'",
									" onerror=\'eval()\'",
									" onerror=\"eval();\"",
									" onerror=\"eval();\"",
									" onerror=\'eval();\'",
									" onerror=\'eval();\'",
									"\" onerror=eval()",
									"\' onerror=eval()",
									"\" onerror=\"eval()\"",
									"\' onerror=\"eval()\"",
									"\" onerror=\'eval()\'",
									"\' onerror=\'eval()\'",
									"\" onerror=\"eval();\"",
									"\' onerror=\"eval();\"",
									"\" onerror=\'eval();\'",
									"\' onerror=\'eval();\'"
									]
							for _injection in onerror:
								self.bbcode_list_injection.append([self.create("img",bbcode[0][2]+_injection,""),False])
							#print self.get_supported_bbcodes()
							for tag in self.get_supported_bbcodes():
								for _injection in onerror:
									#self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+"[/img]","",""),False])
									self.bbcode_list_injection.append([("[img]["+tag[0]+"]"+_injection+"[/"+tag[0]+"][/img]","",""),False])
									self.bbcode_list_injection.append([("[img]["+tag[0]+"]"+_injection+"[/img][/"+tag[0]+"]","",""),False])
									self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"]"+_injection+"[/"+tag[0]+"][/img]","",""),False])
									self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"]"+_injection+"[/img][/"+tag[0]+"]","",""),False])
									for valid_data in tag[2]:
										if tag[1]==1:
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+"]"+_injection+"[/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+"]"+_injection+"[/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+"]"+_injection+"[/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+"]"+_injection+"[/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+"]"+valid_data+""+_injection+"[/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+"]"+valid_data+""+_injection+"[/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+"]"+valid_data+" "+_injection+"[/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+"]"+valid_data+" "+_injection+"[/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+""+_injection+"][/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+""+_injection+"][/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+""+_injection+"][/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+""+_injection+"][/img]["+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+""+_injection+"]"+valid_data+" [/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+valid_data+""+_injection+"]"+valid_data+" [/img]["+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+""+_injection+"]"+valid_data+" [/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+valid_data+""+_injection+"]"+valid_data+" "+_injection+"[/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+_injection+"][/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+_injection+"][/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+_injection+"][/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+_injection+"][/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+_injection+"]"+valid_data+" [/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"="+_injection+"]"+valid_data+" [/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+_injection+"]"+valid_data+" [/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"="+_injection+"]"+valid_data+" "+_injection+"[/img]["+tag[0]+"]","",""),False])
										elif tag[1]==0:
											self.bbcode_list_injection.append([("[img]["+tag[0]+"]"+valid_data+""+_injection+"[/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]["+tag[0]+"]"+valid_data+""+_injection+"[/img][/"+tag[0]+"]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"]"+valid_data+""+_injection+"[/"+tag[0]+"][/img]","",""),False])
											self.bbcode_list_injection.append([("[img]"+bbcode[0][2]+" ["+tag[0]+"]"+valid_data+""+_injection+"[/img][/"+tag[0]+"]","",""),False])
							
			for bbcode in self.bbcode_list_injection:
				self.helper.verbose(4,"added to BBCode XSS injection test: "+self.helper.ansi.BLUE+str(bbcode[0][0])+self.helper.ansi.END)
			self.helper.verbose(1,"created a list with "+str(len(self.bbcode_list_injection))+" BBCodes to test XSS injection")
					
	def check_bbcode_list(self,_data,_list):
		_supported = 0
		for bbcode in _list:
			if bbcode[0][0] in _data:
				bbcode[1] = False
				self.helper.verbose(4,"BBCode not supported: "+self.helper.ansi.RED+bbcode[0][0]+self.helper.ansi.END)
			else:
				bbcode[1] = True
				_supported+=1
				self.helper.verbose(3,"BBCode probably supported: "+self.helper.ansi.GREEN+bbcode[0][0]+self.helper.ansi.END)
		self.helper.verbose(1,str(_supported)+" from "+str(len(_list))+" checked BBCodes probably supported")
		
		return _supported