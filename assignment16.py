from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "salary": self.salary
        }
with app.app_context():
    db.create_all()

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    name = data.get("name")
    department = data.get("department")
    salary = data.get("salary")
    if not name or not department or salary is None:
        return jsonify({"msg": "Missing fields"}), 400
    new_emp = Employee(name=name, department=department, salary=salary)
    db.session.add(new_emp)
    db.session.commit()
    return jsonify({"msg": "Employee added", "employee": new_emp.to_dict()}), 201

@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])

@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"msg": "Employee not found"}), 404
    return jsonify(emp.to_dict())

@app.route("/employees/<int:id>", methods=["PUT", "PATCH"])
def update_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"msg": "Employee not found"}), 404
    data = request.get_json()
    emp.name = data.get("name", emp.name)
    emp.department = data.get("department", emp.department)
    emp.salary = data.get("salary", emp.salary)
    db.session.commit()
    return jsonify({"msg": "Employee updated", "employee": emp.to_dict()})

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"msg": "Employee not found"}), 404
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"msg": "Employee deleted"})

if __name__ == "__main__":
    app.run(debug=True)

 