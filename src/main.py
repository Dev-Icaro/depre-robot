import os, sys, time
from utils.path import get_pdfs_folder_path
from helpers.pdf import read_depre_pdf
from helpers.database import search_db_matching_depres
from helpers.xls import write_xls, union_depre_results, generate_xls_file_name
from helpers.analytics import calc_analytics
from db.database import database
from utils.message_formatter import MessageFormatter
from helpers.logger import logger

try:
    pdf_folder = get_pdfs_folder_path()
    pdf_count = len(os.listdir(pdf_folder))
    if pdf_count == 0:
        raise Exception("Nenhum pdf encontrado para conferência")

    xls_file_name = generate_xls_file_name()
    start_time = time.time()

    count_depres_analyzed = 0
    count_depres_matched = 0

    for i, pdf_name in enumerate(os.listdir(pdf_folder)):
        logger.info(f"Iniciando leitura do PDF: {pdf_name}. ({i + 1}/{pdf_count})")

        pdf_path = os.path.join(pdf_folder, pdf_name)
        pdf = read_depre_pdf(pdf_path)
        depres = pdf.extract_depres()

        if not depres.is_empty():
            logger.info(MessageFormatter.starting_conference(pdf_name, depres.count))
        else:
            logger.info(f'Não foi encontrado nenhum Nº de Depre no PDF "{pdf_name}".')
            continue

        depre_numbers = depres.get_numbers()
        matched_depres = search_db_matching_depres(depre_numbers)

        count_depres_analyzed += depres.count
        count_depres_matched += matched_depres.count

        if not matched_depres.is_empty():
            logger.info(MessageFormatter.search_result(pdf_name, matched_depres.count))

            xls_depres = union_depre_results(matched_depres, depres)
            xls_object = xls_depres.to_object()
            xls_object["arquivo"] = pdf_name

            write_xls(xls_file_name, xls_object)
        else:
            logger.info(
                f'Não foi encontrado nenhum Nº de Depre correspondente em nossa base de dados no PDF "{pdf_name}".'
            )

    end_time = time.time()
    analytics = calc_analytics(start_time, end_time, count_depres_analyzed)

    logger.info(MessageFormatter.conference_success(xls_file_name))
    logger.info(
        MessageFormatter.analytics(
            count_depres_analyzed,
            count_depres_matched,
            analytics.process_time,
            analytics.depres_per_second,
        ),
    )

except Exception as e:
    logger.error(f"Erro: {e}")

finally:
    database.disconnect()

    input("Pressione ENTER para finalizar ...")

    logger.info("Finalizando ... Até mais!")
    sys.exit()
