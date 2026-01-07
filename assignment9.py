from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:userabc@localhost:5432/testdb1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


with app.app_context():
    db.create_all()
    db_name = db.session.execute(text("SELECT current_database();")).scalar()
    print("Connected to DB:", db_name)

class TestUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    if not username or not email:
        return jsonify({"error": "Missing data"}), 400
    user = TestUser(username=username, email=email)
    db.session.add(user)
    print("engine url:",db.engine.url)
    print(app.config["SQLALCHEMY_DATABASE_URI"])
    db.session.commit()
    
    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201

@app.route("/users", methods=["GET"])
def get_users():
    users = TestUser.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
