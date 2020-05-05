import configuration
import connection
import handle_client_data
import os
import create_log

#class to get connection to client FTP server (ftp.haraldmueller.ch) and get invoices
class customerFTP():    

    def __init__(self):
        self.client_ftp_out = connection.connectionToServer().connectionToFTP(configuration.CUSTOMER_HOST, configuration.CUSTOMER_USER, configuration.CUSTOMER_PASSWORD, configuration.PATH_OUT)
        self.client_ftp_in = connection.connectionToServer().connectionToFTP(configuration.CUSTOMER_HOST, configuration.CUSTOMER_USER, configuration.CUSTOMER_PASSWORD, configuration.PATH_IN)
        self.data = []

    #saves invoice data from file in list data, gives invoice data to class prepareInvoiceData to cleanup the data
    def handle_binary(self, more_data):
        more_data = more_data.decode('utf-8')
        self.data.append(more_data)

        string_data = str(self.data)
        handle_client_data.prepareInvoiceData().prepare_data(string_data.replace('[',''))
        
    #gets files from ftp .data file from the ftp server 
    def getFileFromCustomerFTP(self):
        files = self.client_ftp_out.nlst()

        for file in files:
            if file.endswith(configuration.FILE_ENDING):
                self.client_ftp_out.retrbinary("RETR " + file , self.handle_binary)
                self.deleteInvoiceFilesFtp(file) 
                break
    
    #deletes .data file on the ftp server 
    def deleteInvoiceFilesFtp(self, file):
        self.client_ftp_out.delete(file)
    
    #uploads the created zip data (with invoice.txt and receipt.txt)
    def uploadZip(self):
        try:
            files = os.listdir()
            for zipfile in files:
                if zipfile.endswith('.zip'):
                    filename = open(zipfile, 'rb')
                    self.client_ftp_in.storbinary('STOR ' + zipfile , filename)
        except:
            create_log.log().createLog('failed upload of the zip file:' + zipfile)
    
    #function to check what is inside the folder ftp server
    def getDirInfo(self):
        data = []
        self.client_ftp_out.dir(data.append)
        for line in data:
            print(line)
                
    