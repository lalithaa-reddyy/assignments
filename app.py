from flask import Flask, request, jsonify
import os
import importlib.util

# Load local modules explicitly to avoid clashes with top-level modules
def _load_local(module_name, filename):
    base = os.path.dirname(__file__)
    path = os.path.join(base, filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

_db_mod = _load_local('employee_api.database', 'database.py')
db = _db_mod.db
_models_mod = _load_local('employee_api.models', 'models.py')
Employee = _models_mod.Employee

app = Flask(__name__)

# Database configuration (SQLite for demo — replace with PostgreSQL)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])

@app.route("/employees/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(emp.to_dict())

@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.json
    emp = Employee(
        name=data["name"],
        email=data["email"],
        role=data["role"]
    )
    db.session.add(emp)
    db.session.commit()
    return jsonify(emp.to_dict()), 201

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message": "Employee deleted"})
