import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyUI.UI_MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)    
        self.setupUi(self)
        self.sned.clicked.connect(self.send_email)

        with open('./auth_pwd.cfg', 'r') as f:
            for line in f:
                self.auth_pwd = line
    
    def verification(self):
        subject = self.subtitle.text()
        sender = self.sender.text()
        receiver = self.receiver.text()
        content = self.content.toPlainText()
        for element in [subject, sender, receiver, content]:
            if element == '':
                return False
        return True

    def send_email(self):
        if self.verification():
            content = MIMEMultipart()
            content['subject'] = self.subtitle.text()
            content['from'] = self.sender.text()
            content['to'] = self.receiver.text()
            content.attach(MIMEText(self.content.toPlainText()))

            with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(self.sender.text(), self.auth_pwd)
                    smtp.send_message(content)
                    self.statusBar.showMessage('Complete sending of e-mail.')
                except Exception as e:
                    self.statusBar.showMessage('Error message: ', e)
        else:
            self.statusBar.showMessage('Please write content.')
