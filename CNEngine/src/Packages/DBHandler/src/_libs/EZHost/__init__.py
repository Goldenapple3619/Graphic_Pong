from .libs import *

class MyServer:
    def __init__(self, host='127.0.0.1', port=8082):
        self.HOST,self.PORT = host,port

        self.create_access()
        self.setup_connection()

        print(f"Serving on port {port} and host {host}")
        print(f"link: http://{host}:{port}")

    def create_access(self):
        self.connection_point = socket(AF_INET,SOCK_STREAM)

    def setup_connection(self):
        self.connection_point.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.connection_point.bind((self.HOST,self.PORT))
        self.connection_point.listen(5)
        #self.connection_point.setblocking(False)

    def launch_loop(self, func, args=None):
        while True:
            connection,address = self.connection_point.accept()
            request = connection.recv(1024).decode('utf-8')
            string_list = request.split(' ')
            if args is not None:
                func(address, string_list, connection, args)
            else:
                func(address, string_list, connection)