import os, sys, time
from utils.path import get_pdfs_folder_path
from helpers.pdf import read_depre_pdf
from helpers.database import search_db_matching_depres
from helpers.xls import write_xls, union_depre_results
from db.database import database
from utils.message_formatter import MessageFormatter
from helpers.logger import logger


pdf_folder = get_pdfs_folder_path()
if not os.path.exists(pdf_folder):
    os.mkdir(pdf_folder)

timestamp = int(time.time())
xls_file_name = f"conferencia_{timestamp}.xlsx"

try:
    pdf_count = len(os.listdir(pdf_folder))
    if pdf_count == 0:
        raise Exception("Nenhum pdf encontrado para conferência")

    for i, pdf_name in enumerate(os.listdir(pdf_folder)):
        pdf_path = os.path.join(pdf_folder, pdf_name)

        logger.info(f"Iniciando leitura do PDF: {pdf_name}. ({i + 1}/{pdf_count})")
        pdf = read_depre_pdf(pdf_path)
        depres = pdf.extract_depres()

        if depres.count > 0:
            logger.info(MessageFormatter.starting_conference(pdf_name, depres.count))
        else:
            logger.info(f'Não foi encontrado nenhum Nº de Depre no PDF "{pdf_name}".')
            continue

        depre_numbers = depres.get_numbers()
        matched_depres = search_db_matching_depres(depre_numbers)

        if matched_depres.count > 0:
            logger.info(MessageFormatter.search_result(pdf_name, matched_depres.count))

            xls_depres = union_depre_results(matched_depres, depres)
            xls_object = xls_depres.to_object()
            xls_object["arquivo"] = pdf_name

            write_xls(xls_file_name, xls_object)
        else:
            logger.info(
                f'Não foi encontrado nenhum Nº de Depre correspondente em nossa base de dados no PDF "{pdf_name}".'
            )

    logger.info(MessageFormatter.conference_success(xls_file_name, xls_depres.count))

except Exception as e:
    logger.error(f"Erro: {e}")

finally:
    database.disconnect()

    input("Pressione enter para finalizar ...")

    logger.info("Finalizando ... Até mais!")
    sys.exit()
