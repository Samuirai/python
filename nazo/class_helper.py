
def verbose(_level, _message, _verbose):
	if _level == _verbose:
		print "> "+_message
			
def print_header(_text):
	print "___["+_text+"]____________________"
	
def print_disclaimer():
	print_header("Disclaimer")
	print "nazo is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied\
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more\
details."
	print ""
	print "Whatever you do with this tool is uniquely your responsibility. If you are not authorized to test\
a specific bbcode form be aware that such action might get you in trouble with a lot of law\
enforcement agencies."
	print "I wrote this tool to help bbcode parser developer or penetration testers - who are \
authorized - to test a product or their code for security issues."
	print ""
	print "With Great Power Comes Great Responsibility!"
	print ""

def print_version(_version):
	print_header("Version")
	print '{0:.<15}  {1}'.format("version",		_version+"v")
	print '{0:.<15}  {1}'.format("date",		'7 February 2012')
	print '{0:.<15}  {1}'.format("coder",		'smrrd')
	print '{0:.<15}  {1}'.format("thx to",		'momo, hdznrrd, dop3j0e, rel0c8,')
	print '{0: <15}  {1}'.format("",			'r0_x, theflip, snapcatcher,')
	print '{0: <15}  {1}'.format("",			'glyxbaer, D4rk5in, travisgoodspeed')
	print '{0: <15}  {1}'.format("",			' and the whole @shackspace...')
	print '  '