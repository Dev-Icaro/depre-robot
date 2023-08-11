import os
#import fdb
import firebirdsql
from utils.path import get_pdfs_folder_path
from utils.pdf import extract_depre_numbers

pdf_folder = get_pdfs_folder_path()

#for pdf_name in os.listdir(pdf_folder):
  #pdf_path = os.path.join(pdf_folder, pdf_name)

#  depre_numbers = extract_depre_numbers(pdf_path)

  #print(f"Foram encontrados {len(depre_numbers)} DEPRES no pdf {pdf_name}")


print("Conectando ao banco de dados")

host = 'node113446-s1info.jelastic.saveincloud.net'
port = 11235
database = '/opt/firebird/data/ASM.FDB'
user = 'SYSDBA'
password = 'DZ1Y7M9JR6fJvhVu0iK1'

#conn_string = f"hostname={host};database={database};user={user};password={password}"

connection = None
try:
  connection = firebirdsql.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password,
    charset='UTF8'
  )
  print("Conexão bem-sucedida! Iniciando consulta...")

  query = f'SELECT nr_depre FROM processos_incidentes WHERE nr_depre = '

except:
  print("Falha ao conectar com o banco de dados")

finally:
  if connection:
    connection.close()




