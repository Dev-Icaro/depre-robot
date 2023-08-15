from utils.colors import Colors
import firebirdsql


class Database:
    def __init__(self):
        self.con = None

    def connect(self):
        host = "node113446-s1info.jelastic.saveincloud.net"
        port = 11235
        database = "/opt/firebird/data/ASM.FDB"
        user = "SYSDBA"
        password = "DZ1Y7M9JR6fJvhVu0iK1"

        print("Conectando ao banco de dados ...")

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
            print(Colors.GREEN + "Conexão bem-sucedida!" + Colors.END + "\n---\n")

        except Exception as e:
            print(
                Colors.RED
                + "Ocorreram erros ao se conectar com o banco de dados ..."
                + Colors.END
            )

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
            print("SQL Execution error:", e)
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
            print("SQL Read error:", e)
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
        print("SQL Read error:", e)
    finally:
        if cur:
            cur.close()


print(
    Colors.BLUE
    + "Olá, Bem-vindo(a) ao depre-robot! Iniciando ..."
    + Colors.END
    + "\n---\n"
)

database = Database()
database.connect()
