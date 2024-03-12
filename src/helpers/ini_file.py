import os
import sys
from utils.path import get_current_path
from helpers.logger import logger


class iniFile:
    def __init__(self):
        self.path = rf"{get_current_path()}\dbxconnections.ini"

        if not os.path.exists(self.path):
            msg = f"O arquivo ini: {self.path} não foi encontrado! Finalizando ..."
            logger.error(msg)
            sys.exit(msg)

        self.read_ini_file()

    def read_ini_file(self):
        with open(self.path, "r", encoding="UTF-8") as ini:
            self.lines = clear_text_lines(ini.readlines())

    def get_value(self, value_name):
        value = ""

        for line in self.lines:
            if value_name in line:
                start_pos = line.find("=") + 1
                value = line[start_pos : len(line)]

                return value


def clear_text_lines(lines):
    return [line.rstrip() for line in lines]
