import configuration
import connection
import os

HasReceipt = 0

class paymentServer():

    def __init__(self):
        self.payment_ftp_in = connection.connectionToServer().connectionToFTP(configuration.PAYMENT_HOST, configuration.PAYMENT_USER, configuration.PAYMENT_PASSWORD, configuration.PATH_IN)
        self.payment_ftp_out = connection.connectionToServer().connectionToFTP(configuration.PAYMENT_HOST, configuration.PAYMENT_USER, configuration.PAYMENT_PASSWORD, configuration.PATH_OUT)
    
    #uploads File onto ftp server (payment) to get receipt.txt
    def uploadeFile(self):
        data = []
        self.payment_ftp_in.dir(data.append)
        for indata in data:
            print(indata)
   
        files = os.listdir()
        for invoice in files:
            if (invoice.endswith('.txt')) or invoice.endswith('.xml'):
                filename = open(invoice, 'rb')
                self.payment_ftp_in.storbinary('STOR ' + invoice , filename)

    #gets the receipt from the payment ftp server 
    def getReceipt(self):
        global HasReceipt
        HasReceipt = 0
        files = self.payment_ftp_out.nlst()
        for file in files:
            if file.startswith('quittungsfile'):  
                self.payment_ftp_out.retrbinary("RETR " + file , open(file, 'wb').write)
                self.payment_ftp_out.delete(file)
                HasReceipt = 1 
    
    #deltes all downloaded files from the ftp server
    def deleteLocal(self):
        try:
            files = os.listdir()
            for file in files:
                if file.startswith('quittungsfile') or file.endswith('.txt') or file.endswith('.xml'):
                    os.remove(file)
        except:
            print('no file')


    #function to check what is inside the payment folders (currently not called) (just call the functions to test)  
    def getDirInfoIn(self):
        data = []
        self.payment_ftp_in.dir(data.append)
        for line in data:
            print(line)
    
    def getDirInfoOut(self):
        data = []
        self.payment_ftp_out.dir(data.append)
        for line in data:
            print(line)