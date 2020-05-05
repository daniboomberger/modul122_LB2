import client
import payment
import handle_receipt_data
import mail
import create_zip
import time

def main():
    payment.paymentServer().getReceipt()
    if payment.HasReceipt == 1:
        create_zip.zip().zipInvoice()
        handle_receipt_data.handleReceiptData().getReceipt()
        client.customerFTP().uploadZip()
        create_zip.zip().deleteZip()
        payment.paymentServer().deleteLocal()
        main()
    else:
        client.customerFTP().getFileFromCustomerFTP()
        payment.paymentServer().uploadeFile()
        time.sleep(300)
        main()
main()


