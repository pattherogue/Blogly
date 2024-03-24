# Import the pytest library for testing
import pytest
# Import the Flask application instance (app), the database instance (db), and the User model from the app module
from app import app, db, User

# Define a pytest fixture named client to set up a test client and a temporary database
@pytest.fixture
def client():
    # Set the app configuration to indicate that testing is enabled
    app.config['TESTING'] = True
    # Set the database URI to a SQLite in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # Set up a test client for the Flask application
    with app.test_client() as client:
        # Use the application context to create all tables in the temporary database
        with app.app_context():
            db.create_all()
            # Yield the test client for use in the test functions
            yield client
            # Drop all tables from the temporary database after the test completes
            db.drop_all()

# Define a test function to test the /users route
def test_users_index(client):
    # Send a GET request to the /users route using the test client
    response = client.get('/users')
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the string "Users" is present in the response data
    assert b"Users" in response.data

# Define a test function to test the user creation functionality
def test_users_new(client):
    # Send a POST request to the /users/new route with mock user data
    response = client.post('/users/new', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'image_url': 'https://example.com/image.jpg'
    })
    # Assert that the response status code is 302 (Redirect)
    assert response.status_code == 302
    # Assert that a user with the first name "John" exists in the database
    assert User.query.filter_by(first_name='John').first()

# Define a test function to test the user detail page
def test_users_show(client):
    # Create a mock user and add it to the database
    user = User(first_name='Jane', last_name='Doe')
    db.session.add(user)
    db.session.commit()
    # Send a GET request to the user detail page for the created user
    response = client.get(f'/users/{user.id}')
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the full name of the user ("Jane Doe") is present in the response data
    assert b"Jane Doe" in response.data

# Define a test function to test the user update functionality
def test_users_update(client):
    # Create a mock user and add it to the database
    user = User(first_name='Jane', last_name='Doe')
    db.session.add(user)
    db.session.commit()
    # Send a POST request to update the user with new data
    response = client.post(f'/users/{user.id}/edit', data={
        'first_name': 'Jane Updated',
        'last_name': 'Doe Updated',
        'image_url': 'https://example.com/image_updated.jpg'
    })
    # Assert that the response status code is 302 (Redirect)
    assert response.status_code == 302
    # Retrieve the updated user from the database
    updated_user = User.query.get(user.id)
    # Assert that the first name, last name, and image URL of the updated user match the new data
    assert updated_user.first_name == 'Jane Updated'
    assert updated_user.last_name == 'Doe Updated'
    assert updated_user.image_url == 'https://example.com/image_updated.jpg'
