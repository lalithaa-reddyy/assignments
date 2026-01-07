from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DB_NAME = "employee.db"
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
init_db()

def execute_query(query, args=(), fetch=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    data = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data

@app.route("/")
def home():
    rows = execute_query("SELECT * FROM employees", fetch=True)
    employees = [dict(row) for row in rows]
    return render_template("index.html", employees=employees)


@app.route("/employees", methods=["GET"])
def get_employees():
    rows = execute_query("SELECT * FROM employees", fetch=True)
    employees = [dict(row) for row in rows]
    return jsonify({"employees": employees})

@app.route("/employees", methods=["POST"])
def employee_actions():
    data = request.form
    action = data.get("action")
    
    if action == "add":
        name = data.get("name")
        role = data.get("role")
        salary = data.get("salary")
        execute_query("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)",
                      (name, role, salary))
    
    elif action == "update":
        emp_id = data.get("id")
        name = data.get("name")
        role = data.get("role")
        salary = data.get("salary")
        execute_query("UPDATE employees SET name=?, role=?, salary=? WHERE id=?",
                      (name, role, salary, emp_id))
    
    elif action == "delete":
        emp_id = data.get("id")
        execute_query("DELETE FROM employees WHERE id=?", (emp_id,))
    
    return home() 


if __name__ == "__main__":
    app.run(debug=True)
