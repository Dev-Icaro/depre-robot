import os
import pandas as pd
import time
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
        df.to_excel(xls_file_path, engine="openpyxl", index=False)
    else:
        df_existing = pd.read_excel(
            xls_file_path,
            engine="openpyxl",
            converters={col: str for col in df.columns},
        )
        df = pd.concat([df_existing, df], ignore_index=True)
        df.to_excel(xls_file_path, engine="openpyxl", index=False)


class UnionDepresResult:
    def __init__(self, xls_depres):
        self.xls_depres = xls_depres
        self.count = len(xls_depres)

    def to_object(self):
        nr_proc = []
        nr_depre = []
        ordem_cron = []

        for depre in self.xls_depres:
            nr_proc.append(depre.nr_proc)
            nr_depre.append(depre.nr_depre)
            ordem_cron.append(depre.ordem_cron)

        xls_object = {
            "nr_depre": nr_depre,
            "ordem_cron": ordem_cron,
            "nr_proc": nr_proc,
        }
        return xls_object


def union_depre_results(database_depres, pdf_depres):
    xls_depres = []

    for db_depre in database_depres.depres:
        for pdf_depre in pdf_depres.depres:
            if db_depre.number == pdf_depre.number:
                xls_depres.append(
                    XlsDepre(
                        format_depre_number(db_depre.number),
                        format_depre_number(pdf_depre.proc_number),
                        pdf_depre.ordem_cron,
                    )
                )

    return UnionDepresResult(xls_depres)


def format_depre_number(depre_number):
    if len(depre_number) == 20:
        return f"{depre_number[:7]}-{depre_number[7:9]}.{depre_number[9:13]}.{depre_number[13]}.{depre_number[14:16]}.{depre_number[16:len(depre_number)]}"

    return depre_number


def generate_xls_file_name():
    timestamp = int(time.time())
    return f"conferencia_{timestamp}.xlsx"
