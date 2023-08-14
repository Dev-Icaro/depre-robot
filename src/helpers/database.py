import math
from db.database import read_sql

class DepreSearchResult:
  def __init__(self, matched_depres):
    self.matched_depres = matched_depres
    self.count = len(matched_depres)

def search_depres_in_chunks(depre_numbers):
  matched_depres = []

  desired_chunk_size = 500
  num_elements = len(depre_numbers)
  num_chunks = math.ceil(num_elements / desired_chunk_size)
  chunk_size = num_elements // num_chunks

  depre_number_chunks = [depre_numbers[i:i + chunk_size] for i in range(0, len(depre_numbers), chunk_size)]

  for chunk in depre_number_chunks:
    query = format_depre_query(chunk)
    result = read_sql(query)

    if result is not None:
      for row in result:
        matched_depres.append(row)

  return DepreSearchResult(matched_depres)


def search_depres(depre_numbers):
  matched_depres = []

  query = format_depre_query(depre_numbers)
  result = read_sql(query)

  if result is not None:
    for row in result:
      matched_depres.append(row)

  return DepreSearchResult(matched_depres)


def format_depre_query(depre_numbers):
  formated_nums = ["'{}'".format(element) for element in depre_numbers]
  formated_nums = ','.join(formated_nums)

  query = f'SELECT nr_depre FROM processos_incidentes WHERE nr_depre IN ({formated_nums})'

  return query