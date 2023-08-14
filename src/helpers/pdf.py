import pdfplumber
import re
import os

REGEX_DEPRE_NUM = r"DEPRE Nº: \d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}"

class DeprePdf: 
  def __init__(self, pdf_path):
    if len(pdf_path) == 0:
      raise 'Invalid pdf_path'

    self.path = pdf_path
    self.name = os.path.basename(pdf_path)


  def extract_depre_numbers(self):
    depre_numbers = []

    print(f'Iniciando leitura do PDF: {self.name}.\n')

    with pdfplumber.open(self.path) as pdf:
      page_count = len(pdf.pages)

      for page_num, page in enumerate(pdf.pages, start=1):
        print(f"Processando página {page_num} de {page_count} ...")

        depre_numbers += re.findall(REGEX_DEPRE_NUM, page.extract_text())

    print(f'\nLeitura finalizada com sucesso!')

    depre_numbers = clean_depre_numbers(depre_numbers)
    return DepreExtractionResult(self.name, depre_numbers)


class DepreExtractionResult:
  def __init__(self, pdf_name, depre_numbers):
    self.pdf_name = pdf_name
    self.numbers = depre_numbers
    self.count = len(depre_numbers)


def clean_depre_numbers(depre_numbers):
  return [extract_numbers(number) for number in depre_numbers]


def extract_numbers(string):
  return re.sub(r'\D', '', string)


def read_depre_pdf(pdf_path):
  pdf = DeprePdf(pdf_path)
  return pdf
  
