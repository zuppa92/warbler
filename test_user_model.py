import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows, Likes

# Set up the test database
os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

# Create all tables and configure app for testing
db.create_all()
app.config['TESTING'] = True

class UserModelTestCase(TestCase):
    """Test model for Users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "test1@test.com", "password", None, None, "bio1", "location1")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "test2@test.com", "password", None, None, "bio2", "location2")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        self.u1 = User.query.get(uid1)
        self.u2 = User.query.get(uid2)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_repr(self):
        """Does the repr method work as expected?"""
        self.assertEqual(repr(self.u1), f"<User #{self.u1.id}: test1, test1@test.com>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""
        self.assertFalse(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        self.u2.following.append(self.u1)
        db.session.commit()

        self.assertTrue(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))

    def test_is_not_followed_by(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""
        self.assertFalse(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))

    def test_user_signup(self):
        """Does User.signup successfully create a new user given valid credentials?"""
        u = User.signup("newuser", "newuser@test.com", "password", None, None, "bio", "location")
        db.session.commit()

        self.assertIsNotNone(u)
        self.assertEqual(u.username, "newuser")
        self.assertEqual(u.email, "newuser@test.com")
        self.assertNotEqual(u.password, "password")  # password should be hashed

    def test_invalid_user_signup(self):
        """Does User.signup fail to create a new user if any of the validations fail?"""
        invalid = User.signup(None, "invalid@test.com", "password", None, None, "bio", "location")
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user when given valid username and password?"""
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.u1.id)

    def test_invalid_username_authenticate(self):
        """Does User.authenticate fail to return a user when the username is invalid?"""
        self.assertFalse(User.authenticate("invalidusername", "password"))

    def test_invalid_password_authenticate(self):
        """Does User.authenticate fail to return a user when the password is invalid?"""
        self.assertFalse(User.authenticate(self.u1.username, "invalidpassword"))

if __name__ == '__main__':
    import unittest
    unittest.main()
