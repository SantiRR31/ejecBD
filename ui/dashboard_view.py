import flet as ft
import os
import threading
import time
from db.database import DBManager
from services.auth_service import AuthService
from services.monitor_service import MonitorService

def dashboard_v(page: ft.Page, auth_service: AuthService, monitor_service: MonitorService):
    page.views.clear()
    user = page.session.get("user") or {"username": "Guest", "role": "user"}
    is_admin = user.get("role") == "admin"
    db_mgr = page.session.get("db_manager")
    
    ACCENT_CYAN = "#00F2FF"
    ACCENT_PURPLE = "#7000FF"
    BG_DARK = "#0A0B10"
    GLASS_BG = "white05"
    BORDER_RADIUS = 20

    import_field = ft.TextField(label="Nombre Tabla Destino", border_color=ACCENT_CYAN, border_radius=10)
    import_status = ft.Text("")
    import_progress = ft.ProgressBar(width=300, color=ACCENT_CYAN, visible=False)
    
    def on_import_confirm(e):
        import_progress.visible = True
        import_status.value = "🛸 Inyectando datos en MariaDB..."
        page.update()
        path = page.session.get("active_path")
        ext = path.split('.')[-1].lower()
        def process():
            try:
                if ext == "csv": success, msg = db_mgr.import_csv_to_table(import_field.value, path)
                elif ext == "json": success, msg = db_mgr.import_json_to_table(import_field.value, path)
                else: success, msg = db_mgr.import_sql_file(path)
                import_status.value = msg
                import_status.color = ACCENT_CYAN if success else "red400"
                import_progress.visible = False
                if success: show_explorer()
                page.update()
            except Exception as ex:
                import_status.value = f"Error: {ex}"
                import_progress.visible = False
                page.update()
        threading.Thread(target=process).start()

    dlg_import = ft.AlertDialog(
        title=ft.Text("IMPORTACIÓN MAESTRA", weight="bold", color=ACCENT_CYAN),
        content=ft.Column([import_field, import_progress, import_status], tight=True, spacing=15),
        actions=[
            ft.TextButton("CANCELAR", on_click=lambda _: [setattr(dlg_import, "open", False), page.update()]),
            ft.ElevatedButton("IMPORTAR AHORA", on_click=on_import_confirm, bgcolor=ACCENT_PURPLE, color="white")
        ],
        bgcolor=BG_DARK, shape=ft.RoundedRectangleBorder(radius=20)
    )

    def on_import_res(e: ft.FilePickerResultEvent):
        if e.files:
            page.session.set("active_path", e.files[0].path)
            import_field.value = "data_" + os.path.basename(e.files[0].path).split('.')[0].lower().replace(" ","_")
            page.open(dlg_import)
            page.update()

    # Visual Table Builder
    new_table_name = ft.TextField(label="Nombre de la Tabla", border_color=ACCENT_CYAN)
    builder_rows = ft.Column(spacing=10, scroll="adaptive", height=300)
    builder_status = ft.Text("")

    def add_builder_row(e=None):
        row = ft.Row([
            ft.TextField(label="Nombre Columna", border_color=ACCENT_CYAN, expand=2),
            ft.Dropdown(
                label="Tipo",
                options=[
                    ft.dropdown.Option("INT AUTO_INCREMENT PRIMARY KEY"),
                    ft.dropdown.Option("VARCHAR(255)"),
                    ft.dropdown.Option("INT"),
                    ft.dropdown.Option("TEXT"),
                    ft.dropdown.Option("DECIMAL(10,2)"),
                    ft.dropdown.Option("DATE"),
                    ft.dropdown.Option("BOOLEAN")
                ],
                expand=3, value="VARCHAR(255)"
            ),
            ft.IconButton("delete", icon_color="red400", on_click=lambda _: [builder_rows.controls.remove(row), page.update()])
        ])
        builder_rows.controls.append(row)
        page.update()

    def on_create_table(e):
        if not new_table_name.value:
            builder_status.value = "❌ El nombre es obligatorio"; page.update(); return
        cols = []
        for row in builder_rows.controls:
            name, dtype = row.controls[0].value, row.controls[1].value
            if name: cols.append(f"`{name}` {dtype}")
        if not cols:
            builder_status.value = "❌ Añade al menos una columna"; page.update(); return
        sql = f"CREATE TABLE `{new_table_name.value}` (\n  " + ",\n  ".join(cols) + "\n);"
        success, res = db_mgr.execute_query(sql)
        if success:
            page.open(ft.AlertDialog(title=ft.Text("Éxito"), content=ft.Text(f"Tabla '{new_table_name.value}' creada."), bgcolor=BG_DARK))
            setattr(dlg_builder, "open", False)
            show_explorer()
        else:
            builder_status.value = f"Error SQL: {res}"; builder_status.color = "red400"
        page.update()

    dlg_builder = ft.AlertDialog(
        title=ft.Text("CREAR NUEVA TABLA", weight="bold", color=ACCENT_CYAN),
        content=ft.Column([new_table_name, ft.Divider(color="white10"), builder_rows, ft.TextButton("+ AÑADIR COLUMNA", icon="add", on_click=add_builder_row), builder_status], tight=True, spacing=15, width=500),
        actions=[
            ft.TextButton("CANCELAR", on_click=lambda _: [setattr(dlg_builder, "open", False), page.update()]),
            ft.ElevatedButton("CREAR TABLA", on_click=on_create_table, bgcolor=ACCENT_PURPLE, color="white")
        ],
        bgcolor=BG_DARK, shape=ft.RoundedRectangleBorder(radius=20)
    )
    add_builder_row()

    def on_export_res(e: ft.FilePickerResultEvent):
        if e.path:
            path = e.path
            table, fmt = page.session.get("exp_table"), page.session.get("exp_fmt")
            if fmt == "csv" and not path.lower().endswith(".csv"): path += ".csv"
            elif fmt == "json" and not path.lower().endswith(".json"): path += ".json"
            elif fmt == "sql" and not path.lower().endswith(".sql"): path += ".sql"
            if fmt == "csv": db_mgr.export_table_csv(table, path)
            elif fmt == "json": db_mgr.export_table_json(table, path)
            elif fmt == "sql": db_mgr.export_database_full(path)
            page.snack_bar = ft.SnackBar(ft.Text(f"Archivo generado: {os.path.basename(path)}"), bgcolor=ACCENT_PURPLE)
            page.snack_bar.open = True; page.update()

    im_p, ex_p = ft.FilePicker(on_result=on_import_res), ft.FilePicker(on_result=on_export_res)
    page.overlay.extend([im_p, ex_p, dlg_import, dlg_builder])
    
    main_content = ft.Container(expand=True, padding=20)

    def show_explorer():
        if not db_mgr: return
        tables = db_mgr.list_tables()
        table_list = ft.ListView(expand=True, spacing=10)
        detail_view = ft.Column(expand=True, scroll="adaptive", spacing=20)
        btn_new_table = ft.ElevatedButton("NUEVA TABLA", icon="add", bgcolor=ACCENT_CYAN, color="black", visible=is_admin, on_click=lambda _: page.open(dlg_builder))
        
        def select_t(e):
            t = e.control.data
            schema, count = db_mgr.get_table_schema(t), db_mgr.get_record_count(t)
            detail_view.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Icon("table_rows", color=ACCENT_CYAN, size=40), ft.Text(t, size=32, weight="bold")], alignment="spaceBetween"),
                        ft.Text(f"📦 Métrica: {count} registros almacenados", color="grey400", size=16),
                        ft.Divider(color="white10"),
                        ft.Row([
                            ft.ElevatedButton("EXPORTAR CSV", icon="download", on_click=lambda _: [page.session.set("exp_table", t), page.session.set("exp_fmt", "csv"), ex_p.save_file(file_name=f"{t}.csv")], bgcolor="white10"),
                            ft.ElevatedButton("EXPORTAR JSON", icon="code", on_click=lambda _: [page.session.set("exp_table", t), page.session.set("exp_fmt", "json"), ex_p.save_file(file_name=f"{t}.json")], bgcolor="white10"),
                            ft.IconButton("delete_forever", icon_color="red400", visible=is_admin, on_click=lambda _: [db_mgr.drop_table(t), show_explorer()]),
                        ], spacing=15)
                    ]),
                    padding=30, bgcolor=GLASS_BG, border_radius=BORDER_RADIUS, border=ft.border.all(1, "white10")
                ),
                ft.Text("ESQUEMA DE DATOS (DDL)", weight="bold", color=ACCENT_CYAN),
                ft.Container(content=ft.Text(schema, font_family="monospace", size=11, color="grey300"), padding=25, bgcolor="black", border_radius=15, border=ft.border.all(1, "white10"))
            ]; page.update()

        for t in tables:
            table_list.controls.append(ft.Container(content=ft.ListTile(title=ft.Text(t, size=16, weight="w500"), leading=ft.Icon("table_chart", color=ACCENT_CYAN), on_click=select_t, data=t), bgcolor=GLASS_BG, border_radius=15, ink=True))
        main_content.content = ft.Row([ft.Container(content=ft.Column([ft.Row([ft.Text("TABLAS", weight="bold", color="grey500"), btn_new_table], alignment="spaceBetween"), table_list]), width=280), ft.VerticalDivider(color="white10"), ft.Container(content=detail_view, expand=True)], expand=True)

    def show_sql():
        sql_input = ft.TextField(label="COMANDO SQL", multiline=True, min_lines=6, border_color=ACCENT_CYAN, bgcolor="black26")
        res_view = ft.Column(scroll="adaptive", expand=True)
        def run(e):
            success, r = db_mgr.execute_query(sql_input.value)
            res_view.controls.clear()
            if not success: res_view.controls.append(ft.Text(f"❌ ERROR: {r}", color="red400", weight="bold"))
            else:
                if "columns" in r:
                    res_view.controls.append(ft.Column([ft.Text(f"✅ Ejecutado en {r['time']:.3f}s", color=ACCENT_CYAN), ft.DataTable(columns=[ft.DataColumn(ft.Text(c, color=ACCENT_CYAN)) for c in r["columns"]], rows=[ft.DataRow([ft.DataCell(ft.Text(str(v))) for v in row]) for row in r["data"][:50]], bgcolor="black12", border_radius=15)], scroll="adaptive"))
                else: res_view.controls.append(ft.Text(r["message"], color="green400"))
            page.update()
        main_content.content = ft.Column([ft.Text("CONSOLA SQL INTERACTIVA", size=24, weight="bold", color=ACCENT_CYAN), sql_input, ft.ElevatedButton("EJECUTAR COMANDO", icon="play_arrow", on_click=run, bgcolor=ACCENT_PURPLE, height=50), ft.Divider(color="white10"), res_view], expand=True, spacing=20)

    def show_data():
        main_content.content = ft.Column([ft.Text("HERRAMIENTAS DE ADMINISTRACIÓN", size=24, weight="bold", color=ACCENT_CYAN), ft.Row([ft.Container(content=ft.Column([ft.Icon("cloud_upload", size=60, color=ACCENT_CYAN), ft.Text("IMPORTAR", size=20, weight="bold"), ft.Text("Carga archivos SQL, CSV o JSON.", color="grey500", text_align="center"), ft.ElevatedButton("SELECCIONAR", on_click=lambda _: im_p.pick_files(), bgcolor="white10")], horizontal_alignment="center", spacing=15), padding=40, bgcolor=GLASS_BG, border_radius=30, expand=True), ft.Container(content=ft.Column([ft.Icon("security", size=60, color=ACCENT_PURPLE), ft.Text("RESPALDO", size=20, weight="bold"), ft.Text("Genera un Full Dump del servidor.", color="grey500", text_align="center"), ft.ElevatedButton("DESCARGAR", on_click=lambda _: [page.session.set("exp_fmt", "sql"), ex_p.save_file(file_name="full_backup.sql")], bgcolor="white10")], horizontal_alignment="center", spacing=15), padding=40, bgcolor=GLASS_BG, border_radius=30, expand=True)], spacing=25)], expand=True, spacing=30)

    def show_logs():
        logs = monitor_service.get_logs(50)
        main_content.content = ft.Column([ft.Text("REGISTROS DE ACTIVIDAD", size=24, weight="bold", color=ACCENT_CYAN), ft.DataTable(columns=[ft.DataColumn(ft.Text(c, color=ACCENT_CYAN)) for c in ["TIMESTAMP", "USUARIO", "OPERACIÓN", "ESTADO", "TIEMPO"]], rows=[ft.DataRow([ft.DataCell(ft.Text(str(v))) for v in r]) for r in logs], bgcolor=GLASS_BG, border_radius=15)], expand=True, scroll="adaptive")

    def show_users():
        u_name, u_pass = ft.TextField(label="Nombre de Usuario", border_color=ACCENT_CYAN), ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_color=ACCENT_CYAN)
        u_role = ft.Dropdown(label="Rol", options=[ft.dropdown.Option("admin"), ft.dropdown.Option("user")], value="user", border_color=ACCENT_CYAN)
        user_list_view = ft.Column(spacing=10)
        def load_users():
            user_list_view.controls.clear()
            for u_id, name, role in auth_service.list_users():
                user_list_view.controls.append(ft.Container(content=ft.Row([ft.Icon("person", color=ACCENT_PURPLE), ft.Text(f"{name} ({role})", size=16, expand=True), ft.IconButton("delete", icon_color="red400", on_click=lambda _, n=name: [auth_service.delete_user(n), load_users(), page.update()], visible=(name != user["username"] and name != "admin"))]), padding=15, bgcolor=GLASS_BG, border_radius=15, border=ft.border.all(1, "white10")))
        def add_user(e):
            if not u_name.value or not u_pass.value: return
            success, msg = auth_service.create_user(u_name.value, u_pass.value, u_role.value)
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ACCENT_PURPLE if success else "red800"); page.snack_bar.open = True
            if success: u_name.value, u_pass.value = "", ""; load_users()
            page.update()
        load_users()
        main_content.content = ft.Row([ft.Column([ft.Text("NUEVO USUARIO", weight="bold", color=ACCENT_CYAN), u_name, u_pass, u_role, ft.ElevatedButton("CREAR CREDENCIAL", icon="person_add", on_click=add_user, bgcolor=ACCENT_PURPLE, width=250)], width=300, spacing=20), ft.VerticalDivider(color="white10"), ft.Column([ft.Text("USUARIOS DEL SISTEMA", weight="bold", color="grey500"), user_list_view], expand=True, scroll="adaptive")], expand=True, spacing=30)

    rail_destinations = [ft.NavigationRailDestination(icon="search", label="Explorador"), ft.NavigationRailDestination(icon="terminal", label="Consola SQL"), ft.NavigationRailDestination(icon="settings", label="Herramientas de Datos"), ft.NavigationRailDestination(icon="history", label="Registros de Actividad")]
    if is_admin: rail_destinations.append(ft.NavigationRailDestination(icon="people", label="Administracion de usuarios"))
    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0: show_explorer()
        elif idx == 1: show_sql()
        elif idx == 2: show_data()
        elif idx == 3: show_logs()
        elif idx == 4 and is_admin: show_users()
        page.update()
    nav = ft.NavigationRail(selected_index=0, label_type="all", extended=True, bgcolor="black", destinations=rail_destinations, on_change=on_nav_change)
    app_bar = ft.AppBar(title=ft.Text(f"DATABASE ARCHITECT :: {db_mgr.host}", weight="bold", color=ACCENT_CYAN), bgcolor="black", actions=[ft.IconButton("logout", icon_color="red400", on_click=lambda _: page.go("/"))])
    show_explorer()
    return ft.View("/dashboard", [app_bar, ft.Row([nav, ft.Container(content=main_content, expand=True, bgcolor=BG_DARK)], expand=True, spacing=0)], padding=0)
