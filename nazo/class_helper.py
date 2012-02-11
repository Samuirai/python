class helper:
	
	def __init__(self,_verbose=0,_error=0,_logfile="log"):
		self.verbose_lvl = _verbose
		self.error_lvl = _error
		self.logfile = _logfile
		
	class ansi:
	    END 	= '\033[0m'
	    BOLD 	= '\033[1m'
	    RED 	= '\033[31m'
	    GREEN 	= '\033[32m'
	    YELLOW 	= '\033[33m'
	    BLUE 	= '\033[34m'
	    CLEAR 	= '\033[2J'
	    @staticmethod
	    def POS(_x=0,_y=0):
		   return '\033['+str(_x)+';'+str(_y)+'H'
				
	def print_header(self,_text):
		print "___["+self.ansi.BOLD+_text+self.ansi.END+"]___________________________"
	
	def verbose(self,_level, _message):
		if _level <= self.verbose_lvl:
			print self.ansi.YELLOW+"["+str(_level)+"]"+self.ansi.END+" "+_message
			
	def error(self, _message):
		if self.error_lvl and self.verbose_lvl > 0:
			print self.ansi.RED+"[Error]"+self.ansi.END+" "+_message
			
	def print_nazo(self):
		print """
"""+self.ansi.BLUE+self.ansi.BOLD+""" ___   \   \ | /
"""+self.ansi.BLUE+"""_____ \ \   \|/          """+self.ansi.GREEN+"""__________   
"""+self.ansi.BLUE+""" ___   \  ___|___       """+self.ansi.GREEN+"""/  ____   /  _______  __   ___________   ___________
"""+self.ansi.BLUE+""" ___ __     /|\        """+self.ansi.GREEN+"""/  /   /  /  /  ___  |/ /  /_____   __/  /  _____   / 
"""+self.ansi.BLUE+""" ___   \   / | \      """+self.ansi.GREEN+"""/  /   /  /  /  /  /    /    __  /__/    /  /    /  /
"""+self.ansi.BLUE+"""|   |   \    |       """+self.ansi.GREEN+"""/  /   /  /  /  /__/    /  __/  /____    /  /____/  / """+self.ansi.RED+""">> nazo
"""+self.ansi.BLUE+"""|___|  _/\          """+self.ansi.GREEN+"""/__/   /__/  /_______/|_/  /__________/  /__________/ """+self.ansi.RED+""">> by smrrd
"""+self.ansi.BLUE+"""|   '     \______

"""+self.ansi.END+self.ansi.RED+""" >> a BBCode XSS Vulnerability Scanner
"""+self.ansi.END

	def print_disclaimer(self):
		self.print_header("Disclaimer")
		print self.ansi.END+" nazo is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;"
		print " without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."
		print " See the GNU General Public License for more details."
		print ""
		print " Whatever you do with this tool is uniquely your responsibility."
		print " If you are not authorized to test a specific bbcode form be aware that such action might"
		print " get you in trouble with a lot of law enforcement agencies."
		print " I wrote this tool to help bbcode parser developer or penetration testers - who are"
		print " authorized - to test a product or their code for security issues."
		print ""
		print self.ansi.RED+" With Great Power Comes Great Responsibility!"+self.ansi.END
		print ""
	
	def print_version(self,_version):
		self.print_header("Version")
		print '{0:.<25}  {1}'.format(self.ansi.RED+"version"+self.ansi.END,	_version+"v")
		print '{0:.<25}  {1}'.format(self.ansi.RED+"date"+self.ansi.END,		'9 February 2012')
		print '{0:.<25}  {1}'.format(self.ansi.RED+"coder"+self.ansi.END,		self.ansi.GREEN+'smrrd'+self.ansi.END)
		print '{0:.<25}  {1}'.format(self.ansi.RED+"thx to"+self.ansi.END,	'momo, hdznrrd, dop3j0e, rel0c8,')
		print '{0: <15}  {1}'.format("",							' r0_x, theflip, snapcatcher,')
		print '{0: <15}  {1}'.format("",							' glyxbaer, D4rk5in, travisgoodspeed')
		print '{0: <15}  {1}'.format("",							'  and the whole '+self.ansi.GREEN+'@shackspace...'+self.ansi.END)
		print '  '