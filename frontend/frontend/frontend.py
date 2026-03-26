import reflex as rx
import requests
import io

class State(rx.State):
    host: str = "localhost"
    port: str = "3307"
    user: str = "root"
    password: str = ""
    database: str = ""
    connected: bool = False
    loading: bool = False
    message: str = ""
    
    tables: list[str] = []
    selected_table: str = ""
    schema: str = ""
    
    sql_query: str = ""
    query_result_columns: list[str] = []
    query_result_data: list[list[str]] = []
    query_result_message: str = ""
    
    import_target_table: str = ""
    import_message: str = ""

    new_db_name: str = ""
    create_db_message: str = ""

    new_tb_name: str = ""
    new_tb_columns: list[dict[str, str]] = [{"name": "id", "type": "INT AUTO_INCREMENT PRIMARY KEY"}]
    create_tb_message: str = ""

    # App Authentication State
    app_username: str = ""
    app_password: str = ""
    app_logged_in: bool = False
    app_role: str = ""
    app_login_message: str = ""
    app_users_list: list[dict] = []

    # New User State
    new_u_name: str = ""
    new_u_pass: str = ""
    new_u_role: str = "user"
    new_u_db: str = ""
    new_u_host: str = "localhost"
    new_u_port: str = "3307"
    new_u_muser: str = "root"
    new_u_mpass: str = ""
    new_u_msg: str = ""

    @rx.var
    def backend_url(self) -> str:
        return "http://localhost:5000/api"

    @rx.var
    def message_color(self) -> str:
        return "red" if "Error" in self.message else "green"

    @rx.var
    def query_message_color(self) -> str:
        return "red" if "Error" in self.query_result_message or "DENEGADO" in self.query_result_message else "green"

    @rx.var
    def import_message_color(self) -> str:
        return "red" if "Error" in self.import_message else "green"

    @rx.var
    def create_db_message_color(self) -> str:
        return "red" if "Error" in self.create_db_message else "green"

    @rx.var
    def create_tb_message_color(self) -> str:
        return "red" if "Error" in self.create_tb_message else "green"

    def do_app_login(self):
        self.loading = True
        yield
        try:
            resp = requests.post(f"{self.backend_url}/auth/login", json={"username": self.app_username, "password": self.app_password}, timeout=5)
            data = resp.json()
            if data.get("success"):
                self.app_logged_in = True
                self.app_role = data.get("role")
                if self.app_role == "admin":
                    self.get_app_users()
                    
                mc = data.get("maria_config")
                if self.app_role == "user" and mc:
                    self.host = mc.get("host", "localhost")
                    self.port = str(mc.get("port", "3306"))
                    self.user = mc.get("user", "")
                    self.password = mc.get("password", "")
                    self.database = mc.get("database", "")
                    
                    conn_resp = requests.post(
                        f"{self.backend_url}/connect", 
                        json={"host": self.host, "port": int(self.port), "user": self.user, "password": self.password, "database": self.database}, 
                        timeout=5
                    )
                    conn_data = conn_resp.json()
                    if conn_data.get("success"):
                        self.connected = True
                        self.get_tables()
                    else:
                        self.app_login_message = "Error conectando a DB: " + conn_data.get("message", "")
                        self.app_logged_in = False
            else:
                self.app_login_message = data.get("message", "Credenciales inválidas")
        except Exception as e:
            self.app_login_message = f"Error: {e}"
        self.loading = False

    def app_logout(self):
        self.app_logged_in = False
        self.app_role = ""
        self.app_username = ""
        self.app_password = ""
        self.connected = False
        self.database = ""
        self.tables = []

    def get_app_users(self):
        try:
            resp = requests.get(f"{self.backend_url}/auth/users", timeout=5)
            self.app_users_list = resp.json()
        except Exception:
            pass

    def create_app_user(self):
        self.loading = True
        yield
        data = {
           "username": self.new_u_name,
           "password": self.new_u_pass,
           "role": self.new_u_role,
           "maria_host": self.new_u_host,
           "maria_port": self.new_u_port,
           "maria_user": self.new_u_muser,
           "maria_password": self.new_u_mpass,
           "maria_db": self.new_u_db
        }
        try:
            resp = requests.post(f"{self.backend_url}/auth/users", json=data, timeout=5)
            ans = resp.json()
            if ans.get("success"):
                self.new_u_msg = "Usuario creado exitosamente"
                self.get_app_users()
            else:
                self.new_u_msg = ans.get("message", "Error")
        except Exception as e:
            self.new_u_msg = str(e)
        self.loading = False

    def delete_app_user(self, uid: int):
        try:
            requests.delete(f"{self.backend_url}/auth/users/{int(uid)}", timeout=5)
            self.get_app_users()
        except:
            pass

    def add_tb_column(self):
        self.new_tb_columns.append({"name": "", "type": "VARCHAR(255)"})

    def remove_tb_column(self, idx: int):
        idx = int(idx)
        if len(self.new_tb_columns) > 1:
            self.new_tb_columns.pop(idx)

    def update_col_name(self, val: str, idx: int):
        self.new_tb_columns[int(idx)]["name"] = val

    def update_col_type(self, val: str, idx: int):
        self.new_tb_columns[int(idx)]["type"] = val
        
    def execute_create_table(self):
        if not self.new_tb_name.strip():
            self.create_tb_message = "Error: Falta el nombre de la tabla."
            return
            
        cols = []
        for col in self.new_tb_columns:
            if not col["name"].strip():
                self.create_tb_message = "Error: Todas las columnas deben tener nombre."
                return
            cols.append(f"`{col['name'].strip()}` {col['type']}")
            
        sql = f"CREATE TABLE `{self.new_tb_name.strip()}` (\n  " + ",\n  ".join(cols) + "\n);"
        
        self.loading = True
        self.create_tb_message = "Ejecutando..."
        yield
        try:
            resp = requests.post(f"{self.backend_url}/query", json={"query": sql, "role": self.app_role}, timeout=5)
            data = resp.json()
            if data.get("success"):
                self.create_tb_message = f"¡Tabla '{self.new_tb_name}' creada!"
                self.get_tables()
                self.new_tb_name = ""
                self.new_tb_columns = [{"name": "id", "type": "INT AUTO_INCREMENT PRIMARY KEY"}]
            else:
                self.create_tb_message = f"Error SQL: {data.get('message')}"
        except Exception as e:
            self.create_tb_message = f"Error al crear: {str(e)}"
        self.loading = False
        yield

    def connect_db(self):
        self.loading = True
        self.message = "Conectando..."
        yield
        
        try:
            resp = requests.post(
                f"{self.backend_url}/connect", 
                json={
                    "host": self.host,
                    "port": int(self.port),
                    "user": self.user,
                    "password": self.password,
                    "database": self.database
                },
                timeout=5
            )
            data = resp.json()
            if data.get("success"):
                self.connected = True
                self.message = ""
                self.get_tables()
            else:
                self.message = f"Error: {data.get('message')}"
        except Exception as e:
            self.message = f"Error de conexión: {str(e)}"
        
        self.loading = False
        yield

    def create_database(self):
        if not self.new_db_name.strip():
            self.create_db_message = "Error: El nombre de la BD no puede estar vacío."
            return
            
        self.loading = True
        self.create_db_message = "Creando base de datos..."
        yield
        
        try:
            resp_root = requests.post(
                f"{self.backend_url}/connect", 
                json={
                    "host": self.host,
                    "port": int(self.port),
                    "user": self.user,
                    "password": self.password,
                    "database": ""
                }, timeout=5
            )
            data_root = resp_root.json()
            
            if data_root.get("success"):
                resp_query = requests.post(f"{self.backend_url}/query", json={"query": f"CREATE DATABASE `{self.new_db_name.strip()}`"}, timeout=5)
                data_query = resp_query.json()
                
                if data_query.get("success"):
                    self.database = self.new_db_name.strip()
                    self.create_db_message = "Base de datos creada. Conectando..."
                    yield
                    return type(self).connect_db
                else:
                    self.create_db_message = f"Error SQL: {data_query.get('message')}"
            else:
                self.create_db_message = f"Error al conectar a raíz: {data_root.get('message')}"
        except Exception as e:
            self.create_db_message = f"Error de red: {str(e)}"
            
        self.loading = False
        yield

    def disconnect_db(self):
        self.connected = False
        self.database = ""
        self.tables = []
        self.selected_table = ""
        self.schema = ""
        requests.post(f"{self.backend_url}/disconnect", timeout=5)

    def get_tables(self):
        try:
            resp = requests.get(f"{self.backend_url}/tables", timeout=5)
            data = resp.json()
            if data.get("success"):
                self.tables = data.get("tables", [])
                if not self.tables:
                    self.selected_table = ""
                    self.schema = ""
        except:
            pass

    def get_schema(self, table_name: str):
        self.selected_table = table_name
        if not table_name:
            self.schema = ""
            return
            
        try:
            resp = requests.get(f"{self.backend_url}/schema/{table_name}", timeout=5)
            data = resp.json()
            if data.get("success"):
                self.schema = data.get("schema", "")
            else:
                self.schema = f"Error: {data.get('message')}"
        except Exception as e:
            self.schema = f"Error de red: {str(e)}"

    def drop_table(self):
        if not self.selected_table:
            return
            
        self.loading = True
        yield
        
        try:
            resp = requests.delete(f"{self.backend_url}/table/{self.selected_table}", timeout=5)
            data = resp.json()
            if data.get("success"):
                self.selected_table = ""
                self.schema = ""
                self.get_tables()
            else:
                self.schema = f"Error al eliminar: {data.get('message')}"
        except Exception as e:
            self.schema = f"Error de conexión: {str(e)}"
            
        self.loading = False
        yield

    def execute_sql(self):
        if not self.sql_query.strip():
            self.query_result_message = "Por favor, ingresa una consulta."
            return
            
        self.loading = True
        self.query_result_message = "Ejecutando consulta..."
        yield
        
        try:
            resp = requests.post(f"{self.backend_url}/query", json={"query": self.sql_query, "role": self.app_role}, timeout=5)
            data = resp.json()
            if data.get("success"):
                self.query_result_message = data.get("message", "Ejecución exitosa.")
                self.query_result_columns = data.get("columns", [])
                self.query_result_data = data.get("data", [])
                self.get_tables()
            else:
                self.query_result_message = f"Error: {data.get('message')}"
                self.query_result_columns = []
                self.query_result_data = []
        except Exception as e:
            self.query_result_message = f"Error de conexión: {str(e)}"
        
        self.loading = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            self.import_message = "Error: Por favor selecciona o arrastra un archivo primero."
            return
            
        self.loading = True
        self.import_message = "Procesando archivo..."
        yield
        
        file = files[0]
        upload_data = await file.read()
        
        try:
            files_payload = {'file': (file.filename, io.BytesIO(upload_data))}
            data_payload = {'target_table': self.import_target_table}
            
            resp = requests.post(f"{self.backend_url}/import", files=files_payload, data=data_payload, timeout=20)
            data = resp.json()
            if data.get("success"):
                self.import_message = f"Éxito: {data.get('message')}"
                self.get_tables()
            else:
                self.import_message = f"Error: {data.get('message')}"
        except Exception as e:
            self.import_message = f"Error de red: {str(e)}"
            
        self.loading = False

def render_column_row(col: dict, idx: int) -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Nombre", 
            value=col["name"], 
            on_change=lambda val: State.update_col_name(val, idx),
            width="40%",
            size="2"
        ),
        rx.select(
            ["INT AUTO_INCREMENT PRIMARY KEY", "VARCHAR(255)", "INT", "TEXT", "DATE", "BOOLEAN", "DECIMAL(10,2)", "TIMESTAMP"],
            value=col["type"],
            on_change=lambda val: State.update_col_type(val, idx),
            width="50%",
            size="2"
        ),
        rx.button(
            rx.icon("trash", size=16),
            on_click=lambda: State.remove_tb_column(idx),
            color_scheme="red",
            variant="ghost",
            width="10%",
            size="2"
        ),
        width="100%",
        align_items="center"
    )

def render_db_view() -> rx.Component:
    return rx.tabs.root(
        rx.tabs.list(
            rx.tabs.trigger(rx.hstack(rx.icon("table"), rx.text("Estructura"), spacing="2", align_items="center"), value="schema"),
            rx.tabs.trigger(rx.hstack(rx.icon("code"), rx.text("Consola SQL"), spacing="2", align_items="center"), value="sql"),
            rx.cond(State.app_role == "admin", rx.tabs.trigger(rx.hstack(rx.icon("upload"), rx.text("Importar / Exportar"), spacing="2", align_items="center"), value="io")),
            rx.cond(State.app_role == "admin", rx.tabs.trigger(rx.hstack(rx.icon("users"), rx.text("Usuarios App"), spacing="2", align_items="center"), value="users")),
            size="2",
            margin_bottom="1em"
        ),
        rx.tabs.content(
            rx.vstack(
                rx.hstack(
                    rx.heading("Gestión de Tablas", size="5", weight="bold"),
                    rx.cond(
                        State.app_role == "admin",
                        rx.dialog.root(
                            rx.dialog.trigger(
                                rx.button(rx.icon("plus"), "Nueva Tabla (Visual)", color_scheme="green", size="2")
                            ),
                            rx.dialog.content(
                                rx.dialog.title("Creador Visual de Tablas"),
                                rx.dialog.description("Define el nombre y las columnas de tu nueva tabla."),
                                rx.vstack(
                                    rx.text("Nombre de la tabla", size="2", weight="bold"),
                                    rx.input(placeholder="Ej. inventario_2024", value=State.new_tb_name, on_change=State.set_new_tb_name, width="100%"),
                                    
                                    rx.text("Columnas", size="2", weight="bold", margin_top="1em"),
                                    rx.vstack(
                                        rx.foreach(State.new_tb_columns, render_column_row),
                                        spacing="2",
                                        width="100%"
                                    ),
                                    rx.button(rx.icon("plus"), "Añadir Columna", on_click=State.add_tb_column, variant="outline", color_scheme="blue", size="2", margin_y="1em"),
                                    
                                    rx.cond(
                                        State.create_tb_message,
                                        rx.callout(State.create_tb_message, icon="info", color_scheme=State.create_tb_message_color, width="100%")
                                    ),
                                    
                                    rx.hstack(
                                        rx.dialog.close(rx.button("Cerrar", variant="soft", color_scheme="gray")),
                                        rx.button("Construir y Crear Tabla", on_click=State.execute_create_table, color_scheme="green", is_loading=State.loading),
                                        justify="between",
                                        width="100%",
                                        margin_top="1em"
                                    )
                                ),
                                max_width="600px"
                            )
                        )
                    ),
                    justify="between",
                    width="100%"
                ),
                rx.text("Explora el esquema de las tablas de tu base de datos.", color_scheme="gray", size="2"),
                rx.hstack(
                    rx.select(
                        State.tables,
                        placeholder="Selecciona una tabla",
                        on_change=State.get_schema,
                        width="300px",
                        size="3"
                    ),
                    rx.cond(
                        (State.selected_table != "") & (State.app_role == "admin"),
                        rx.button(
                            rx.icon("trash"),
                            "Eliminar Tabla", 
                            on_click=State.drop_table, 
                            color_scheme="red",
                            variant="soft",
                            size="3",
                            is_loading=State.loading
                        )
                    ),
                    spacing="4",
                    align_items="center"
                ),
                rx.cond(
                    State.schema,
                    rx.box(
                        rx.code_block(State.schema, language="sql", width="100%"),
                        width="100%",
                        border_radius="md",
                        overflow="hidden",
                        margin_top="1em",
                        box_shadow="sm"
                    )
                ),
                width="100%",
                align_items="start",
                spacing="4"
            ),
            value="schema"
        ),
        rx.tabs.content(
            rx.vstack(
                rx.heading("Ejecutar SQL", size="5", weight="bold"),
                rx.text("Escribe comandos SELECT (si eres Admin, también INSERT, UPDATE, DELETE o CREATE).", size="2", color_scheme="gray"),
                rx.text_area(
                    placeholder="SELECT * FROM mi_tabla LIMIT 10;", 
                    value=State.sql_query, 
                    on_change=State.set_sql_query,
                    height="120px",
                    width="100%",
                    font_family="monospace"
                ),
                rx.button(
                    rx.icon("play"),
                    "Ejecutar Consulta", 
                    on_click=State.execute_sql, 
                    color_scheme="indigo",
                    size="3",
                    is_loading=State.loading
                ),
                rx.cond(
                    State.query_result_message,
                    rx.callout(
                        State.query_result_message,
                        icon="info",
                        color_scheme=State.query_message_color,
                        width="100%"
                    )
                ),
                rx.cond(
                    State.query_result_data,
                    rx.scroll_area(
                        rx.data_table(
                            data=State.query_result_data,
                            columns=State.query_result_columns,
                            pagination=True,
                            search=True,
                            sort=True
                        ),
                        max_width="100%",
                        max_height="400px",
                        border="1px solid var(--gray-5)",
                        border_radius="md",
                        padding="1em",
                        bg="white"
                    )
                ),
                width="100%",
                align_items="start",
                spacing="4",
            ),
            value="sql"
        ),
        rx.cond(
            State.app_role == "admin",
            rx.tabs.content(
                rx.vstack(
                    rx.heading("Exportar Datos", size="5", weight="bold"),
                    rx.hstack(
                        rx.link(
                            rx.button(rx.icon("download"), "Backup BD Completa (.sql)", color_scheme="indigo", variant="solid", size="3"),
                            href="http://localhost:5000/api/export",
                            is_external=True
                        ),
                        rx.link(
                            rx.button(rx.icon("file-text"), "Tabla Actual (.csv)", color_scheme="teal", variant="outline", size="3", disabled=State.selected_table == ""),
                            href=f"http://localhost:5000/api/export_csv/{State.selected_table}",
                            is_external=True
                        ),
                        spacing="4"
                    ),
                    rx.text("Asegúrate de haber seleccionado una tabla en la pestaña Estructura antes de exportar a CSV.", size="2", color_scheme="gray"),
                    
                    rx.divider(margin_y="2em"),
                    
                    rx.heading("Importar Datos", size="5", weight="bold"),
                    rx.text("Sube un archivo .sql para restaurar, o un archivo .csv para volcar datos.", size="2", color_scheme="gray"),
                    rx.input(
                        placeholder="Nombre de tabla destino (solo requerido si subes un .csv)", 
                        value=State.import_target_table, 
                        on_change=State.set_import_target_table,
                        width="100%",
                        max_width="400px",
                        size="3"
                    ),
                    rx.upload(
                        rx.vstack(
                            rx.icon("upload", size=32, color="var(--gray-9)"),
                            rx.text("Selecciona el archivo o arrástralo aquí", weight="bold", size="3"),
                            rx.text("Soporta .sql y .csv", size="2", color="var(--gray-9)"),
                            align_items="center",
                            spacing="2"
                        ),
                        id="db_upload",
                        multiple=False,
                        accept={
                            "text/csv": [".csv"],
                            "application/sql": [".sql"]
                        },
                        border="2px dashed var(--gray-6)",
                        border_radius="xl",
                        padding="3em",
                        width="100%",
                        cursor="pointer",
                        _hover={"bg": "var(--gray-3)"}
                    ),
                    rx.button(
                        "⬆ Subir e Importar", 
                        on_click=State.handle_upload(rx.upload_files(upload_id="db_upload")), 
                        color_scheme="orange",
                        size="3",
                        is_loading=State.loading
                    ),
                    rx.cond(
                        State.import_message,
                        rx.callout(
                            State.import_message, 
                            icon="info",
                            color_scheme=State.import_message_color, 
                            width="100%"
                        )
                    ),
                    width="100%",
                    align_items="start",
                    spacing="4",
                ),
                value="io"
            )
        ),
        rx.cond(
            State.app_role == "admin",
            rx.tabs.content(
                rx.vstack(
                    rx.heading("Gestión de Usuarios", size="5", weight="bold"),
                    rx.text("Crea usuarios de la App asignándoles acceso seguro a MariaDB.", size="2", color_scheme="gray"),
                    
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.button(rx.icon("plus"), "Nuevo Usuario", color_scheme="green", size="3", margin_y="1em")
                        ),
                        rx.dialog.content(
                            rx.dialog.title("Añadir Usuario"),
                            rx.vstack(
                                rx.input(placeholder="Nombre de Usuario Web", value=State.new_u_name, on_change=State.set_new_u_name),
                                rx.input(placeholder="Contraseña Web", type="password", value=State.new_u_pass, on_change=State.set_new_u_pass),
                                rx.select(["user", "admin"], value=State.new_u_role, on_change=State.set_new_u_role),
                                rx.cond(
                                    State.new_u_role == "user",
                                    rx.vstack(
                                        rx.text("Conexión Auto-Asignada de MariaDB:", size="1", weight="bold", margin_top="1em"),
                                        rx.input(placeholder="Host (ej. localhost)", value=State.new_u_host, on_change=State.set_new_u_host),
                                        rx.input(placeholder="Port (ej. 3307)", value=State.new_u_port, on_change=State.set_new_u_port),
                                        rx.input(placeholder="Usuario MariaDB", value=State.new_u_muser, on_change=State.set_new_u_muser),
                                        rx.input(placeholder="Contraseña MariaDB", type="password", value=State.new_u_mpass, on_change=State.set_new_u_mpass),
                                        rx.input(placeholder="Base de Datos", value=State.new_u_db, on_change=State.set_new_u_db),
                                    )
                                ),
                                rx.cond(State.new_u_msg, rx.callout(State.new_u_msg, icon="info")),
                                rx.hstack(
                                    rx.dialog.close(rx.button("Cerrar", variant="soft", color_scheme="gray")),
                                    rx.button("Crear Creadencial", on_click=State.create_app_user, color_scheme="green", is_loading=State.loading),
                                    justify="between", width="100%", margin_top="1em"
                                )
                            ),
                            max_width="450px"
                        )
                    ),
                    
                    rx.table.root(
                        rx.table.header(rx.table.row(rx.table.column_header_cell("ID"), rx.table.column_header_cell("Usuario"), rx.table.column_header_cell("Rol"), rx.table.column_header_cell("DB Base"), rx.table.column_header_cell("Acción"))),
                        rx.table.body(
                            rx.foreach(
                                State.app_users_list,
                                lambda u: rx.table.row(
                                    rx.table.cell(u["id"]),
                                    rx.table.cell(u["username"]),
                                    rx.table.cell(u["role"]),
                                    rx.table.cell(u["maria_db"]),
                                    rx.table.cell(rx.button(rx.icon("trash", size=16), on_click=lambda: State.delete_app_user(u["id"]), color_scheme="red", size="1", variant="ghost"))
                                )
                            )
                        ),
                        width="100%",
                        variant="surface"
                    ),
                    width="100%", align_items="start"
                ),
                value="users"
            )
        ),
        default_value="schema",
        width="100%"
    )
    
def render_app_login_view() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.vstack(
                        rx.icon("users", size=48, color="var(--accent-9)"),
                        rx.heading("Acceso al Manager", size="7"),
                        align_items="center"
                    ),
                    width="100%"
                ),
                rx.text("Inicia sesión para administrar MariaDB", size="2", color_scheme="gray", align="center"),
                rx.box(height="1em"),
                rx.text("Usuario", size="2", weight="bold"),
                rx.input(placeholder="Añade tu cuenta web", value=State.app_username, on_change=State.set_app_username, width="100%", size="3"),
                
                rx.text("Contraseña", size="2", weight="bold"),
                rx.input(placeholder="Tu clave secreta", type="password", value=State.app_password, on_change=State.set_app_password, width="100%", size="3"),
                
                rx.box(height="0.5em"),
                rx.button("Ingresar", on_click=State.do_app_login, size="3", color_scheme="indigo", width="100%", is_loading=State.loading),
                
                rx.cond(
                    State.app_login_message,
                    rx.callout(State.app_login_message, icon="info", color_scheme="red", width="100%")
                ),
                spacing="3",
                align_items="start"
            ),
            width="400px",
            size="4",
            box_shadow="lg"
        ),
        min_height="100vh",
        width="100vw",
        bg="var(--gray-2)"
    )

def render_mariadb_login_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.icon("database", size=48, color="var(--accent-9)"),
                rx.heading("Gestor de MariaDB", size="9", align="center"),
                align_items="center",
                spacing="4"
            ),
            rx.text("Administración de bases de datos elegante y veloz", color_scheme="gray", align="center", size="4"),
            rx.box(height="1em"),
            rx.card(
                rx.vstack(
                    rx.heading("Conexión Manual", size="5", weight="bold"),
                    rx.text("Ingresa las credenciales de tu servidor", size="2", color_scheme="gray"),
                    
                    rx.box(height="0.5em"),
                    
                    rx.text("Host", size="2", weight="bold"),
                    rx.input(placeholder="Ej. localhost", value=State.host, on_change=State.set_host, width="100%", size="3"),
                    
                    rx.text("Puerto", size="2", weight="bold"),
                    rx.input(placeholder="Ej. 3306", value=State.port, on_change=State.set_port, width="100%", size="3"),
                    
                    rx.text("Usuario", size="2", weight="bold"),
                    rx.input(placeholder="Ej. root", value=State.user, on_change=State.set_user, width="100%", size="3"),
                    
                    rx.text("Contraseña", size="2", weight="bold"),
                    rx.input(placeholder="Tu contraseña", type="password", value=State.password, on_change=State.set_password, width="100%", size="3"),
                    
                    rx.text("Base de Datos", size="2", weight="bold"),
                    rx.input(placeholder="(Opcional) Vacío para servidor raíz", value=State.database, on_change=State.set_database, width="100%", size="3"),
                    
                    rx.box(height="0.5em"),
                    
                    rx.button(
                        rx.icon("zap"),
                        "Conectar al Servidor", 
                        on_click=State.connect_db, 
                        is_loading=State.loading,
                        width="100%",
                        color_scheme="indigo",
                        size="3"
                    ),
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.button(rx.icon("plus"), "Crear Nueva Base de Datos", width="100%", variant="soft", color_scheme="gray", size="3")
                        ),
                        rx.dialog.content(
                            rx.dialog.title("Crear Base de Datos desde Cero"),
                            rx.dialog.description("Ingresa el nombre de la nueva base de datos. Una vez creada, te conectaremos directamente a ella."),
                            rx.vstack(
                                rx.input(
                                    placeholder="Ejemplo: mi_nuevo_sistema", 
                                    value=State.new_db_name, 
                                    on_change=State.set_new_db_name,
                                    width="100%",
                                    size="3"
                                ),
                                rx.cond(
                                    State.create_db_message,
                                    rx.callout(State.create_db_message, icon="info", color_scheme=State.create_db_message_color, width="100%")
                                ),
                                rx.hstack(
                                    rx.dialog.close(rx.button("Cancelar", variant="soft", color_scheme="gray", size="3")),
                                    rx.button("Crear y Conectar", on_click=State.create_database, color_scheme="green", is_loading=State.loading, size="3"),
                                    margin_top="1em",
                                    justify="between",
                                    width="100%"
                                )
                            ),
                            max_width="400px"
                        )
                    ),
                    rx.cond(
                        State.message,
                        rx.callout(State.message, icon="info", color_scheme=State.message_color, width="100%")
                    ),
                    width="100%",
                    spacing="3",
                    align_items="stretch"
                ),
                width="450px",
                size="4",
                box_shadow="lg"
            ),
            spacing="4",
            align_items="center"
        ),
        min_height="100vh",
        width="100vw",
        bg="var(--gray-2)"
    )

def render_dashboard_view() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("database", size=32, color="var(--accent-9)"),
                rx.heading("MariaDB Manager", size="6"),
                rx.badge(rx.cond(State.database != "", State.database, "Servidor Raíz"), color_scheme="indigo", size="2", radius="full"),
                rx.badge(rx.cond(State.app_role == "admin", "Administrador", "Lector"), color_scheme=rx.cond(State.app_role == "admin", "red", "teal"), size="2", radius="full"),
                align_items="center",
                spacing="4"
            ),
            rx.hstack(
                rx.cond(State.app_role == "admin", rx.button(rx.icon("plug"), "Desconectar DB", on_click=State.disconnect_db, color_scheme="gray", variant="soft", size="2")),
                rx.button(rx.icon("log-out"), "Cerrar Sesión", on_click=State.app_logout, color_scheme="red", variant="soft", size="2"),
                spacing="3"
            ),
            justify="between",
            width="100%",
            padding_x="2em",
            padding_y="1em",
            bg="white",
            border_bottom="1px solid var(--gray-4)",
            box_shadow="sm"
        ),
        rx.container(
            rx.card(
                render_db_view(),
                width="100%",
                padding="2em",
                margin_top="2em",
                box_shadow="md",
                size="4"
            ),
            max_width="1200px"
        ),
        width="100%",
        min_height="100vh",
        bg="var(--gray-2)"
    )

def index() -> rx.Component:
    db_interface = rx.cond(
        State.connected,
        render_dashboard_view(),
        render_mariadb_login_view()
    )
    return rx.cond(
        State.app_logged_in,
        db_interface,
        render_app_login_view()
    )

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="indigo"
    )
)
app.add_page(index, title="MariaDB Manager")