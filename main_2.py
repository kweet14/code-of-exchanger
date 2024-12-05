import sys
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRegExp
from exchanger import Ui_MainWindow
from pay import Ui_Dialog
from currency_converter import CurrencyConverter
from error import Ui_Dialog_2

class CurrencyConv(QtWidgets.QMainWindow):
    def __init__(self):
        super(CurrencyConv, self).__init__()
        self.exchanger = Ui_MainWindow()
        self.exchanger.setupUi(self)
        self.init_UI_MainWindow()

        self.push_button_pressed = False

    def init_UI_MainWindow(self):
        self.setWindowTitle('Обменный пункт валют')

        self.exchanger.input_currency.setPlaceholderText('EUR')
        self.exchanger.output_currency.setPlaceholderText('USD')
        self.exchanger.input_amount.setPlaceholderText('100')

        self.exchanger.output_amount.setReadOnly(True)

        self.exchanger.input_currency.textChanged.connect(self.format_currency_input)
        self.exchanger.output_currency.textChanged.connect(self.format_currency_input)

        currency_regex = QRegExp('[A-Za-z]{1,3}') #https://stackoverflow.com/questions/15829782/how-to-restrict-user-input-in-qlineedit-in-pyqt
        currency_validator = QtGui.QRegExpValidator(currency_regex, self)
        self.exchanger.input_currency.setValidator(currency_validator)
        self.exchanger.output_currency.setValidator(currency_validator)

        amount_validator = QtGui.QIntValidator(0, 9999999, self)  # https://www.pythonguis.com/docs/qlineedit-widget/
        self.exchanger.input_amount.setValidator(amount_validator)

        self.exchanger.pushButton_2.setEnabled(False)

        self.exchanger.pushButton.clicked.connect(self.converter)
        self.exchanger.pushButton_2.clicked.connect(self.show_dialog)

        self.exchanger.input_currency.textChanged.connect(self.update_buttons_state)
        self.exchanger.input_amount.textChanged.connect(self.update_buttons_state)
        self.exchanger.output_currency.textChanged.connect(self.update_buttons_state)

    def format_currency_input(self):
        sender = self.sender()
        text = sender.text().upper()[:3]
        sender.setText(text)

    def update_buttons_state(self):
        input_currency = self.exchanger.input_currency.text()
        input_amount = self.exchanger.input_amount.text()
        output_currency = self.exchanger.output_currency.text()

        if input_currency and input_amount and output_currency:
            self.exchanger.pushButton.setEnabled(True)
        else:
            self.exchanger.pushButton.setEnabled(False)

    def converter(self):
        try:
            c = CurrencyConverter()
            input_currency = self.exchanger.input_currency.text()
            input_amount = int(self.exchanger.input_amount.text())
            output_currency = self.exchanger.output_currency.text()

            output_amount = round(c.convert(input_amount, '%s' % (input_currency), '%s' % (output_currency)), 2)
            self.exchanger.output_amount.setText(str(output_amount))

            self.push_button_pressed = True
            self.exchanger.pushButton_2.setEnabled(True)

        except Exception as e:
            self.show_error_dialog()

    def show_dialog(self):  # https://ru.stackoverflow.com/questions/992221/Открыть-новое-окно-при-нажатии-кнопки-pyqt5-qt-designer
        if self.push_button_pressed:
            self.pay = mywindow2()
            self.pay.show()
            self.close()

    def show_error_dialog(self):
        self.error_dialog = Ui_Dialog_2()
        self.error_window = QtWidgets.QMainWindow()
        self.error_dialog.setupUi(self.error_window)
        self.error_window.show()

        QtCore.QTimer.singleShot(2000, self.restart_application)

    def restart_application(self):  #https://ru.stackoverflow.com/questions/1074592/Как-в-pyqt-при-нажатии-на-кнопку-закрыть-окно-и-открыть-новое
        QtCore.QCoreApplication.quit()
        time.sleep(1)
        os.execl(sys.executable, sys.executable, *sys.argv)


class mywindow2(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow2, self).__init__()
        self.pay = Ui_Dialog()
        self.pay.setupUi(self)

        self.pay.pushButton_3.clicked.connect(self.on_push_button_3_click)

        self.pay.lineEdit.textChanged.connect(self.update_pushButton_3_state)
        self.pay.lineEdit_2.textChanged.connect(self.update_pushButton_3_state)

        rockwell_font = QFont('Rockwell', 12)
        self.pay.lineEdit.setFont(rockwell_font)
        self.pay.lineEdit_2.setFont(rockwell_font)

        self.update_pushButton_3_state()

    def update_pushButton_3_state(self):
        if self.pay.lineEdit.text() and self.pay.lineEdit_2.text():
            self.pay.pushButton_3.setEnabled(True)
        else:
            self.pay.pushButton_3.setEnabled(False)

    def on_push_button_3_click(self):
        self.pay.pushButton_3.setText('УСПЕШНО')

        QtCore.QTimer.singleShot(2000, self.close_window)

    def close_window(self):
        self.close()


app = QtWidgets.QApplication([])
application = CurrencyConv()
application.show()

sys.exit(app.exec())