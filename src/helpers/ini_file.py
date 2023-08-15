import os
import sys
from utils.path import get_current_path


class iniFile:
    def __init__(self):
        self.path = rf"{get_current_path()}\dbxconnections.ini"

        if not os.path.exists(self.path):
            msg = f"O arquivo ini: {self.path} não foi encontrado! Finalizando ..."
            sys.exit(msg)

        self.readIniFile()

    def readIniFile(self):
        with open(self.path, "r", encoding="UTF-8") as ini:
            self.lines = clearTextLines(ini.readlines())

    def getValue(self, valueName):
        value = ""

        for line in self.lines:
            if valueName in line:
                startPos = line.find("=") + 1
                value = line[startPos : len(line)]

                return value


def clearTextLines(lines):
    return [line.rstrip() for line in lines]
