import pandas as pd
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
        self.engine = create_engine(self.conn_str)

    def connect(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True, "Conexión exitosa"
        except Exception as e:
            return False, str(e)

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

    def export_database_full(self, output_path):
        try:
            tables = self.list_tables()
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"-- Backup of {self.database}\n\n")
                with self.engine.connect() as connection:
                    for table in tables:
                        # Write Schema
                        schema_res = connection.execute(text(f"SHOW CREATE TABLE {table}"))
                        create_stmt = schema_res.fetchone()[1]
                        f.write(f"{create_stmt};\n\n")
                        
                        # Write Data
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

    def _format_val(self, val):
        if val is None:
            return "NULL"
        if isinstance(val, (int, float)):
            return str(val)
        # Escape single quotes for SQL
        safe_val = str(val).replace("'", "''")
        return f"'{safe_val}'"

    def import_sql_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            
            statements = sql_content.split(";")
            with self.engine.connect() as connection:
                with connection.begin():
                    for stmt in statements:
                        if stmt.strip():
                            connection.execute(text(stmt))
            return True, "Importación SQL exitosa"
        except Exception as e:
            return False, str(e)

    def import_csv_to_table(self, table_name, file_path):
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            return True, "Importación CSV exitosa"
        except Exception as e:
            return False, str(e)

    def drop_table(self, table_name):
        try:
            with self.engine.connect() as connection:
                connection.execute(text(f"DROP TABLE {table_name}"))
            return True, f"Tabla '{table_name}' eliminada con éxito"
        except Exception as e:
            return False, f"Error al eliminar tabla: {e}"

    def execute_query(self, query):
        try:
            with self.engine.connect() as connection:
                # Use begin() to automatically commit transactions like INSERT/UPDATE/DELETE/CREATE
                with connection.begin():
                    result = connection.execute(text(query))
                    
                    # If the query returns rows (like SELECT)
                    if result.returns_rows:
                        columns = list(result.keys())
                        rows = [list(row) for row in result]
                        return True, {"columns": columns, "data": rows}
                    else:
                        return True, {"message": f"Consulta ejecutada correctamente. Filas afectadas: {result.rowcount}"}
        except Exception as e:
            return False, str(e)
