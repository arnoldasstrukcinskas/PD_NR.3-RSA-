import math
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox


class Encryptor(QObject):
    def __init__(self):
        super().__init__()
        print("encryptor starter")
        self.pValue: int = None
        self.qValue: int = None
        self.text: str = None
        self.globalKey: str = None
        self.privateKey: str = None
        self.nValue: int = None
        self.fiValue: int = None
        self.eValue: int = None
        self.eValues: list = []
        self.dvalues: list = []

    def findN(self) -> None:
        self.nValue = self.pValue * self.qValue

    def calculateFi(self) -> None:
        self.fiValue = (self.pValue - 1) * (self.qValue - 1)

    def getEValue(self) -> None:
        for e in range(3, (self.fiValue + 1), 2):  # +1 for inclusion of last odd number
            gcd = self.euclidean_algorythm(self.fiValue, e)
            if gcd == 1:
                self.eValues.append(e)

        self.eValue = self.eValues[1]
        print(f"e value - {self.eValue}")

    def euclidean_algorythm(self, a, b) -> int:
        while b != 0:
            remainder = a % b
            a = b
            b = remainder
        return a

    def findDValue(self):
        self.dValues = []

        for d in range(3, self.fiValue * 10):
            if (d * self.eValue) % self.fiValue == 1:
                self.dvalues.append(d)

            if len(self.dvalues) >= 5:
                break

        print(self.dvalues)

    def cypher(self):
        self.findN()
        self.calculateFi()
        self.getEValue()
        self.findDValue()
        x = self.convertToDecimal()

        ciphered_text = []

        for code in x:
            y = code**self.eValue % self.nValue
            ciphered_text.append(y)

        return ciphered_text

    def convertToDecimal(self):
        desimtainis_kodas = []
        for raide in self.text:
            kodas = ord(raide)
            desimtainis_kodas.append(kodas)

        return desimtainis_kodas
