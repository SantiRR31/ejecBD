from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database import DBManager
import os

app = Flask(__name__)
CORS(app)

import sqlite3
def init_sqlite():
    conn = sqlite3.connect('app_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  role TEXT,
                  maria_host TEXT,
                  maria_port TEXT,
                  maria_user TEXT,
                  maria_password TEXT,
                  maria_db TEXT)''')
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")
    conn.commit()
    conn.close()

init_sqlite()

db_manager = None

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect('app_users.db')
    c = conn.cursor()
    c.execute("SELECT role, maria_host, maria_port, maria_user, maria_password, maria_db FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        role, m_host, m_port, m_user, m_pass, m_db = user
        return jsonify({
            "success": True, 
            "role": role,
            "maria_config": {
                "host": m_host, "port": m_port, "user": m_user, "password": m_pass, "database": m_db
            } if m_host else None
        })
    return jsonify({"success": False, "message": "Credenciales inválidas"}), 401

@app.route('/api/auth/users', methods=['GET', 'POST'])
def auth_users():
    conn = sqlite3.connect('app_users.db')
    c = conn.cursor()
    if request.method == 'GET':
        c.execute("SELECT id, username, role, maria_db FROM users")
        users = [{"id": r[0], "username": r[1], "role": r[2], "maria_db": r[3] or ""} for r in c.fetchall()]
        conn.close()
        return jsonify(users)
    elif request.method == 'POST':
        data = request.json
        try:
            c.execute("INSERT INTO users (username, password, role, maria_host, maria_port, maria_user, maria_password, maria_db) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (data.get('username'), data.get('password'), data.get('role'), data.get('maria_host'), data.get('maria_port'), data.get('maria_user'), data.get('maria_password'), data.get('maria_db')))
            conn.commit()
            conn.close()
            return jsonify({"success": True})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({"success": False, "message": "El usuario ya existe"})

@app.route('/api/auth/users/<int:user_id>', methods=['DELETE'])
def auth_delete_user(user_id):
    conn = sqlite3.connect('app_users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/api/connect", methods=["POST"])
def connect():
    global db_manager
    data = request.json
    db_manager = DBManager(
        data.get("host"),
        data.get("port", 3307),
        data.get("user"),
        data.get("password"),
        data.get("database")
    )
    success, message = db_manager.connect()
    return jsonify({"success": success, "message": message})

@app.route("/api/tables", methods=["GET"])
def get_tables():
    if not db_manager:
        return jsonify({"success": False, "message": "No conectado"}), 400
    tables = db_manager.list_tables()
    return jsonify({"success": True, "tables": tables})

@app.route("/api/schema/<table_name>", methods=["GET"])
def get_schema(table_name):
    if not db_manager:
        return jsonify({"success": False, "message": "No conectado"}), 400
    schema = db_manager.get_table_schema(table_name)
    return jsonify({"success": True, "schema": schema})

@app.route("/api/export", methods=["GET"])
def export():
    if not db_manager:
        return jsonify({"success": False, "message": "No conectado"}), 400
    filename = f"backup_{db_manager.database}.sql"
    success, result = db_manager.export_database_full(filename)
    if success:
        return send_file(filename, as_attachment=True)
    return jsonify({"success": False, "message": result}), 500

@app.route("/api/export_csv/<table_name>", methods=["GET"])
def export_csv(table_name):
    if not db_manager:
        return jsonify({"success": False, "message": "No conectado"}), 400
    filename = f"{table_name}_export.csv"
    success, result = db_manager.export_table_csv(table_name, filename)
    if success:
        return send_file(filename, as_attachment=True)
    return jsonify({"success": False, "message": result}), 500

@app.route("/api/import", methods=["POST"])
def import_data():
    if not db_manager:
        return jsonify({"success": False, "message": "No conectado"}), 400
    
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No hay archivo"}), 400
    
    target_table = request.form.get("target_table", "csv_import")
    
    file = request.files['file']
    filename = file.filename
    file.save(filename)
    
    try:
        if filename.endswith('.sql'):
            success, message = db_manager.import_sql_file(filename)
        else:
            success, message = db_manager.import_csv_to_table(target_table, filename)
        
        os.remove(filename)
        return jsonify({"success": success, "message": message})
    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/tables/<table_name>", methods=["DELETE"])
def drop_table(table_name):
    if not db_manager:
        return jsonify({"success": False, "message": "No conectado"}), 400
    success, message = db_manager.drop_table(table_name)
    return jsonify({"success": success, "message": message})

@app.route('/api/query', methods=['POST'])
def execute_query():
    if not db_manager:
        return jsonify({"success": False, "message": "No conectado"}), 400
    
    data = request.json
    query = data.get('query', '')
    role = data.get('role', 'admin')
    
    if role == 'user':
        q_upper = query.strip().upper()
        if not (q_upper.startswith('SELECT') or q_upper.startswith('SHOW') or q_upper.startswith('DESCRIBE') or q_upper.startswith('EXPLAIN')):
            return jsonify({
                "success": False, 
                "message": "ACCESO DENEGADO: Tu rol de usuario (solo-lectura) no te permite modificar ni destruir información de esta base de datos.",
                "data": [],
                "columns": []
            })

    if not query:
        return jsonify({"success": False, "message": "No query provided"}), 400
        
    success, result = db_manager.execute_query(query)
    if success:
        return jsonify({"success": True, "result": result})
    else:
        return jsonify({"success": False, "message": result}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)