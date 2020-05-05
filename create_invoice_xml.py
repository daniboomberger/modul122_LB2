import configuration
from string import Template
import create_log

class createInvoiceXml():

    def __init__(self): 
        self.finished_invoice_text = ''
        self.position_text = ''
        self.number_positions = 0
        self.vat_total_position = 0
        self.vat_amount = 0
    
    #creates invoice.xml file locally
    def createXml(self, invoice_data, calculated_date, position_data,calculated_price, calculated_total_with_vat, vat):
        invoice_xml_text = open(configuration.TEMPLATE_INVOICE_XML).read()
        self.createPositions(position_data, invoice_data)
        filename = open(invoice_data[7] + "_" + invoice_data[0].replace('\'Rechnung_', '') + "_invoice.xml", "w", encoding='utf-8')
        template_invoice_xml  = Template(invoice_xml_text)

        try:
            invoice_xml = template_invoice_xml.substitute(
                invoice_number = invoice_data[0].replace('\'Rechnung_', ''), 
                date = invoice_data[3],
                mail = invoice_data[13],
                receiver_number_4 = invoice_data[15][:4],
                receiver_number_17 = invoice_data[15],
                receiver_name = invoice_data[16],
                receiver_plz = invoice_data[18][:4],
                receiver_location = invoice_data[18][5:],
                firmname = invoice_data[8], 
                firm_address = invoice_data[10],
                firm_plz = invoice_data[11][:4],
                firm_location = invoice_data[11][5:],
                calculated_date = calculated_date,
                vat_number = invoice_data[12],
                invoice_xml_position = self.position_text,
                number_positions = self.number_positions, 
                calculated_total = calculated_price, 
                vat_amount = vat, 
                calculated_total_with_vat = calculated_total_with_vat,
                vat = vat
            )

            filename.write(invoice_xml)
        except:
            create_log.log().createLog('failed to create' + filename)
    
    #creates dynamic string for xml invoice positions
    def createPositions(self, position_data, invoice_data): 
        invoice_xml_positions_text = open(configuration.TEMPLATE_INVOICE_XML_POSITION).read()
        invoice_xml_position = Template(invoice_xml_positions_text)
        
        try:
            for i in range(0, len(position_data)):
                self.calculateVatPos(position_data, i)
                self.position_text += invoice_xml_position.substitute(
                        position_id = position_data[i][1],
                        item_description = position_data[i][2],
                        item_date = invoice_data[3],
                        quantity = position_data[i][3], 
                        total_item_amount = position_data[i][5], 
                        total_item_amount_vat = self.vat_total_position,
                        vat = position_data[i][6],
                )
                self.number_positions = self.number_positions + 1
        except:
            create_log.log().createLog('failed to create position for xml')
    
    #calculates the total of each dynamic invoice positon for the xml 
    def calculateVatPos(self, position_data, i): 
        self.vat_total_position = round(float(position_data[i][5])) * round(float(position_data[i][6].replace('MWST_', '').replace('%', '')) / 100.0)
        self.vat_amount = self.vat_amount + self.vat_total_position 