import os, sys, time
from utils.path import get_pdfs_folder_path
from helpers.pdf import read_depre_pdf
from helpers.database import search_db_matching_depres
from helpers.logger import log
from helpers.xls import write_xls, union_depre_results
from utils.colors import Colors
from db.database import database
from utils.message_formatter import MessageFormatter


pdf_folder = get_pdfs_folder_path()
timestamp = int(time.time())
xls_file_name = f"conferencia_{timestamp}.xlsx"

try:
    for pdf_name in os.listdir(pdf_folder):
        pdf_path = os.path.join(pdf_folder, pdf_name)

        pdf = read_depre_pdf(pdf_path)
        depres = pdf.extract_depres()

        if depres.count > 0:
            print(MessageFormatter.starting_conference(pdf_name, depres.count))
        else:
            print(f'Não foi encontrado nenhum Nº de Depre no PDF "{pdf_name}".\n---\n')
            continue

        depre_numbers = depres.get_numbers()
        matched_depres = search_db_matching_depres(depre_numbers)

        if matched_depres.count > 0:
            print(MessageFormatter.search_result(pdf_name, matched_depres.count))

            xls_depres = union_depre_results(matched_depres, depres)
            xls_object = xls_depres.to_object()
            xls_object["arquivo"] = pdf_name

            write_xls(xls_file_name, xls_object)
        else:
            print(
                f'Não foi encontrado nenhum Nº de Depre correspondente em nossa base de dados no PDF "{pdf_name}".\n---\n'
            )

        MessageFormatter.conference_success(xls_file_name)

except Exception as e:
    print(Colors.RED + f"Erro: {e}" + Colors.END)
    log(e)

finally:
    database.disconnect()
    sys.exit(Colors.GREY + "\nFinalizando ... Até mais!" + Colors.END + "\n")
