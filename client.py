import configuration
import connection
import handle_client_data

#class to get connection to client FTP server (ftp.haraldmueller.ch) and get invoices
class customerFTP():    

    def __init__(self):
        self.client_ftp = connection.connectionToServer().connectionToFTP(configuration.CUSTOMER_HOST, configuration.CUSTOMER_USER, configuration.CUSTOMER_PASSWORD, configuration.PATH_OUT)
        self.data = []

    #saves invoice data from file in list data, gives invoice data to class prepareInvoiceData to cleanup the data
    def handle_binary(self, more_data):
        more_data = more_data.decode('utf-8')
        self.data.append(more_data)

        string_data = str(self.data)
        handle_client_data.prepareInvoiceData().prepare_data(string_data.replace('[',''))
        

    def getFileFromCustomerFTP(self):
        files = self.client_ftp.nlst()
    
        for file in files:
            if file.endswith(configuration.FILE_ENDING):  
                self.client_ftp.retrbinary("RETR " + file , open(file, 'wb').write)
                self.client_ftp.retrbinary("RETR " + file , self.handle_binary)
    
    def getDirInfo(self):
        data = []
        self.client_ftp.dir(data.append)
        for line in data:
            print(line) 