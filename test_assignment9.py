import unittest
from assignment9 import app, db, User
import json

class UserTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://userabc:userabc@localhost:5432/testdb1_test"
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user_success(self):
        res = self.app.post("/users", json={"username": "john", "email": "john@example.com"})
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data["username"], "john")
        self.assertEqual(data["email"], "john@example.com")

    def test_create_user_missing_data(self):
        res = self.app.post("/users", json={"username": "john"})
        self.assertEqual(res.status_code, 400)

    def test_get_users(self):
        with app.app_context():
            user = User(username="alice", email="alice@example.com")
            db.session.add(user)
            db.session.commit()
        res = self.app.get("/users")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["username"], "alice")

if __name__ == "__main__":
    unittest.main()
