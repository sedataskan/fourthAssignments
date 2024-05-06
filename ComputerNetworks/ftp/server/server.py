from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# create a user for login
authorizer = DummyAuthorizer()
authorizer.add_user("seda", "6653", "files", perm="elradfmw")

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer

# Instantiate FTP server class and listen on 0.0.0.0:21
server = FTPServer(("0.0.0.0", 21), handler)

# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 5

# start FTP server
server.serve_forever()