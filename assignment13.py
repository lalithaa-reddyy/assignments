from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "emplo1.db"

def init_db():
    try:
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
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

init_db()

def execute_query(query, args=(), fetch=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return rows

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Employee API is running"})

@app.route("/employees", methods=["GET"])
def get_employees():
    rows = execute_query("SELECT * FROM employees", fetch=True)
    employees = [dict(row) for row in rows]
    return jsonify({"employees": employees})

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()

    name = data.get("name")
    role = data.get("role")
    salary = data.get("salary")

    if not name or not role or not salary:
        return jsonify({"error": "Missing required fields"}), 400

    execute_query(
        "INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)",
        (name, role, salary),
    )
    return jsonify({"message": "Employee added successfully"}), 201

@app.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json()

    name = data.get("name")
    role = data.get("role")
    salary = data.get("salary")

    execute_query(
        "UPDATE employees SET name=?, role=?, salary=? WHERE id=?",
        (name, role, salary, emp_id)
    )
    return jsonify({"message": "Employee updated successfully"})

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    execute_query("DELETE FROM employees WHERE id=?", (emp_id,))
    return jsonify({"message": "Employee deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
#add the urls for postman
