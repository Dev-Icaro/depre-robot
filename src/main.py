import os, sys, time
from utils.path import get_pdfs_folder_path, get_current_path
from utils.files import change_file_extension
from helpers.pdf import read_depre_pdf
from helpers.database import search_depres_in_chunks, search_depres
from helpers.logger import log
from helpers.xls import write_xls
from db.database import database
from helpers.xls import XlsDepre
import pandas as pd

class UnionDepresResult:
  def __init__(self, xls_depres):
    self.xls_depres = xls_depres

  def to_object(self):
    nr_proc = []
    nr_depre = []
    ordem_cron = []

    for depre in self.xls_depres:
      nr_proc.append(depre.nr_proc)
      nr_depre.append(depre.nr_depre)
      ordem_cron.append(depre.ordem_cron)

    xls_object = { "nro_depre": nr_depre, "nr_proc": nr_proc, "ordem_cron": ordem_cron }
    return xls_object


def union_depre_results(database_depres, pdf_depres):
  xls_depres = []

  for db_depre in database_depres.depres:
    for pdf_depre in pdf_depres.depres:
      if db_depre.number == pdf_depre.number:
        xls_depres.append(XlsDepre(db_depre.number, db_depre.nr_proc, pdf_depre.ordem_cron))

  return UnionDepresResult(xls_depres)


DEPRE_SEARCH_LIMIT = 1000

pdf_folder = get_pdfs_folder_path()
search_result = []

try:
  for pdf_name in os.listdir(pdf_folder):
    pdf_path = os.path.join(pdf_folder, pdf_name)

    pdf = read_depre_pdf(pdf_path)
    depres = pdf.extract_depres()

    if depres.count > 0:
      print(f'\nO PDF "{pdf_name}" contém {depres.count} Depre(s), iniciando conferência ...')

    depre_numbers = depres.get_numbers()

    if (depres.count > DEPRE_SEARCH_LIMIT):
      matched_depres = search_depres_in_chunks(depre_numbers)
    else:
      matched_depres = search_depres(depre_numbers)

    if matched_depres.count > 0:
      print(f'Foram encontrados {matched_depres.count} Depre(s) correspondente(s) em nossa base de dados no PDF "{pdf_name}".\n---\n')

      xls_depres = union_depre_results(matched_depres, depres)
      xls_object = xls_depres.to_object()
      xls_object['arquivo'] = pdf_name

      search_result.append(xls_object)

    else: 
      print(f'Não foi encontrado nenhum Nº de Depre correspondente em nossa base de dados no PDF "{pdf_name}".\n---\n')

  if len(search_result) > 0:
    timestamp = int(time.time())
    xls_file_name = f"conferencia_{timestamp}.xlsx"

    for result in search_result:
      write_xls(xls_file_name, result)

    
except Exception as e:
  print(e)
  log(e)

finally:
  database.disconnect()
  sys.exit('\nFinalizando ...\n---')

  




