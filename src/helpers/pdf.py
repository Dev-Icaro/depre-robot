import pdfplumber
import re
import os

REGEX_DEPRE_NUM = r"DEPRE Nº: \d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}"
REGEX_ORDEM_CRONOLOGICA = r'Ordem Cronológica: (\d+/\d+)'

class DeprePdf: 
  def __init__(self, pdf_path):
    if len(pdf_path) == 0:
      raise 'Invalid pdf_path'

    self.path = pdf_path
    self.name = os.path.basename(pdf_path)

  def extract_depres(self):
    depre_numbers = []
    depre_ordens_cron = []

    print(f'Iniciando leitura do PDF: {self.name}.\n')

    with pdfplumber.open(self.path) as pdf:
      page_count = len(pdf.pages)

      for page_num, page in enumerate(pdf.pages, start=1):
        print(f"Processando página {page_num} de {page_count} ...")

        page_text = page.extract_text()

        depre_numbers += re.findall(REGEX_DEPRE_NUM, page_text)
        depre_ordens_cron += re.findall(REGEX_ORDEM_CRONOLOGICA, page_text)

    print(f'\nLeitura finalizada com sucesso!')

    depre_numbers = clean_depre_numbers(depre_numbers)
    depres = union_depre_data(depre_numbers, depre_ordens_cron)

    return DepreExtractionResult(self.name, depres)


class DepreExtractionResult:
  def __init__(self, pdf_name, depres):
    self.pdf_name = pdf_name
    self.depres = depres
    self.count = len(depres)

  def get_numbers(self):
    numbers = []

    for depre in self.depres:
      numbers.append(depre.number)

    return numbers


class Depre: 
  def __init__(self, number, ordem_cron):
    self.number = number
    self.ordem_cron = ordem_cron


def clean_depre_numbers(depre_numbers):
  return [extract_numbers(number) for number in depre_numbers]


def extract_numbers(string):
  return re.sub(r'\D', '', string)


def read_depre_pdf(pdf_path):
  pdf = DeprePdf(pdf_path)
  return pdf


def union_depre_data(depre_numbers, depre_ordens_cron):
  if len(depre_numbers) != len(depre_ordens_cron):
      raise f'''
          A quantidade de Nº Depres: {len(depre_numbers)} 
          é diferente da quantidade de Ordens cronológicas: {len(depre_ordens_cron)}, 
          favor entrar em contato com o desenvolvedor: Icaro
        '''
  
  depres = []
  
  for i, number in enumerate(depre_numbers):
    depres.append(Depre(depre_numbers[i], depre_ordens_cron[i]))

  return depres
  
