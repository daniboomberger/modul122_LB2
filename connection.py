import ftplib 

#class to build up connection to FTP Server
class connectionToServer():

    def connectionToFTP(self, host, user, password, path):
        self.ftp = ftplib.FTP(host)
        self.ftp.login(user, password)
        self.ftp.cwd(path)
        return self.ftp