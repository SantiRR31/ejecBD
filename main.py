import flet as ft
from services.auth_service import AuthService
from services.backup_service import BackupService
from services.monitor_service import MonitorService
from ui.login_view import login_v
from ui.dashboard_view import dashboard_v

# Initialize Core Services
auth_service = AuthService()
backup_service = BackupService()
monitor_service = MonitorService()
backup_service.start_scheduler()

def main(page: ft.Page):
    page.title = "MariaDB Manager Pro"
    page.theme_mode = "dark"
    page.padding = 0
    page.window_width = 1200
    page.window_height = 850
    page.window_resizable = True

    # State management via page.session
    if not page.session.get("user"):
        page.session.set("user", None)
    
    def route_change(e):
        page.views.clear()
        if page.route == "/" or page.route == "":
            page.views.append(login_v(page, auth_service))
        elif page.route == "/dashboard":
            if not page.session.get("user"):
                page.go("/")
                return
            page.views.append(dashboard_v(page, auth_service, monitor_service))
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
