from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def runServer():
    authorizer = DummyAuthorizer()
    authorizer.add_user("seda", "6653", ".", perm="elradfmw")

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Instantiate FTP server class and listen on 0.0.0.0:21
    server = FTPServer(("127.0.0.1", 21), handler)
    server.serve_forever()

runServer()