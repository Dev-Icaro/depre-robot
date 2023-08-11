import pdfplumber
import re

#regex_numero_depre = r"DEPRE N�: \d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}"
regex_numero_depre = r"DEPRE Nº: \d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}"

def read_pdf(pdf_path):
  with pdfplumber.open(pdf_path) as pdf:
    return pdf

def extract_depre_numbers(pdf_path):
  depre_numbers = []

  with pdfplumber.open(pdf_path) as pdf:

    for page_num, page in enumerate(pdf.pages, start=1):
      print(f"Processando página {page_num}")

      depre_numbers += re.findall(regex_numero_depre, page.extract_text())

  return depre_numbers

  
