from utils.colors import Colors


class MessageFormatter:
    def starting_conference(pdf_name, found_depres_count):
        return f"O PDF {pdf_name} contém {found_depres_count} Depre(s), Conferindo no banco de dados ..."

    def search_result(pdf_name, matched_depres_count):
        return f"Foram encontrados {matched_depres_count} Depre(s) correspondente(s) em nossa base de dados no PDF {pdf_name}."

    def conference_success(xls_file_name):
        return f"Conferência finalizada com sucesso!\nArquivo xls criado na pasta xls com o nome: {xls_file_name}"

    def processing_page(page_num, page_count):
        if page_num == page_count:
            return f"     Processando página {page_num} de {page_count}...\n"
        else:
            return f"     Processando página {page_num} de {page_count}..."

    def analytics(count_depres_analyzed, count_depres, process_time, depres_per_second):
        return f"     Total de Depres analisados: {count_depres_analyzed}\n     Total de Depres correspondentes: {count_depres}\n     Tempo percorrido: {process_time}\n     Depres analisados por segundo: {depres_per_second}"
