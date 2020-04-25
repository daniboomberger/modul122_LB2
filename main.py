import configuration
import ftplib

class customerFTP():
    
    #open connection to customer FTP
    def __init__(self):
        self.ftp = ftplib.FTP(configuration.CUSTOMER_HOST)
        self.ftp.login(configuration.CUSTOMER_USER, configuration.CUSTOMER_PASSWORD)
        self.ftp.cwd(configuration.CUSTOMER_PATH)

    def getFileFromCustomerFTP(self):
        #create local file
        fileName  = configuration.CUSTOMER_FILE
        localFile = open(fileName, 'wb')

        #get remote file from customer FTP Server
        self.ftp.retrbinary('RETR %s' % fileName, localFile.write)
        
        localFile.close()
        self.ftp.close()



if __name__ == '__main__':
    customerFTP().getFileFromCustomerFTP()
