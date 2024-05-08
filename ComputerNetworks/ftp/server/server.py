from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def runServer():
    """
    Uygulamayi calistirir. FTP sunucusunu baslatir.
    """
    authorizer = DummyAuthorizer()
    # username, password, directory, permission
    authorizer.add_user("seda", "6653", "files", perm="elradfmw")

    handler = FTPHandler  # FTPHandler sinifindan bir nesne olusturulur.
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 21), handler)  # FTP sunucusu olusturulur.
    server.serve_forever()  # FTP sunucusunun acik kalmasi saglanir.


runServer()  # Uygulama calistirilir.
