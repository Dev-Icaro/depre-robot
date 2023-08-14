import os 
import pandas as pd
from utils.path import get_xls_folder_path

class XlsDepre:
  def __init__(self, nr_depre, nr_proc, ordem_cron):
    self.nr_depre = nr_depre
    self.nr_proc = nr_proc
    self.ordem_cron = ordem_cron


def write_xls(file_name, data_frame):
  xls_folder_path = get_xls_folder_path()

  if not os.path.exists(xls_folder_path):
    os.makedirs(xls_folder_path)

  df = pd.DataFrame(data_frame)
  xls_file_path = os.path.join(xls_folder_path, file_name)

  if not os.path.exists(xls_file_path):
    df.to_excel(xls_file_path, engine='openpyxl', index=False)
  else:
    df_existing = pd.read_excel(xls_file_path, engine="openpyxl", converters={col: str for col in df.columns})
    df = pd.concat([df_existing, df], ignore_index=True)
    df.to_excel(xls_file_path, engine='openpyxl', index=False)
  

