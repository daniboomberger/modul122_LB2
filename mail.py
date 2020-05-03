import configuration
import smtplib
import client
from string import Template

#class to write mail            
class mail():

    def __init__(self):
        self.mail_text = ''

    def writeMail(self, invoice_data):
        try:
            mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            mailserver.ehlo()
            mailserver.login(configuration.EMAIL_USER, configuration.EMAIL_PASSWORD)
            mailserver.sendmail(configuration.EMAIL_USER, sending_to, 'mail_text')
            mailserver.close()
            print ('Sent!')
        except:
            print("couldnt send the e-mail")
    
    def prepareMail(self, invoice_data):
        template_mail_text = open(configuration.TEMPLATE_EMAIL).read()
        template_mail =  Template(template_mail_text)

        self.mail_text = template_mail.substitute(
            customer_name = invoice_data[16], 
            receipt_date = ,
            receipt_time = ,
            invoice_number = ,
            ftp_server = 
        )   
         