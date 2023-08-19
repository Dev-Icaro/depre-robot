import os, sys


def get_current_path():
    if getattr(sys, "frozen", False):
        return os.path.abspath(os.path.dirname(sys.executable))
    else:
        return os.path.abspath(os.path.dirname(__file__))


def get_pdfs_folder_path():
    working_path = os.path.abspath(os.getcwd())
    pdf_folder = os.path.join(working_path, "pdfs")

    if not os.path.exists(pdf_folder):
        os.mkdir(pdf_folder)

    return pdf_folder


def get_xls_folder_path():
    working_path = os.path.abspath(os.getcwd())
    xls_folder = os.path.join(working_path, "xls")

    return xls_folder
