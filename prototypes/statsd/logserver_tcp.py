import SocketServer

from JumpScale import j

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        data=self.request.recv(20000)
        while len(data)>0:
            if data=="\x04":
                data==""            
            if data=="":
                print "DONE"
                break
            data = self.request.recv(1024)
            print data,
        # self.request.sendall("1")

if __name__ == "__main__":
    HOST, PORT = "localhost", 1001

    # Create the server, binding to localhost on port 9999
    print "listen on 1001"
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()