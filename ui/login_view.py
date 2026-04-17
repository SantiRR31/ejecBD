import flet as ft
from services.auth_service import AuthService
from db.database import DBManager

def login_v(page: ft.Page, auth_service: AuthService):
    page.views.clear()
    
    # Manager User Fields
    username_field = ft.TextField(label="Usuario Administrador", width=350, prefix_icon="person", value="admin")
    password_field = ft.TextField(label="Contraseña", password=True, width=350, can_reveal_password=True, prefix_icon="lock", value="admin123")
    
    # MariaDB Fields
    host_field = ft.TextField(label="Host MariaDB", width=350, value="localhost")
    port_field = ft.TextField(label="Puerto", width=350, value="3307")
    db_user_field = ft.TextField(label="Usuario DB", width=350, value="root")
    db_pass_field = ft.TextField(label="Password DB", width=350, password=True)
    db_name_field = ft.TextField(label="Base de Datos", width=350)
    
    error_text = ft.Text("", color="red400")

    config_container = ft.Column([
        ft.Text("CONFIGURACIÓN DE CONEXIÓN", size=16, weight="bold", color="sky400"),
        host_field, port_field, db_user_field, db_pass_field, db_name_field
    ], spacing=10, scroll="adaptive", visible=True)
    
    user_container = ft.Column([
        ft.Text("ACCESO AL PANEL", size=16, weight="bold", color="sky400"),
        username_field, password_field
    ], spacing=10, visible=False)
    
    def switch_view(e):
        config_container.visible = not config_container.visible
        user_container.visible = not user_container.visible
        btn_switch.text = "CONFIGURAR CONEXIÓN" if user_container.visible else "DATOS DE USUARIO"
        page.update()

    btn_switch = ft.TextButton("DATOS DE USUARIO", on_click=switch_view)

    def handle_login(e):
        success_auth, res_auth = auth_service.login(username_field.value, password_field.value)
        if not success_auth:
            error_text.value = f"Error de Acceso: {res_auth}"
            page.update()
            return
        
        db_params = {
            "host": host_field.value, "port": port_field.value, "user": db_user_field.value,
            "password": db_pass_field.value, "database": db_name_field.value
        }
        mgr = DBManager(host_field.value, int(port_field.value), db_user_field.value, db_pass_field.value, db_name_field.value)
        success_db, msg_db = mgr.connect()
        
        if success_db:
            page.session.set("user", res_auth)
            page.session.set("db_manager", mgr)
            page.session.set("db_params", db_params)
            page.go("/dashboard")
        else:
            error_text.value = f"Error MariaDB: {msg_db}"
            page.update()

    return ft.View(
        "/",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([ft.Icon("database", size=40, color="sky400"), ft.Text("MariaDB Manager Pro", size=28, weight="bold")], alignment="center"),
                        ft.Divider(height=20, color="transparent"),
                        ft.Container(
                            content=ft.Column([config_container, user_container]),
                            bgcolor="grey900",
                            padding=20,
                            border_radius=15,
                            border=ft.border.all(1, "grey800"),
                            width=400
                        ),
                        btn_switch,
                        ft.ElevatedButton("CONECTAR Y ENTRAR", on_click=handle_login, width=350, height=50, 
                                          style=ft.ButtonStyle(bgcolor="sky700", color="white")),
                        error_text
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=20
                ),
                expand=True,
                padding=50,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["grey900", "blue900"]
                )
            )
        ]
    )
