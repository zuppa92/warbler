import os
from unittest import TestCase
from models import db, User, Message
from app import app

# Set up the test database
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Create the tables and do not allow the app to raise exceptions
db.create_all()
app.config['TESTING'] = True

class MessageModelTestCase(TestCase):
    """Test model for Messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "test1@test.com", "password", None, None, None, None)
        uid1 = 1111
        u1.id = uid1
        db.session.commit()

        self.u1 = User.query.get(uid1)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(
            text="Test message",
            user_id=self.u1.id
        )

        db.session.add(m)
        db.session.commit()

        # User should have one message
        self.assertEqual(len(self.u1.messages), 1)
        self.assertEqual(self.u1.messages[0].text, "Test message")
