import re

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

v = [
     "http://vimeo.com/28257653",
     "http://www.vimeo.com/28257653",
     "www.vimeo.com/28257653",
     "vimeo.com/28257653",
     "28257653"
    ]


regex_y = r'.*(?:v=|/v/|^)(?P<id>[^&]*)'
regex_v = r'.*/(?P<id>\d+)'
#regex = r"^((?:.*)(?=&)|(?:.*)$)"
#regex = r".*v=(.*)&|.*v=(.*)[^&]?"

#print "RegularExpression: "+regex+"\n_____________"

regex_y = re.compile(regex_y)

for url in y:
    erg = regex_y.match(url)
    #print "## "+url+" ##"
    try:
        #print "( ) "+erg.group()
        if erg.group('id'): print erg.group('id')+" | "+url
    except: pass
    #assert erg == "M14Pnulj-j8"

regex_v = re.compile(regex_v)

for url in v:
    erg = regex_v.match(url)
    #print "## "+url+" ##"
    try:
        #print "( ) "+erg.group()
        if erg.group('id'): print erg.group('id')+" | "+url
    except: pass
    #assert erg == "M14Pnulj-j8"
