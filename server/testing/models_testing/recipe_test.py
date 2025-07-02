import pytest
from sqlalchemy.exc import IntegrityError

from server.app import create_app
from server.models import db, Recipe, User

app = create_app()

class TestRecipe:
    '''User in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''

        with app.app_context():

            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(username="testuser")
            user.password_hash = "password"
            db.session.add(user)
            db.session.commit()

            recipe = Recipe(
                    title="Delicious Shed Ham",
                    instructions="""Or kind rest bred with am shed then. In""" + \
                        """ raptures building an bringing be. Elderly is detract""" + \
                        """ tedious assured private so to visited. Do travelling""" + \
                        """ companions contrasted it. Mistress strongly remember""" + \
                        """ up to. Ham him compass you proceed calling detract.""" + \
                        """ Better of always missed we person mr. September""" + \
                        """ smallness northward situation few her certainty""" + \
                        """ something.""",
                    minutes_to_complete=60,
                    user_id=user.id
                    )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter(Recipe.title == "Delicious Shed Ham").first()

            assert new_recipe.title == "Delicious Shed Ham"
            assert new_recipe.instructions == """Or kind rest bred with am shed then. In""" + \
                    """ raptures building an bringing be. Elderly is detract""" + \
                    """ tedious assured private so to visited. Do travelling""" + \
                    """ companions contrasted it. Mistress strongly remember""" + \
                    """ up to. Ham him compass you proceed calling detract.""" + \
                    """ Better of always missed we person mr. September""" + \
                    """ smallness northward situation few her certainty""" + \
                    """ something."""
            assert new_recipe.minutes_to_complete == 60

    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            recipe = Recipe()

            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        with app.app_context():

            Recipe.query.delete()
            db.session.commit()

            '''must raise either a sqlalchemy.exc.IntegrityError with constraints or a custom validation ValueError'''
            with pytest.raises( (IntegrityError, ValueError) ):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="idk lol")
                db.session.add(recipe)
                db.session.commit()
