import BaseHTTPServer, SimpleHTTPServer, time
from urlparse import urlparse

PORT = 1212

ips = []

class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if len(self.path)>5:
            ip = self.client_address[0]
            print '['+time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime())+'] '+ip
            f = open(str(ip), 'a')
            f.write('['+time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime())+'] '+self.path[1:]+'\n')
            f.close()
        self.wfile.write("m16 is a noob")

server_address = ("", PORT)
server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
server.serve_forever()