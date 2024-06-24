import os
from unittest import TestCase
from models import db, User, Message
from app import app, CURR_USER_KEY

# Set up the test database
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Create the tables and do not allow the app to raise exceptions
db.create_all()
app.config['TESTING'] = True

class MessageViewsTestCase(TestCase):
    """Test views for Messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None, header_image_url=None, bio=None, location=None)
        self.testuser_id = 999
        self.testuser.id = self.testuser_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_add_message(self):
        """Can a logged-in user add a message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello", str(resp.data))

    def test_delete_message(self):
        """Can a logged-in user delete their message?"""

        m = Message(
            id=1234,
            text="test message",
            user_id=self.testuser_id
        )
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/messages/1234/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            m = Message.query.get(1234)
            self.assertIsNone(m)
