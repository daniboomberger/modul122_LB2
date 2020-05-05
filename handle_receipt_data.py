import configuration
import os
import handle_client_data
import mail
import datetime

class handleReceiptData():

    def __init__(self):
        self.invoice_data = handle_client_data.string_invoice_data
    
    #handles data from the receipt.txt
    def handleData(self, receipt_text):
        try:
            receipt_datetime = receipt_text[:15]
            receipt_split_datetime = receipt_datetime.split('-')
            receipt_date_string = datetime.datetime.strptime(receipt_split_datetime[0], "%Y%m%d")
            receipt_date = datetime.datetime.strftime(receipt_date_string, "%d.%m.%Y")
            receipt_time_string = datetime.datetime.strptime(receipt_split_datetime[1], "%H%M%S")
            receipt_time = datetime.datetime.strftime(receipt_time_string, "%H:%M:%S")
            mail.mail().prepareMail(self.invoice_data, receipt_date, receipt_time)
        except:
            print('no content')
        
    #reads the string out of the file receipt.txt
    def readReceipt(self, receipt):
        receipt_text = open(receipt).read()
        self.handleData(receipt_text)
        
    #gets receipt from the local folder
    def getReceipt(self):
        files = os.listdir()
        for receipt in files:
            if receipt.startswith('quittung'):
                self.readReceipt(receipt)
    