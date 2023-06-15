from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import json
import time

import handler

exit_thread = False
exited_thread = False


#NOTE must be called from a thread that isn't server_target
def shutdown():
    global exit_thread


    exit_thread = True


class YDLHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        print(f"Recieved POST request: {self.path}")

        #check that request is valid

        #pass to relevant request handler


        raw_data = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(raw_data)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        #TODO this should give an actual status
        self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))

        op = handler.HandlerSingleDownload(data["url"], "mp4", "/downloads")
        handler.add_handler_operation(op)

#NOTE if this needs an additional argument, ensure start_server also recieves an additional argument
#NOTE if changing defaults here, change defaults in start_server
def server_target(address:str="127.0.0.1", port:int=8000):
    global exited_thread, exit_thread


    #HTTPServer only performs basic security checks, but we're binding to loopback
    #so this doesn't need to be all that secure, nobody is going to be accessing it
    #other than local users. as long as we're limited to the local machine, we're fine
    server_address = (address, port)
    _http_server = HTTPServer(server_address, YDLHTTPRequestHandler)
    _http_server.socket.settimeout(1)
    print(f"<Server> Listening at {address}:{port}")

    while True:
        if exit_thread:
            break

        _http_server.handle_request()

    exited_thread = True
    print("<Server> Exited cleanly.")

def start_server(address:str="127.0.0.1", port:int=8000, *args,**kwargs):
    server_thread = threading.Thread(target=server_target, args=[address, port, *args], kwargs=kwargs)
    server_thread.start()
    return server_thread