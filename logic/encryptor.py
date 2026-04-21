import ast
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox


class Encryptor(QObject):
    def __init__(self):
        super().__init__()
        self.pValue: int = None
        self.qValue: int = None
        self.text: str = None
        self.globalKey: str = None
        self.privateKey: str = None
        self.nValue: int = None
        self.fiValue: int = None
        self.eValue: int = None
        self.eValues: list = []
        self.dValue: list = []
        self.dValues: list = []
        self.save_dir: str = "data"
        self.data: dict = {}
        self.extendedEuclidean: bool = False

    def find_n(self) -> None:
        self.nValue = self.pValue * self.qValue

    def calculate_fi(self) -> None:
        self.fiValue = (self.pValue - 1) * (self.qValue - 1)

    def get_e_value(self) -> None:
        for e in range(3, (self.fiValue + 1), 2):  # +1 for inclusion of last odd number
            gcd = self.euclidean_algorythm(self.fiValue, e)
            if gcd == 1:
                self.eValues.append(e)

        self.eValue = self.eValues[1]

    def euclidean_algorythm(self, a, b) -> int:
        while b != 0:
            remainder = a % b
            a = b
            b = remainder
        return a

    def extented_euclidean_algorythm(self, a, b):
        r0 = a
        r1 = b
        s0 = 1
        s1 = 0
        t0 = 0
        t1 = 1

        while r1 != 0:
            q = int(r0 / r1)

            r2 = r0 - q * r1
            s2 = s0 - q * s1
            t2 = t0 - q * t1

            r0 = r1
            r1 = r2

            s0 = s1
            s1 = s2

            t0 = t1
            t1 = t2

        return t0

    def find_d_value(self):
        self.dValues = []

        for d in range(3, self.fiValue * 10):
            if (d * self.eValue) % self.fiValue == 1:
                self.dValues.append(d)

            if len(self.dValues) >= 5:
                break

        print(self.dValues)

    def cypher(self):
        self.find_n()
        self.calculate_fi()
        self.get_e_value()
        self.find_d_value()
        x = self.convert_to_decimal()

        self.ciphered_text = []

        for code in x:
            y = code**self.eValue % self.nValue
            self.ciphered_text.append(y)

        return self.ciphered_text

    def decypher(self):
        deciphered_text = ""

        if not self.extendedEuclidean:
            print("----------------------Paprastas----------------------")
            self.find_d_value()
            self.dValue = self.dValues[1]
        else:
            print("----------------------Isplestinis----------------------")
            self.dValue = self.extented_euclidean_algorythm(self.fiValue, self.eValue)

        if not self.pValue and not self.qValue:
            self.find_qp_values()

        for code in self.ciphered_text:
            # x = code**self.dValue % self.nValue  # maziems skaiciams
            x = pow(code, self.dValue, self.nValue)
            deciphered_text += chr(x)

        return deciphered_text

    def convert_to_decimal(self):
        desimtainis_kodas = []
        for raide in self.text:
            kodas = ord(raide)
            desimtainis_kodas.append(kodas)

        return desimtainis_kodas

    def write_to_txt(self):
        os.makedirs(self.save_dir, exist_ok=True)

        self.data["pValue"] = self.pValue
        self.data["qValue"] = self.qValue
        self.data["nValue"] = self.nValue
        self.data["eValue"] = self.eValue
        self.data["fiValue"] = self.fiValue
        self.data["cyphered_text"] = self.ciphered_text

        file_path = os.path.join(self.save_dir, "saved.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            for key, value in self.data.items():
                f.write(f"{key}: {value}\n")

    def read_from_txt(self):
        self.data = {}

        file_path = os.path.join("data/saved.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            for row in f:
                key, value = row.strip().split(": ", 1)
                self.data[key] = value

        print(self.data)

        self.qValue = int(self.data["qValue"])
        self.pValue = int(self.data["pValue"])
        self.nValue = int(self.data["nValue"])
        self.eValue = int(self.data["eValue"])
        self.fiValue = int(self.data["fiValue"])
        self.ciphered_text = ast.literal_eval(self.data["cyphered_text"])

    def find_qp_values(self):
        for number in range(1, self.nValue):
            if self.nValue % number == 0:
                self.pValue = number
                self.qValue = self.nValue // number
