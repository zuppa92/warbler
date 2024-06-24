import os
from unittest import TestCase
from models import db, User, Message, Follows
from app import app, CURR_USER_KEY

# Set up the test database
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="password",
                                    image_url=None,
                                    header_image_url=None,
                                    bio=None,
                                    location=None)
        self.testuser_id = 1234
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("u1", "test1@test.com", "password", None, None, None, None)
        self.u1_id = 1111
        self.u1.id = self.u1_id

        self.u2 = User.signup("u2", "test2@test.com", "password", None, None, None, None)
        self.u2_id = 2222
        self.u2.id = self.u2_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_following_pages_logged_in(self):
        """Can a logged in user see following/followers pages?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/users/{self.u1_id}/following")
            self.assertEqual(resp.status_code, 200)

            resp = c.get(f"/users/{self.u1_id}/followers")
            self.assertEqual(resp.status_code, 200)

    def test_following_pages_logged_out(self):
        """Are logged out users prohibited from seeing following/followers pages?"""

        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}/following", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

            resp = c.get(f"/users/{self.u1_id}/followers", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

    def test_add_message_logged_in(self):
        """Can a logged in user add a message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/messages/new", data={"text": "Test message"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Test message")

    def test_add_message_logged_out(self):
        """Are logged out users prohibited from adding messages?"""

        with self.client as c:
            resp = c.post("/messages/new", data={"text": "Test message"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

            self.assertEqual(Message.query.count(), 0)

    def test_delete_message_logged_in(self):
        """Can a logged in user delete their own message?"""

        msg = Message(text="Test message", user_id=self.testuser.id)
        db.session.add(msg)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(Message.query.count(), 0)

    def test_delete_message_logged_out(self):
        """Are logged out users prohibited from deleting messages?"""

        msg = Message(text="Test message", user_id=self.testuser.id)
        db.session.add(msg)
        db.session.commit()

        with self.client as c:
            resp = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

            self.assertEqual(Message.query.count(), 1)

    def test_delete_other_users_message_logged_in(self):
        """Are logged in users prohibited from deleting other users' messages?"""

        msg = Message(text="Test message", user_id=self.u1.id)
        db.session.add(msg)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

            self.assertEqual(Message.query.count(), 1)

    def test_add_message_as_another_user(self):
        """Are logged in users prohibited from adding messages as another user?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/messages/new", data={"text": "Test message", "user_id": self.u1.id}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

            self.assertEqual(Message.query.count(), 0)
