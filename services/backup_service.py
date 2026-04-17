import os
import time
import schedule
import threading
from db.database import DBManager

class BackupService:
    def __init__(self, backups_dir="backups"):
        self.backups_dir = backups_dir
        if not os.path.exists(backups_dir):
            os.makedirs(backups_dir)
        self.jobs = {} # {db_name: job}

    def schedule_daily_backup(self, db_params, time_str="00:00"):
        db_name = db_params.get("database", "all")
        job = schedule.every().day.at(time_str).do(
            self.run_backup, db_params
        ).tag(db_name)
        self.jobs[db_name] = job
        return f"Backup programado diariamente para {db_name} a las {time_str}"

    def run_backup(self, db_params):
        try:
            db_inst = DBManager(**db_params)
            db_name = db_params.get("database", "mysql")
            filename = f"backup_{db_name}_{int(time.time())}.sql"
            output_path = os.path.join(self.backups_dir, filename)
            success, path = db_inst.export_database_full(output_path)
            if success:
                print(f"[BackupService] Éxito: {path}")
            else:
                print(f"[BackupService] Fallo: {path}")
        except Exception as e:
            print(f"[BackupService] Error: {e}")

    def start_scheduler(self):
        def run_loop():
            while True:
                schedule.run_pending()
                time.sleep(60)
        thread = threading.Thread(target=run_loop, daemon=True)
        thread.start()
        return thread
