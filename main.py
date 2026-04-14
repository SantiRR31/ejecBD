import flet as ft
from database import DBManager
import os
import pandas as pd

def main(page: ft.Page):
    page.title = "Gestor Avanzado MariaDB"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    # Enable Material 3 which gives a premium look by default
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)

    # Global State
    state = {
        "db": None,
        "tables": []
    }

    # Reference variables
    # Login Refs
    host_ref = ft.Ref[ft.TextField]()
    port_ref = ft.Ref[ft.TextField]()
    user_ref = ft.Ref[ft.TextField]()
    pass_ref = ft.Ref[ft.TextField]()
    db_ref = ft.Ref[ft.TextField]()
    login_status = ft.Ref[ft.Text]()

    # Main layout Refs
    main_view = ft.Ref[ft.Container]()
    login_view = ft.Ref[ft.Container]()

    # Views internal Refs
    sql_query_ref = ft.Ref[ft.TextField]()
    sql_result_list = ft.Ref[ft.ListView]()
    graph_container = ft.Ref[ft.Container]()
    
    # Import/Export Refs
    table_dropdown_ref = ft.Ref[ft.Dropdown]()
    target_table_ref = ft.Ref[ft.TextField]()

    def show_snack(msg, is_error=False):
        color = ft.Colors.ERROR if is_error else ft.Colors.GREEN
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def handle_login(e):
        try:
            h = host_ref.current.value
            p = port_ref.current.value
            u = user_ref.current.value
            pw = pass_ref.current.value
            db = db_ref.current.value

            port_num = int(p) if p else 3306

            manager = DBManager(h, port_num, u, pw, db)
            success, msg = manager.connect()

            if success:
                state["db"] = manager
                login_view.current.visible = False
                main_view.current.visible = True
                refresh_tables()
                refresh_graph()
                show_snack("Conexión exitosa a MariaDB")
            else:
                login_status.current.value = f"Error: {msg}"
                login_status.current.color = ft.Colors.ERROR
        except Exception as ex:
            login_status.current.value = f"Error: {str(ex)}"
            login_status.current.color = ft.Colors.ERROR
        page.update()

    def do_logout(e):
        state["db"] = None
        state["tables"] = []
        main_view.current.visible = False
        login_view.current.visible = True
        page.update()

    def refresh_tables():
        if not state["db"] or not state["db"].database: return
        try:
            tabs = state["db"].list_tables()
            state["tables"] = tabs
            # Update dropdowns
            opts = [ft.dropdown.Option(t) for t in tabs]
            table_dropdown_ref.current.options = opts
        except Exception as ex:
            show_snack(f"Error listando tablas: {str(ex)}", True)
        page.update()

    # --------------- TAB: CONSOLA SQL (USUARIOS Y COMANDOS) ---------------
    def execute_sql(e):
        q = sql_query_ref.current.value
        if not q.strip():
            show_snack("Escribe una consulta primero", True)
            return
        
        success, res = state["db"].execute_query(q)
        sql_result_list.current.controls.clear()
        
        if success:
            if "columns" in res and "data" in res:
                # Build Data Table
                dt = ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(c, weight=ft.FontWeight.BOLD)) for c in res["columns"]],
                    rows=[]
                )
                for row in res["data"]:
                    dt_row = ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row])
                    dt.rows.append(dt_row)
                sql_result_list.current.controls.append(dt)
            else:
                msg = res.get("message", "Exito")
                sql_result_list.current.controls.append(ft.Text(msg, color=ft.Colors.GREEN))
            show_snack("Consulta ejecutada")
            refresh_tables()
            refresh_graph()
        else:
            sql_result_list.current.controls.append(ft.Text(res, color=ft.Colors.ERROR))
            show_snack("Error ejecutando SQL", True)
        
        page.update()

    tab_sql = ft.Tab(
        label="Consola SQL Avanzada",
        icon=ft.Icons.TERMINAL,
    )
    tab_sql_content = ft.Container(
        padding=20,
            content=ft.Column([
                ft.Text("Administrador de Esquemas y Accesos", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Escribe sentencias DDL, DCL (CREATE USER, GRANT), o SELECT convencionales.", color=ft.Colors.WHITE_70),
                ft.TextField(
                    ref=sql_query_ref,
                    multiline=True,
                    min_lines=5,
                    max_lines=15,
                    border_color=ft.Colors.TEAL,
                    text_style=ft.TextStyle(font_family="Consolas"),
                    hint_text="Ejemplo:\nCREATE USER 'nuevo_usuario'@'localhost' IDENTIFIED BY 'mi_clave';\nGRANT ALL PRIVILEGES ON *.* TO 'nuevo_usuario'@'localhost';"
                ),
                ft.ElevatedButton("Ejecutar Sentencia", icon=ft.Icons.PLAY_ARROW, on_click=execute_sql, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL)),
                ft.Divider(height=30, color=ft.Colors.WHITE_24),
                ft.Text("Resultados", weight=ft.FontWeight.BOLD),
                ft.Container(
                    border=ft.Border.all(1, ft.Colors.WHITE_24),
                    border_radius=5,
                    padding=10,
                    expand=True,
                    content=ft.ListView(ref=sql_result_list, expand=True)
                )
            ], expand=True)
        )

    # --------------- TAB: IMPORT / EXPORT (BACKUP & CSV) ---------------
    
    backup_picker = ft.FilePicker()
    export_csv_picker = ft.FilePicker()
    restore_sql_picker = ft.FilePicker()
    import_csv_picker = ft.FilePicker()
    
    pickers_added = False
    def ensure_pickers():
        nonlocal pickers_added
        if not pickers_added:
            page.overlay.extend([backup_picker, export_csv_picker, restore_sql_picker, import_csv_picker])
            page.update()
            pickers_added = True

    async def handle_backup_click(e):
        ensure_pickers()
        path = await backup_picker.save_file(allowed_extensions=["sql"])
        if path and state["db"]:
            success, msg = state["db"].export_database_full(path)
            if success:
                show_snack(f"Backup global completado en {path}")
            else:
                show_snack(f"Error realizando backup: {msg}", True)

    async def handle_export_csv_click(e):
        ensure_pickers()
        t = table_dropdown_ref.current.value
        if not t:
            show_snack("Selecciona una tabla primero", True)
            return
        path = await export_csv_picker.save_file(allowed_extensions=["csv"])
        if path and state["db"]:
            success, msg = state["db"].export_table_csv(t, path)
            if success:
                show_snack(f"Muestra exportada a {path}")
            else:
                show_snack(f"Error exportando CSV: {msg}", True)

    async def handle_restore_sql_click(e):
        ensure_pickers()
        files = await restore_sql_picker.pick_files(allowed_extensions=["sql"])
        if files and state["db"]:
            fpath = files[0].path
            success, msg = state["db"].import_sql_file(fpath)
            if success:
                show_snack("Servidor restaurado desde el archivo SQL exitosamente.")
                refresh_tables()
                refresh_graph()
            else:
                show_snack(f"Error al restaurar SQL: {msg}", True)

    async def handle_import_csv_click(e):
        ensure_pickers()
        t = target_table_ref.current.value
        if not t:
            show_snack("Debe indicar el nombre de la tabla destino", True)
            return
        files = await import_csv_picker.pick_files(allowed_extensions=["csv"])
        if files and state["db"]:
            fpath = files[0].path
            success, msg = state["db"].import_csv_to_table(t, fpath)
            if success:
                show_snack(f"Datos CSV cargados en '{t}'")
                refresh_tables()
                refresh_graph()
            else:
                show_snack(f"Error importando CSV: {msg}", True)
    
    tab_io = ft.Tab(
        label="Importar / Exportar (Backup)",
        icon=ft.Icons.SWAP_VERT,
    )
    tab_io_content = ft.Container(
        padding=30,
            content=ft.Column([
                ft.Text("Clonador Global", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Manejo de archivos unificados de la base de datos (.SQL)", color=ft.Colors.WHITE_70),
                ft.Row([
                    ft.ElevatedButton("Exportar Backup Completo (.SQL)", icon=ft.Icons.DOWNLOAD, on_click=handle_backup_click, style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO)),
                    ft.ElevatedButton("Restaurar desde Backup (.SQL)", icon=ft.Icons.UPLOAD, on_click=handle_restore_sql_click),
                ], alignment=ft.MainAxisAlignment.START),
                
                ft.Divider(height=40, color=ft.Colors.WHITE_24),
                
                ft.Text("Manipulador de Tablas a Bloques", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Manejo de conjuntos de datos de una tabla específica (.CSV)", color=ft.Colors.WHITE_70),
                ft.Row([
                    ft.Column([
                        ft.Text("Exportar como CSV", weight=ft.FontWeight.BOLD),
                        ft.Dropdown(ref=table_dropdown_ref, hint_text="Tabla a exportar", width=250),
                        ft.OutlinedButton("Descargar CSV", icon=ft.Icons.DOWNLOAD, on_click=handle_export_csv_click)
                    ], spacing=10),
                    
                    ft.Container(width=40),
                    
                    ft.Column([
                        ft.Text("Importar CSV a Tabla", weight=ft.FontWeight.BOLD),
                        ft.TextField(ref=target_table_ref, label="Nombre Tabla Destino", width=250),
                        ft.OutlinedButton("Cargar CSV", icon=ft.Icons.UPLOAD, on_click=handle_import_csv_click)
                    ], spacing=10)
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
            ], expand=True)
        )

    # --------------- TAB: RENDIMIENTO Y MÉTRICAS ---------------
    def refresh_graph():
        if not state["db"] or not state["db"].database: return
        tables = state["tables"]
        if not tables:
            graph_container.current.content = ft.Text("No hay tablas para graficar rendimento de volumen.", color=ft.Colors.WHITE54)
            page.update()
            return
            
        data = []
        for t in tables:
            success, res = state["db"].execute_query(f"SELECT COUNT(*) FROM `{t}`")
            if success and "data" in res:
                count = res["data"][0][0]
                data.append((t, count))
                
        if not data:
            graph_container.current.content = ft.Text("No se pudo obtener datos.")
            return

        # Build BarChart
        groups = []
        for idx, (t_name, count) in enumerate(data):
            # Using teal color variation based on height to be aesthetically pleasing
            groups.append(
                ft.BarChartGroup(
                    x=idx,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=count,
                            width=30,
                            color=ft.Colors.TEAL,
                            tooltip=f"{t_name}: {count} filas",
                            border_radius=4
                        )
                    ]
                )
            )

        max_y = max((item[1] for item in data), default=1)
        max_y = max_y if max_y > 0 else 1 # Avoid max_Y=0
        
        # Configure X Axis Labels
        x_axis_labels = []
        for idx, (t_name, _) in enumerate(data):
            x_axis_labels.append(
                ft.ChartAxisLabel(
                    value=idx,
                    label=ft.Container(ft.Text(t_name[:10], size=10), padding=5)
                )
            )
            
        chart = ft.BarChart(
            bar_groups=groups,
            border=ft.Border.all(1, ft.Colors.WHITE_24),
            bottom_axis=ft.ChartAxis(
                labels=x_axis_labels,
                labels_size=40,
            ),
            left_axis=ft.ChartAxis(title=ft.Text("Número de Filas"), labels_size=40),
            tooltip_bgcolor=ft.Colors.BLACK_87,
            max_y=max_y + (max_y * 0.1),
            interactive=True,
            expand=True
        )
        
        graph_container.current.content = chart
        page.update()


    tab_performance = ft.Tab(
        label="Métricas & Gráfica",
        icon=ft.Icons.BAR_CHART,
    )
    tab_performance_content = ft.Container(
        padding=30,
            content=ft.Column([
                ft.Row([
                    ft.Text("Rendimiento del Servidor:", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Volumen de Filas por Tabla", size=20, color=ft.Colors.TEAL),
                ]),
                ft.Text("La escalabilidad e indexado depende intensamente del tamaño de datos en tus tablas. Consulta esta gráfica en tus mantenimientos.", color=ft.Colors.WHITE_70),
                ft.Row([
                    ft.ElevatedButton("Actualizar Métricas", icon=ft.Icons.REFRESH, on_click=lambda _: refresh_graph())
                ]),
                ft.Container(height=20),
                ft.Container(
                    ref=graph_container,
                    expand=True,
                    content=ft.Text("Conéctate y refreca para generar la gráfica", color=ft.Colors.WHITE_54),
                    padding=20,
                    border=ft.Border.all(1, ft.Colors.WHITE_12),
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                )
            ], expand=True)
        )

    # --------------- DEFINICIÓN DE VISTAS PRINCIPALES ---------------
    
    # Login View
    login_card = ft.Card(
        elevation=10,
        content=ft.Container(
            padding=40,
            width=400,
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.STORAGE, size=40, color=ft.Colors.TEAL), ft.Text("MariaDB Manager", size=26, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Conexión de servidor de alto rendimiento.", text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE_54),
                ft.Divider(height=30),
                ft.TextField(ref=host_ref, label="Host", value="localhost", prefix_icon=ft.Icons.COMPUTER),
                ft.TextField(ref=port_ref, label="Port", value="3306", prefix_icon=ft.Icons.NUMBERS),
                ft.TextField(ref=user_ref, label="Usuario", value="root", prefix_icon=ft.Icons.PERSON),
                ft.TextField(ref=pass_ref, label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.PASSWORD),
                ft.TextField(ref=db_ref, label="Base de Datos (Opcional)", prefix_icon=ft.Icons.STORAGE),
                ft.Container(height=10),
                ft.ElevatedButton("Ingresar al Gestor", on_click=handle_login, width=320, height=45, style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL, color=ft.Colors.WHITE)),
                ft.Text(ref=login_status, color=ft.Colors.ERROR, text_align=ft.TextAlign.CENTER)
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    )
    
    page.add(
        ft.Container(
            ref=login_view,
            expand=True,
            content=ft.Row([login_card], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            visible=True
        )
    )
    
    # Main Dashboard View
    dashboard_layout = ft.Column([
        # Navbar / Header
        ft.Container(
            padding=15,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.STORAGE, color=ft.Colors.TEAL),
                    ft.Text("MariaDB Manager Workspace", size=20, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.START),
                ft.ElevatedButton("Desconectar Server", icon=ft.Icons.LOGOUT, color=ft.Colors.ERROR, on_click=do_logout)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ),
        # Tabs Body
        ft.Tabs(
            selected_index=0,
            length=3,
            content=ft.Column([
                ft.TabBar(tabs=[tab_sql, tab_io, tab_performance]),
                ft.TabBarView(controls=[tab_sql_content, tab_io_content, tab_performance_content], expand=True)
            ], expand=True),
            expand=True
        )
    ], expand=True)

    page.add(
        ft.Container(
            ref=main_view,
            expand=True,
            content=dashboard_layout,
            visible=False
        )
    )

if __name__ == "__main__":
    ft.run(main)
