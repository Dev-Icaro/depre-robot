from utils.colors import Colors


class MessageFormatter:
    def starting_conference(pdf_name, found_depres_count):
        return (
            "\nO PDF "
            + Colors.BLUE
            + f"{pdf_name}"
            + Colors.END
            + " contém "
            + Colors.RED
            + f"{found_depres_count}"
            + Colors.END
            + " Depre(s), iniciando conferência ...\n"
        )

    def search_result(pdf_name, matched_depres_count):
        return (
            "Foram encontrados "
            + Colors.RED
            + f"{matched_depres_count}"
            + Colors.END
            + " Depre(s) correspondente(s) em nossa base de dados no PDF "
            + Colors.BLUE
            + f"{pdf_name}."
            + Colors.END
            + "\n---\n"
        )

    def conference_success(xls_file_name):
        return (
            Colors.GREEN
            + f"Conferência finalizada com sucesso!"
            + Colors.END
            + f"\nArquivo xls criado na pasta xls com o nome: "
            + Colors.BLUE
            + f"{xls_file_name}"
            + Colors.END
            + "\n---"
        )

    def processing_page(page_num, page_count):
        return (
            f"Processando página "
            + Colors.YELLOW
            + f"{page_num}"
            + Colors.END
            + " de "
            + Colors.YELLOW
            + f"{page_count}"
            + Colors.END
            + " ..."
        )
