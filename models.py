# Import SQLAlchemy module for database ORM functionality
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy database instance
db = SQLAlchemy()

# Default image URL for users
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

# Define User model with SQLAlchemy ORM
class User(db.Model):
    # Define table name
    __tablename__ = "users"

    # Define columns for user data
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    # Define a property to get the full name of the user
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Function to connect the Flask application with the SQLAlchemy database
def connect_db(app):
    # Set the Flask application for the SQLAlchemy instance
    db.app = app
    # Initialize the SQLAlchemy instance with the Flask application
    db.init_app(app)
