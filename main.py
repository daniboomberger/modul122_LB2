import configuration
import ftplib
import smtplib


#class to build up connection to FTP Server
class connectionToServer():

    def connectionToFTP(self, host, user, password, path):
        self.ftp = ftplib.FTP(host)
        self.ftp.login(user, password)
        self.ftp.cwd(path)
        return self.ftp

#class to get connection to client FTP server (ftp.haraldmueller.ch) and get invoices
class customerFTP():    

    def __init__(self):
        self.client_ftp = connectionToServer().connectionToFTP(configuration.CUSTOMER_HOST, configuration.CUSTOMER_USER, configuration.CUSTOMER_PASSWORD, configuration.PATH_OUT)
        self.data = []

    #saves invoice data from file in list data, gives invoice data to class prepareInvoiceData to cleanup the data
    def handle_binary(self, more_data):
        more_data = more_data.decode('utf-8')
        self.data.append(more_data)

        string_data = str(self.data)
        prepareInvoiceData().prepare_data(string_data.replace('[',''))
        

    def getFileFromCustomerFTP(self):
        files = self.client_ftp.nlst()
    
        for file in files:
            if file.endswith(configuration.FILE_ENDING):  
                self.client_ftp.retrbinary("RETR " + file , self.handle_binary)

#class to prepare data for xml and txt
class prepareInvoiceData():

    def __init__(self):
        self.invoice_data = []
    
    def prepare_data(self, data):
        string_data = str(data)
        string_data = string_data.replace('\\r\\n', ';')
        string_data = string_data.split(';')
        for splitted_data in string_data:
            self.invoice_data.append(splitted_data)
        
class mail():

    def writeMail(self):

        sending_to = 'dani.boomberger@gmail.com'
        #mail_text = 'Sehr geehrter s\n Am s um s wurde die erfolgreiche Bearbeitung der s vom Zahlungssystem <s> gemeldet.\n Mit Freundlichen Grüssen\n Din Jakupi'

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(configuration.EMAIL_USER, configuration.EMAIL_PASSWORD)
            server.sendmail(configuration.EMAIL_USER, sending_to, 'mail_text')
            server.close()

            print ('Sent!')
        except:
            print("couldnt send the e-mail")



        

if __name__ == '__main__':
    customerFTP().getFileFromCustomerFTP()
    #mail().writeMail()
