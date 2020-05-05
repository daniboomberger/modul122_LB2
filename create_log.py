import handle_client_data
from datetime import datetime
import payment

class log:

    #creates a log file for every invoice to show what append during the progress
    def createLog(self, message):
        payment.paymentServer().deleteLocal()
        logfile = open( 'log.txt', 'w')
        logfile.writelines(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' ' + message)
        logfile.close

        