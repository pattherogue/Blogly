# Import necessary modules from Flask and other dependencies
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User  # Importing necessary database models

# Create Flask application instance
app = Flask(__name__)

# Configuration for SQLAlchemy database connection URI, track modifications, and secret key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'



# Connect the application with the database and create necessary tables if not exist
with app.app_context():
    connect_db(app)
    db.create_all()

# Root route, redirects to '/users'
@app.route('/')
def root():
    return redirect("/users")

# Route to display all users
@app.route('/users')
def users_index():
    # Query all users from the database and order them by last name, then first name
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

# Route to display form for creating a new user
@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/new.html')

# Route to handle creation of a new user
@app.route("/users/new", methods=["POST"])
def users_new():
    # Create a new User object using data from the form
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    # Add the new user to the database session and commit changes
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

# Route to display information about a specific user
@app.route('/users/<int:user_id>')
def users_show(user_id):
    # Query the database for the user with the given ID, or return a 404 error if not found
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

# Route to display form for editing a specific user
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    # Query the database for the user with the given ID, or return a 404 error if not found
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

# Route to handle updating information about a specific user
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    # Query the database for the user with the given ID, or return a 404 error if not found
    user = User.query.get_or_404(user_id)
    # Update user information with data from the form
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    # Add the updated user to the database session and commit changes
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

# Route to handle deleting a specific user
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    # Query the database for the user with the given ID, or return a 404 error if not found
    user = User.query.get_or_404(user_id)
    # Delete the user from the database session and commit changes
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
