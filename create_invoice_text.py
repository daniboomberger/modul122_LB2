import configuration
from string import Template

class createInvoice():

    def __init__(self):
        self.finished_invoice_text = ''
        self.positions_text = ''

    def writeInvoice(self, invoice_data, calculated_date, invoice_positions, calculated_price):
        invoice_text = open(configuration.TEMPLATE_INVOICE_TEXT).read()
        invoice_template = Template(invoice_text)
        self.createInvoicePosString(invoice_positions)
        calculated_price = "{:10.2f}".format(calculated_price)
        filename = open(invoice_data[1].replace('Auftrag_', '') + "_" + invoice_data[0].replace('\'Rechnung_', '') + ".txt", "w", encoding='utf-8')
        
        try:
            self.finished_invoice_text = invoice_template.substitute(
                firmname = invoice_data[8],
                name = invoice_data[9],
                address = invoice_data[10],
                firm_location = invoice_data[11],
                uid = invoice_data[12],
                location = invoice_data[2],
                date = invoice_data[3],
                customer_number = invoice_data[7],
                job_number = invoice_data[1].replace('Auftrag_', ''), 
                invoice_number = invoice_data[0].replace('\'Rechnung_', ''),
                receiver_firm = invoice_data[16],
                receiver_firm_address = invoice_data[17],
                receiver_firm_location = invoice_data[18],
                calculated_date = calculated_date,
                positions_text = self.positions_text,
                total_price = calculated_price
            )

            filename.write(self.finished_invoice_text)
        except:
            print('failed to create new file')
    
    def createInvoicePosString(self, position_data):
        invoice_position_template_text = open(configuration.TEMPLATE_INVOICE_POSITION).read()
        invoice_postion_template = Template(invoice_position_template_text)

        for i in range(0, len(position_data)):
            self.positions_text += invoice_postion_template.substitute(
                    position_id = position_data[i][1],
                    position_description = position_data[i][2],
                    quantity = position_data[i][3],
                    price_pre_quantity = position_data[i][4],
                    price = position_data[i][5],
                    mwst = position_data[i][6]
            )
    
    
        

         