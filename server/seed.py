from server.app import create_app, db
from server.models import User, Recipe

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(username='testuser1', image_url='https://example.com/image1.jpg', bio='Bio for user 1')
    user1.password_hash = 'password1'

    user2 = User(username='testuser2', image_url='https://example.com/image2.jpg', bio='Bio for user 2')
    user2.password_hash = 'password2'

    db.session.add_all([user1, user2])
    db.session.commit()

    recipe1 = Recipe(
        title='Test Recipe 1',
        instructions='This is a test recipe with instructions that are definitely longer than fifty characters.',
        minutes_to_complete=30,
        user_id=user1.id
    )

    recipe2 = Recipe(
        title='Test Recipe 2',
        instructions='Another test recipe with instructions that exceed the minimum length requirement.',
        minutes_to_complete=45,
        user_id=user2.id
    )

    db.session.add_all([recipe1, recipe2])
    db.session.commit()

    print('Database seeded successfully.')
