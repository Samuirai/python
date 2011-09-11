# author: Samuirai (Fabian Faessler)
# email: fabi@fabif.de
""" 
This is a RegularExpression test, which extracts a Video ID from YouTube or Vimeo URLs. 
It is for my website www.penspinningonline.com, where Users can add their videos, and they do it with all kind of Video URLs.
"""

import re

# Some YouTube Urls
y = [
     "http://www.youtube.com/watch?v=M14Pnulj-j8&feature=feedf",
     "www.youtube.com/watch?v=M14Pnulj-j8&feature=feedf",
     "youtube.com/watch?v=M14Pnulj-j8&feature=feedf&asd=lol",
     "M14Pnulj-j8&feature=feedf",
     "http://www.youtube.com/watch?v=M14Pnulj-j8",
     "www.youtube.com/watch?v=M14Pnulj-j8",
     "youtube.com/watch?v=M14Pnulj-j8",
     "M14Pnulj-j8",
     "http://www.youtube.com/v/M14Pnulj-j8",
     "www.youtube.com/v/M14Pnulj-j8",
     "youtube.com/v/M14Pnulj-j8",
    ]

#Some vimeo.com URLs
v = [
     "http://vimeo.com/28257653",
     "http://www.vimeo.com/28257653",
     "www.vimeo.com/28257653",
     "vimeo.com/28257653",
     "28257653"
    ]

#regex for youtube and for vimeo
regex_y = r'.*(?:v=|/v/|^)(?P<id>[^&]*)'
regex_v = r'.*/(?P<id>\d+)'

#print "RegularExpression: "+regex+"\n_____________"

regex_y = re.compile(regex_y)

for url in y:
    erg = regex_y.match(url)
    #print "## "+url+" ##"
    try:
        if erg.group('id'): print erg.group('id')+" | "+url
    except: pass

regex_v = re.compile(regex_v)

for url in v:
    erg = regex_v.match(url)
    try:
        #print "( ) "+erg.group()
        if erg.group('id'): print erg.group('id')+" | "+url
    except: pass
