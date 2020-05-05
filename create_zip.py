import zipfile
import os
import handle_client_data

class zip():

    def zipInvoice(self):
        zip_file = zipfile.ZipFile(handle_client_data.string_invoice_data[0].replace('\'', '') + '.zip', 'w', zipfile.ZIP_DEFLATED)
        files = os.listdir()
        for file in files: 
            if file.endswith('.txt'):
                zip_file.write(file)
    
    def deleteZip(self):
        files = os.listdir()
        for zipfile in files:
            if zipfile.endswith('.zip'):
                os.remove(zipfile)