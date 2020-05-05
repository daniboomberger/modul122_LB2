import ftplib
import create_log

#class to build up connection to FTP Server
class connectionToServer():

    #creates the connection to ftp server
    def connectionToFTP(self, host, user, password, path):
        try:
            self.ftp = ftplib.FTP(host)
            self.ftp.login(user, password)
            self.ftp.cwd(path)
            return self.ftp
        except:
            create_log.log().createLog('could not build connection to ftp server: ' + host)
            