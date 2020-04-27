import configuration
import smtplib
import client

#class to write mail            
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