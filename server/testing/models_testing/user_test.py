import pytest
from sqlalchemy.exc import IntegrityError

from server.app import create_app
from server.models import db, User

app = create_app()

class TestUser:
    '''User model tests'''

    def test_has_attributes(self):
        '''has attributes id, username, password_hash, image_url, and bio.'''

        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username="TestUser",
                image_url="https://example.com/image.jpg",
                bio="This is a test bio."
            )
            user.password_hash = "password123"

            db.session.add(user)
            db.session.commit()

            new_user = User.query.filter(User.username == "TestUser").first()

            assert new_user.username == "TestUser"
            assert new_user.image_url == "https://example.com/image.jpg"
            assert new_user.bio == "This is a test bio."
            assert new_user.check_password("password123")

    def test_requires_username(self):
        '''requires username to be present and unique.'''

        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User()
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_username_unique(self):
        '''username must be unique.'''

        with app.app_context():
            User.query.delete()
            db.session.commit()

            user1 = User(username="uniqueuser")
            user1.password_hash = "password1"
            db.session.add(user1)
            db.session.commit()

            user2 = User(username="uniqueuser")
            user2.password_hash = "password2"
            db.session.add(user2)
            with pytest.raises(IntegrityError):
                db.session.commit()
