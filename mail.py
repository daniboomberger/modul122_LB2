import configuration
import smtplib
import client
import create_log
import handle_client_data
from string import Template
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

#class to write mail            
class mail():

    def __init__(self):
        self.mail_text = ''
        self.subject = ''
        self.mail_to = ''
        self.zip_attachment = ''
        self.mail_message = MIMEMultipart()
    
    #writes a mail from my 'dani.boomberger@gmail.com'
    def writeMail(self):
        self.createMailMessage()
        try:
            mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            mailserver.ehlo()
            mailserver.login(configuration.EMAIL_USER, configuration.EMAIL_PASSWORD)
            mailserver.send_message(self.mail_message)
            mailserver.close()
        except:
            create_log.log().createLog('failed to send mail')
    
    #code to prepare the mail body with an template
    def prepareMail(self, invoice_data, receipt_date, receipt_time):
        self.subject = invoice_data[0].replace('\'', '').replace('_', ' ')
        self.mail_to = 'dani.boomberger@gmail.com'#invoice_data[13]
        template_mail_text = open(configuration.TEMPLATE_EMAIL).read()
        template_mail =  Template(template_mail_text)

        try:
            self.mail_text = template_mail.substitute(
                customer_name = invoice_data[16], 
                receipt_date = receipt_date,
                receipt_time = receipt_time,
                invoice_number = invoice_data[0].replace('_', ' '),
                ftp_server = configuration.PAYMENT_HOST
            )
            self.writeMail()
        except:
            create_log.log().createLog('could not create mail text')
    
    #creates the mail message and the attachments
    def createMailMessage(self):
        self.attach_zip()
        self.mail_message['Subject'] = 'Erfolgte Verarbeitung ' + self.subject
        self.mail_message['FROM'] = configuration.EMAIL_USER
        self.mail_message['To'] = self.mail_to
        message = self.mail_text
        self.mail_message.attach(MIMEText(message, 'plain'))
        self.mail_message.attach(self.zip_attachment)
    
    #attaches the local created zip file to the mail
    def attach_zip(self):
        filename = handle_client_data.string_invoice_data[0].replace('\'', '') + '.zip'
        file_attachment = MIMEBase('application', 'octate-stream')
        file_attachment.set_payload(open( handle_client_data.string_invoice_data[0].replace('\'', '') + '.zip', 'rb').read())
        encoders.encode_base64(file_attachment)
        file_attachment.add_header('Content-Disposition', 'attachment; filename=' + filename)
        self.zip_attachment = file_attachment
                 