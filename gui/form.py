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

        self.cypherPushButton.clicked.connect(self.cypher)
        self.decypherPushButton.clicked.connect(self.decypher)

    def cypher(self):
        self.encryptor.pValue = self.pValueSpinBox.value()
        self.encryptor.qValue = self.qValueSpinBox.value()
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

    def setPublicKey(self):
        self.globalKeyLineEdit.setText(
            f"Key(pub) = (n, e) = ({self.encryptor.nValue}, {self.encryptor.eValue})"
        )

    def setPrivateKey(self):
        self.privateKeyLineEdit.setText(f"Key(priv) = d = ({self.encryptor.dValue})")
