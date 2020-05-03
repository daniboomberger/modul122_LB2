import create_invoice_text
import datetime
import create_invoice_xml
#class to prepare data for xml and txt
class prepareInvoiceData():

    def __init__(self):
        self.invoice_data = []
        self.invoice_position_data = []
        self.calculated_price = 0.00
        self.calculated_date = ''
        self.calculated_total_with_vat = 0.00
        self.calculated_vat = 0.00
        self.vat = ''
    
    def prepare_data(self, data):
        string_data = str(data)
        string_data = string_data.replace('\\r\\n', ';')
        string_data = string_data.split(';')
        for splitted_data in string_data:
            self.invoice_data.append(splitted_data)
        self.calculateDate()
        self.calculateInvoicePos()
        create_invoice_text.createInvoice().writeInvoice(self.invoice_data, datetime.datetime.strftime(self.calculated_date, "%d.%m.%Y"), self.invoice_position_data, self.calculated_price)
        create_invoice_xml.createInvoiceXml().createXml(self.invoice_data, datetime.datetime.strftime(self.calculated_date, "%d.%m.%Y"), self.invoice_position_data, self.calculated_price, self.calculated_total_with_vat, self.vat)
    
    def calculateDate(self):
        invoice_date = datetime.datetime.strptime(self.invoice_data[3], "%d.%m.%Y")
        self.calculated_date = invoice_date + datetime.timedelta(days=int(self.invoice_data[5].replace('ZahlungszielInTagen_', '')))
    
    def calculateInvoicePos(self):
        invoice_integer = 19
        for y in range(0, int((len(self.invoice_data) - 18) / 7)):
            self.invoice_position_data.append([])
            for i in range(0, 7):
                self.invoice_position_data[y].append(self.invoice_data[invoice_integer + i])
                if i  ==  6:
                    invoice_integer = invoice_integer + 7
                    self.calculated_price = round(self.calculated_price, 2) + round(float(self.invoice_position_data[y][5]), 2)
        self.calculateVAT(self.invoice_position_data[y][6])
    
    def calculateVAT(self, vat_percentage):
        self.vat = vat_percentage
        vat = vat_percentage.replace('MWST_', '').replace('%', '')
        self.calculated_total_with_vat = round(self.calculated_price, 2) * round(float(vat) / 100.0, 2)
            
        