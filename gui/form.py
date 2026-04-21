from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.form_ui import Ui_Form
from logic.encryptor import Encryptor

if TYPE_CHECKING:
    from main.mainwindow import MainWindow


class FormWidget(Ui_Form, QWidget):

    def __init__(self, parent: "MainWindow"):
        super().__init__(parent=parent)
        self.setMinimumSize(400, 400)
        self.setupUi(self)
        self.encryptor = Encryptor()

        self.pValueSpinBox.valueChanged.connect(self.set_p_value)
        self.qValueSpinBox.valueChanged.connect(self.set_q_value)
        self.nValueTextEdit.textChanged.connect(self.set_n_value)
        self.cypherPushButton.clicked.connect(self.cypher)
        self.decypherPushButton.clicked.connect(self.decypher)
        self.euclideanCheckBox.clicked.connect(self.set_mode)

    def cypher(self):
        self.encryptor.text = self.inputTextEdit.toPlainText()
        cyphered_text = self.encryptor.cypher()
        self.setPublicKey()
        self.nValueTextEdit.setText(str(self.encryptor.nValue))
        self.fiValueTextEdit.setText(str(self.encryptor.fiValue))
        self.resultTextEdit.setPlainText(str(cyphered_text))

    def decypher(self):
        decyphered_text = self.encryptor.decypher()
        self.setPrivateKey()
        self.inputTextEdit.setPlainText(str(self.encryptor.ciphered_text))
        self.resultTextEdit.setPlainText(str(decyphered_text))
        self.nValueTextEdit.setText(str(self.encryptor.nValue))
        self.fiValueTextEdit.setText(str(self.encryptor.fiValue))

        if not self.pValueSpinBox.value():
            self.pValueSpinBox.setValue(int(self.encryptor.pValue))
            self.set_p_value(self.encryptor.pValue)

        if not self.qValueSpinBox.value():
            self.qValueSpinBox.setValue(int(self.encryptor.qValue))
            self.set_q_value(self.encryptor.qValue)

    def setPublicKey(self):
        self.globalKeyLineEdit.setText(
            f"Key(pub) = (n, e) = ({self.encryptor.nValue}, {self.encryptor.eValue})"
        )

    def setPrivateKey(self):
        self.privateKeyLineEdit.setText(f"Key(priv) = d = ({self.encryptor.dValue})")

    def save_to_txt(self):
        self.encryptor.write_to_txt()

    def open_txt(self):
        self.encryptor.read_from_txt()
        self.privateKeyLineEdit.setText("")
        self.globalKeyLineEdit.setText("")
        self.resultTextEdit.setPlainText("")
        self.nValueTextEdit.setText("")
        self.pValueSpinBox.setValue(int(self.encryptor.pValue))
        self.qValueSpinBox.setValue(int(self.encryptor.qValue))
        self.inputTextEdit.setPlainText(str(self.encryptor.ciphered_text))

    def set_p_value(self, value: int):
        if value:
            self.encryptor.pValue = int(value)

    def set_q_value(self, value: int):
        if value:
            self.encryptor.qValue = int(value)

    def set_n_value(self, value: int):
        if value:
            self.encryptor.nValue = int(value)

    def set_mode(self):
        if self.euclideanCheckBox.isChecked():
            self.encryptor.extendedEuclidean = True
