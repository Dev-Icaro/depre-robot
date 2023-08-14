import os
from utils.path import get_pdfs_folder_path
from helpers.pdf import read_depre_pdf
from helpers.database import search_depres_in_chunks, search_depres
from db.database import database

DEPRE_SEARCH_LIMIT = 1000

pdf_folder = get_pdfs_folder_path()

try:
  for pdf_name in os.listdir(pdf_folder):
    pdf_path = os.path.join(pdf_folder, pdf_name)

    pdf = read_depre_pdf(pdf_path)
    depres = pdf.extract_depre_numbers()

    if depres.count > 0:
      print(f'\nO PDF "{depres.pdf_name}" contém {depres.count} Depre(s), iniciando conferência ...')

    if (depres.count > DEPRE_SEARCH_LIMIT):
      db_depres_matched = search_depres_in_chunks(depres.numbers)
    else:
      db_depres_matched = search_depres(depres.numbers)

    if db_depres_matched.count > 0:
      print(f'Foram encontrados {len(db_depres_matched)} Depre(s) correspondente(s) em nossa base de dados no PDF "{depres.pdf_name}".\n---\n')
      db_depres_matched = list(set(item[0] for item in db_depres_matched))

    else: 
      print(f'Não foi encontrado nenhum Nº de Depre correspondente em nossa base de dados no PDF "{depres.pdf_name}".\n---\n')
    
except Exception as e:
  print(e)

finally:
  database.disconnect()

  




