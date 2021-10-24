from http.server import BaseHTTPRequestHandler, HTTPServer
import json, logging
from logic.hello_functions import *

log_level = os.environ.get('PYLOGLEVEL', "INFO")
logging.basicConfig(level=log_level)

class HandleRequests(BaseHTTPRequestHandler):

    #use FastAPI or Flask for more routes / complex api.

    def _exit_with_bad_request(self):
        self.send_response(400)
        logging.debug('Request path problem ( not matched or username is not letters only )')
        self.end_headers()

    def do_GET(self):
        user = get_user_and_validate_path(self.path);
        if ( user == "200" ):
            #health check
            self.send_response(200)
            self.end_headers()
        elif ( user != -1): 
            (code, response) = get_birthday_response(user)
            self.send_header('Content-Type', 'application/json')
            self.send_response(code)
            self.end_headers()
            self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
        else:
            self._exit_with_bad_request()

    def do_PUT(self):
        user = get_user_and_validate_path(self.path);
        if ( user != -1): 
            code = upsert_and_validate_json(user,self.rfile.read(int(self.headers['content-length'] or 0)))
            self.send_response(code)
            self.end_headers()
        else:
            self._exit_with_bad_request()


    #other methods like POST , DELETE get 501 and html response

HTTPServer(('', 80), HandleRequests).serve_forever()
 