import pandas as pd
import json
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

class DBManager:
    def __init__(self, host, port, user, password, database=""):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        if database:
            self.conn_str = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        else:
            self.conn_str = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/"
        self.engine = create_engine(self.conn_str, pool_pre_ping=True)

    def connect(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True, "Conexión exitosa"
        except Exception as e:
            return False, str(e)

    def list_databases(self):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SHOW DATABASES"))
                return [row[0] for row in result]
        except Exception:
            return []

    def list_tables(self):
        if not self.database:
            return []
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SHOW TABLES"))
                return [row[0] for row in result]
        except Exception:
            return []

    def get_table_schema(self, table_name):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(f"SHOW CREATE TABLE {table_name}"))
                return result.fetchone()[1]
        except Exception as e:
            return f"Error al obtener esquema: {e}"

    def get_record_count(self, table_name):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                return result.fetchone()[0]
        except Exception:
            return 0

    def export_database_full(self, output_path):
        try:
            tables = self.list_tables()
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"-- Backup of {self.database}\n")
                f.write(f"-- Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                with self.engine.connect() as connection:
                    for table in tables:
                        schema_res = connection.execute(text(f"SHOW CREATE TABLE {table}"))
                        create_stmt = schema_res.fetchone()[1]
                        f.write(f"{create_stmt};\n\n")
                        
                        df = pd.read_sql(f"SELECT * FROM {table}", connection)
                        for _, row in df.iterrows():
                            columns = ", ".join([f"`{c}`" for c in df.columns])
                            values = ", ".join([self._format_val(v) for v in row.values])
                            f.write(f"INSERT INTO `{table}` ({columns}) VALUES ({values});\n")
                        f.write("\n")
            return True, output_path
        except Exception as e:
            return False, str(e)

    def export_table_csv(self, table_name, output_path):
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(f"SELECT * FROM {table_name}", connection)
                df.to_csv(output_path, index=False)
            return True, output_path
        except Exception as e:
            return False, str(e)

    def export_table_json(self, table_name, output_path):
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(f"SELECT * FROM {table_name}", connection)
                df.to_json(output_path, orient='records', indent=4)
            return True, output_path
        except Exception as e:
            return False, str(e)

    def import_sql_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            statements = [s.strip() for s in sql_content.split(";") if s.strip()]
            with self.engine.connect() as connection:
                with connection.begin():
                    for stmt in statements:
                        connection.execute(text(stmt))
            return True, "Importación SQL exitosa"
        except Exception as e:
            return False, str(e)

    def import_csv_to_table(self, table_name, file_path):
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            return True, "Importación CSV exitosa"
        except Exception as e:
            return False, str(e)

    def import_json_to_table(self, table_name, file_path):
        try:
            df = pd.read_json(file_path)
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            return True, "Importación JSON exitosa"
        except Exception as e:
            return False, str(e)

    def _format_val(self, val):
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return "NULL"
        if isinstance(val, (int, float)):
            return str(val)
        safe_val = str(val).replace("'", "''")
        return f"'{safe_val}'"

    def drop_table(self, table_name):
        try:
            with self.engine.connect() as connection:
                with connection.begin():
                    connection.execute(text(f"DROP TABLE {table_name}"))
            return True, f"Tabla '{table_name}' eliminada con éxito"
        except Exception as e:
            return False, f"Error al eliminar tabla: {e}"

    def execute_query(self, query, params=None):
        start_time = time.time()
        try:
            with self.engine.connect() as connection:
                with connection.begin():
                    result = connection.execute(text(query), params or {})
                    execution_time = time.time() - start_time
                    if result.returns_rows:
                        columns = list(result.keys())
                        rows = [list(row) for row in result]
                        return True, {"columns": columns, "data": rows, "time": execution_time}
                    else:
                        return True, {"message": f"Consulta ejecutada. Filas afectadas: {result.rowcount}", "time": execution_time}
        except Exception as e:
            return False, str(e)
