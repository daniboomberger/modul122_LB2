import configuration
import connection
import os

class paymentServer():

    def __init__(self):
        self.payment_ftp_in = connection.connectionToServer().connectionToFTP(configuration.PAYMENT_HOST, configuration.PAYMENT_USER, configuration.PAYMENT_PASSWORD, configuration.PATH_IN)
        self.payment_ftp_out = connection.connectionToServer().connectionToFTP(configuration.PAYMENT_HOST, configuration.PAYMENT_USER, configuration.PAYMENT_PASSWORD, configuration.PATH_OUT)

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

    def getReceipt(self):
        data = []
        self.payment_ftp_out.dir(data.append)
        for indata in data:
            print(indata)

        files = self.payment_ftp_out.nlst()
    
        for file in files:
            if file.startswith('quittungsfile'):  
                self.payment_ftp_out.retrbinary("RETR " + file , open(file, 'wb').write)

    def deleteReceiptFile(self):
        files = self.payment_ftp_out.nlst()
    
        for file in files:
            if file.startswith('quittungsfile'):  
                self.payment_ftp_out.delete(file)