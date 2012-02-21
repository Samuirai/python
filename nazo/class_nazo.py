import threading, urllib, urllib2, cookielib, re, html5lib, random, hashlib, sys, traceback, random
import class_helper, class_bbcode
from html5lib import treebuilders, treewalkers

class nazo:

    def __init__(self,_form,_resulturl=None,_post={},_data="",_helper=class_helper.helper()):
        try:
            _helper.print_disclaimer()
            self.helper = _helper
            self.stream = None
            self.random = None
            self.bbcode = class_bbcode.bbcode(_helper)
            self.bbcode.create_bbcode_list()
            self.post = _post
            self.data = _data
            self.skip = False
            self.form = _form
            self.start_hash = str(hashlib.sha1(str(random.randint(0,10000))).hexdigest());
            self.end_hash = str(hashlib.sha1(str(random.randint(0,10000))).hexdigest());
            self.random = str(random.randint(11111111,99999999))
            #self.helper.verbose(1,self.helper.ansi.BLUE+"Welcome to nazo - the BBCode XSS Vulnerability scanner"+self.helper.ansi.END)
        except:
            _helper.error("nazo.__init__()")
            _helper.error(traceback.format_exc())
        
    def printResult(self):
        data = ''
        result = {} 
        self.helper.verbose(1,"starting result analyse")
        # typ = typ titel , list of all types belongs to this type, nr all of this type, found injections
        result['abba'] = ['[a][b] [/b][/a]',[1,3,5,7, 9,11,13,15,17,19,21,23,25,27,29,31],0,0]
        result['abab'] = ['[a][b] [/a][/b]',[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32],0,0]

        for bbcode in self.bbcode.bbcode_list_injection:
            if bbcode[2] in result['abba'][1]:
                result['abba'][2] += 1
                if bbcode[1]==2:
                    result['abba'][3] += 1
            if bbcode[2] in result['abab'][1]:
                result['abab'][2] += 1
                if bbcode[1]==2:
                    result['abab'][3] += 1
        self.helper.verbose(1,"print result")
        
        while data != 'e' and data != 'exit':
            print '1: '+result['abba'][0]+'('+str(result['abba'][3])+'/'+str(result['abba'][2])+')'
            print '2: '+result['abab'][0]+'('+str(result['abab'][3])+'/'+str(result['abab'][2])+')'
            
            data = self.helper.input("choose a Type: ")
            liste = []
            if data == '1': liste=result['abba'][1]
            elif data == '2': liste=result['abab'][1]

            for bbcode in self.bbcode.bbcode_list_injection:
                if bbcode[1]==2 and bbcode[2] in liste:
                    print str(bbcode[2])+" | "+str(bbcode[1])+": "+str(bbcode[0][0])
 
        
    def text2dom(self,_text):
        parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
        walker = treewalkers.getTreeWalker("dom")
        dom = parser.parse(_text)
        stream = walker(dom)
        self.stream = stream
    
    def learn_bbcode(self):
        self.skip = False
        check_codes = []
        data=""
        self.helper.verbose(1,"Create BBCode list to try diffrent injection styles and learn something about the possibilities")
        if "img" in [tag[0] for tag in self.bbcode.get_supported_bbcodes()]:
            print "asd"
            for tag in self.bbcode.get_supported_bbcodes():
                if tag[0]=="b" or tag[0]=="u" or tag[0]=="i":
                    print tag
                    for valid_data in self.bbcode.get_valid_data("img"):
                        check_codes.append([("[img]"+valid_data+" ["+tag[0]+"][/"+tag[0]+"][/img]","",""),False])
                        data +="[img]"+valid_data+" ["+tag[0]+"][/"+tag[0]+"][/img]"
                        check_codes.append([("[img]["+tag[0]+"][/"+tag[0]+"]"+valid_data+"[/img]","",""),False])
                        data +="[img]["+tag[0]+"][/"+tag[0]+"]"+valid_data+"[/img]"
                        
                        check_codes.append([("[img]"+valid_data+" ["+tag[0]+"][/img][/"+tag[0]+"]","",""),False])
                        data +="[img]"+valid_data+" ["+tag[0]+"][/img][/"+tag[0]+"]"
                        check_codes.append([("[img]["+tag[0]+"]"+valid_data+"[/img][/"+tag[0]+"]","",""),False])
                        data +="[img]["+tag[0]+"]"+valid_data+"[/img][/"+tag[0]+"]"
                
                
            supported=0
            print data
            (html,result) = self.get_result({self.data: self.start_hash+" "+data+" "+self.end_hash})
            print result
            if result:
                supported=self.bbcode.check_bbcode_list(result,check_codes)
            else:
                supported=self.bbcode.check_bbcode_list(html,check_codes)
            self.helper.verbose(1,"[img] tag allows injected tags like [img][tag][/tag][/img]")
            self.bbcode.tag_in_img = True
    
    # 1
    def check_bbcode(self,_anz=None):
        # DELETED!
        self.skip = False
        self.helper.verbose(1,"Check the BBCodes if they are supported")
        data = ""
        counter = 0
        counter2 = 0
        _all_requests = ""
        if self.random: random.shuffle(self.bbcode.bbcode_list)
        for bbcode in self.bbcode.bbcode_list:
            data += str(bbcode[0][0])
            self.helper.progress_bar(counter2,len(self.bbcode.bbcode_list),"("+str(counter2)+"/"+str(len(self.bbcode.bbcode_list))+")")
            counter += 1
            counter2 += 1
            if _anz:
                if counter >= _anz:
                    self.helper.verbose(2,"partial check next "+str(_anz)+"")
                    (html,result) = self.get_result({self.data: self.start_hash+" "+data+" "+self.end_hash})
                    if result: _all_requests+=str(result)
                    data = ""
                    counter = 0
        (html,result) = self.get_result({self.data: self.start_hash+" "+data+" "+self.end_hash})
        if result: _all_requests+=str(result)
        if _all_requests:
            self.bbcode._supported=self.bbcode.check_bbcode_list(_all_requests,self.bbcode.bbcode_list)
            return 1
        return None
        # DELETED!
    
    def check_bbcode_xss(self):
        self.skip = False
        self.bbcode.create_bbcode_list_injection()
        data = ""
        injected = 0
        counter = 0
        if self.random: random.shuffle(self.bbcode.bbcode_list_injection)
        for bbcode in self.bbcode.bbcode_list_injection:
            self.helper.progress_bar(counter,len(self.bbcode.bbcode_list_injection),"("+str(injected)+"/"+str(counter)+" -> "+str(len(self.bbcode.bbcode_list_injection))+")")
            counter += 1
            data = str(bbcode[0][0])
            (html,result) = self.get_result({self.data: self.start_hash+" "+data+" "+self.end_hash})
            data = ""
            #print html
            if result:
                self.text2dom(result)
            else:
                self.text2dom(html)
            # result stored internaly. now check injection
            if self.check_injection()==2:
                injected+=1
                bbcode[1] = 2
                self.helper.verbose(2,"Injection possible with "+self.helper.ansi.GREEN+bbcode[0][0]+self.helper.ansi.END)
            elif self.check_injection()==1:
                bbcode[1] = 1
                self.helper.verbose(3,"Injection maybe possible with "+self.helper.ansi.GREEN+bbcode[0][0]+self.helper.ansi.END)
            else:
                self.helper.verbose(4,"Injection not possible with "+self.helper.ansi.RED+bbcode[0][0]+self.helper.ansi.END)
                
            if counter>(len(self.bbcode.bbcode_list_injection)*0.01):
                if self.helper.input("10% of [img] BBCodes are checked and no injections found. Do you want to stop this test?",['y','n'],'y') == 'y':
                    break
                
        #print data
        self.helper.verbose(1,str(injected)+"/"+str(len(self.bbcode.bbcode_list_injection))+" tested XSS injections were successfull")
        
    def get_result(self,_post):
        re.DOTALL
        opener = urllib2.build_opener()
        _post.update(self.post)
        login_data = urllib.urlencode(_post)
        response = opener.open(self.form, login_data)
        html = response.read()
        self.helper.verbose(5,"HTML:\n"+html)
        result = html[html.find(self.start_hash)+len(self.start_hash):html.find(self.end_hash)]
        self.helper.verbose(5,"RESULT:\n"+result)
        if not result:
            self.helper.error("Couldn't find the expected hashes: internal Parser error")
            if not self.skip:
                answer = self.helper.input("Do you want to exit now? (Y = yes | n = no | r = see html | s = skip next error): ",["y","n","r","s"],"y")
                if answer.lower()=='y':
                    exit(1)
                elif answer.lower()=='r':
                    print "POST:\n"+str(_post)
                    print
                    print "HTML:\n"+str(html)
                elif answer.lower()=='s':
                    self.skip = True
            else:
                self.helper.error("Skipped this Error. Next Module will reset this skip.")
            result = None
            #result = re.search(self.start_hash+"([.]*)"+self.end_hash,html).group(1)
        return (html,result)
        
    def check_injection(self,stream=None):
        script_tag_open = False
        _injection = 0
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
                            if attr[1] == u'eval()':
                                
                                self.helper.verbose(3," 1: "+str(element))
                                _injection = 2
                            elif u'eval()' in attr or u'eval()' in attr[1]:
                                self.helper.verbose(4," 2: "+str(element))
                                _injection = 1
                            else:
                                self.helper.verbose(4," 3: "+str(element))
                                _injection = 1
            except KeyError:
                pass
            except TypeError:
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
                    if u'eval()' in element['data']:
                        self.helper.verbose(1,"<script> eval injection")
                        self.helper.verbose(2," "+str(element))
                        _injection = 2
                    else:
                        self.helper.verbose(1,"<script>")
                        self.helper.verbose(2," "+str(element))
                        _injection = 1
            except KeyError:
                pass
            except TypeError:
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
                            if u'javascript:eval()' in attr[1]:
                                self.helper.verbose(1,"<a href=...> javascript:eval() injection")
                                self.helper.verbose(2," "+str(element))
                                _injection = 2
            except KeyError:
                pass
            except TypeError:
                pass
            except:
                self.helper.error(traceback.format_exc())
        return _injection
                
                
                
