from utils.colors import Colors
from helpers.ini_file import iniFile
import firebirdsql
import sys
import re
from helpers.logger import logger


class Database:
    def __init__(self):
        self.con = None

    def connect(self, host, port, database, user, password):
        logger.info("Conectando ao banco de dados ...")

        self.con = None
        try:
            self.con = firebirdsql.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                charset="UTF8",
            )
            logger.info("Conexão bem-sucedida!")

        except Exception as e:
            msg = "Ocorreram erros ao se conectar com o banco de dados, Finalizando ..."
            logger.error(msg)
            sys.exit(msg)

    def disconnect(self):
        if self.con:
            self.con.close()

    def execute_sql(self, query):
        cur = self.con.cursor()
        try:
            self.con.begin()
            cur.execute(query)
            self.con.commit()
        except Exception as e:
            logger.error("SQL Execution error:", e)
        finally:
            if cur:
                cur.close()

    def read_sql(self, query):
        cur = self.con.cursor()
        result = None
        try:
            cur.execute(query)
            result = cur.fetchall()

            return result
        except Exception as e:
            logger.error("SQL Read error:", e)
        finally:
            if cur:
                cur.close()

    def get_connection(self):
        if self.con:
            return self.con


def read_sql(query):
    con = database.get_connection()
    cur = con.cursor()
    result = None
    try:
        cur.execute(query)
        result = cur.fetchall()

        return result
    except Exception as e:
        logger.error("SQL Read error:", e)
    finally:
        if cur:
            cur.close()


def extract_db_url_values(url):
    pattern = r"^(?P<host>.*?)/(?P<port>\d+):(?P<db>/.*)$"
    match = re.match(pattern, url)

    if match:
        host = match.group("host")
        port = int(match.group("port"))
        db = match.group("db")
        user = "SYSDBA"

        return host, port, db, user
    else:
        return None


logger.info("Olá, Bem-vindo(a) ao depre-robot! Iniciando ...")

ini = iniFile()
db_url = ini.get_value("Database")

password = ini.get_value("Code_Connection")
host, port, db, user = extract_db_url_values(db_url)

database = Database()
database.connect(host=host, port=port, database=db, user=user, password=password)
