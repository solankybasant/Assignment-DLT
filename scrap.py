import http.server
import urllib.request
import re
import json
import ssl  

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':

            url = 'http://time.com'

            context = ssl._create_unverified_context()

            response = urllib.request.urlopen(url, context=context)
            content = response.read().decode('utf-8')

            arr = []
            syntax = r'<li class="latest-stories__item">\s*<a[^>]*href="([^"]+)">\s*<h3[^>]*class="latest-stories__item-headline">([^<]+)<\/h3>\s*<\/a>[\s\S]*?<\/li>'
            matches = re.finditer(syntax, content)

            for match in matches:
                link = match.group(1)
                title = match.group(2).strip()
                arr.append({'title': title, 'link': link})

            json_output = json.dumps(arr, indent=2)

        
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json_output.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

port = 5500
server = http.server.HTTPServer(('localhost', port), MyHandler)
print(f'Starting server on http://localhost:{port}/getTimeStories')
server.serve_forever()
