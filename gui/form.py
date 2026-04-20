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

    def cypher(self):
        self.encryptor.pValue = self.pValueSpinBox.value()
        self.encryptor.qValue = self.qValueSpinBox.value()
        self.encryptor.text = self.inputTextEdit.toPlainText()
        self.pValueResultLabel.setText(str(self.encryptor.pValue))
        self.qValueResultLabel.setText(str(self.encryptor.qValue))
        cyphered_text = self.encryptor.cypher()
        self.setPublicKey()
        self.resultTextEdit.setPlainText(str(cyphered_text))
        print(f"n value - {self.encryptor.nValue}")

    def setPublicKey(self):
        self.globalKeyLineEdit.setText(
            f"Key(pub) = ({self.encryptor.nValue}, {self.encryptor.eValue})"
        )
