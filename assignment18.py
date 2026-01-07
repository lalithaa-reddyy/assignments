from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  


with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "employee")  

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully!"})

@app.route("/login", methods=["POST"])
def login():
   data = request.get_json()
   username = data.get("username")
   password = data.get("password")
   user = User.query.filter_by(username=username).first()
   if not user or not check_password_hash(user.password, password):
       return jsonify({"msg": "Invalid username or password"}), 401
   token = create_access_token(
       identity=username,
       additional_claims={"role": user.role}
   )
   return jsonify(access_token=token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
   username = get_jwt_identity()
   claims = get_jwt()
   role = claims.get("role")
   return jsonify({
       "msg": "You accessed a protected route!",
       "username": username,
       "role": role
   })


@app.route("/admin-panel", methods=["GET"])
@jwt_required()
def admin_panel():
   claims = get_jwt()
   if claims.get("role") != "admin":
       return jsonify({"msg": "Admins only!"}), 403
   return jsonify({"msg": "Welcome Admin!"})

if __name__ == "__main__":
    app.run(debug=True)
