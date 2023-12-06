from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import random
import time
import os
from flask import current_app
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    designs = db.relationship('Design', backref='user', lazy=True)

# Add new columns to the Room model
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)

    designs = db.relationship('Design', backref='room', lazy=True)


class Furniture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    designs = db.relationship('Design', backref='furniture', lazy=True)

class Customization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colors = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    texture = db.Column(db.String(50), nullable=False)

    designs = db.relationship('Design', backref='customization', lazy=True)

class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    furniture_id = db.Column(db.Integer, db.ForeignKey('furniture.id'), nullable=False)
    customization_id = db.Column(db.Integer, db.ForeignKey('customization.id'), nullable=False)
    # Add other design-related attributes as needed

def create_test_data():
    # Create test users
    test_users = [
        User(id='user1', username='user1', password=bcrypt.generate_password_hash('password1').decode('utf-8')),
        User(id='user2', username='user2', password=bcrypt.generate_password_hash('password2').decode('utf-8'))
    ]

    # Create test rooms, furniture, customizations, and designs
    test_rooms = [
        Room(name='Living Room', user_id='user1'),
        Room(name='Bedroom', user_id='user2')
    ]

    test_furniture = [
        Furniture(name='Sofa', room_id=1),
        Furniture(name='Bed', room_id=2)
    ]

    test_customizations = [
        Customization(colors='Red', size='Large', texture='Leather'),
        Customization(colors='Blue', size='Queen', texture='Fabric')
    ]

    test_designs = [
        Design(user_id='user1', room_id=1, furniture_id=1, customization_id=1),
        Design(user_id='user2', room_id=2, furniture_id=2, customization_id=2)
    ]

    # Add test data to the database
    db.session.bulk_save_objects(test_users + test_rooms + test_furniture + test_customizations + test_designs)
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            user = User(id=username, username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different one.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            # User exists, check password
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Login failed. Incorrect password. Please try again.', 'danger')
        else:
            flash('Login failed. Username not found. Please check your username.', 'danger')

    return render_template('login.html')

# The default route is the home page
@app.route('/')
def home():
    return render_template('home.html')


# the dashboard route 
@app.route('/dashboard')
@login_required
def dashboard():
    data = []
    timestamp = int(time.time())

    # Get the model name from the query parameter
    model_name = request.args.get('model', None)

    return render_template('dashboard.html', username=current_user.username, timestamp=timestamp, data=data, model_name=model_name)

# the furniture route
@app.route('/furniture')
@login_required
def furniture():
    data = []
    timestamp = int(time.time())
    return render_template('Furniture.html', username=current_user.username, timestamp=timestamp, data=data)

# the roomdesign route
@app.route('/roomdesign')
@login_required
def roomdesign():
    data = []
    timestamp = int(time.time())
    return render_template('RoomDesign.html', username=current_user.username, timestamp=timestamp, data=data)

# the customization route
@app.route('/customization')
@login_required
def customization():
    data = []
    timestamp = int(time.time())
    return render_template('customization.html', username=current_user.username, timestamp=timestamp, data=data)

# the logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Helper function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/createroom', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        name = request.form.get('name')
        image = save_room_image(request.files.get('image'))
        color = request.form.get('color')
        date = request.form.get('date')
        price = float(request.form.get('price'))

        room = Room(name=name, image=image, color=color, date=date, price=price, user_id=current_user.id)

        try:
            db.session.add(room)
            db.session.commit()
            flash('Room created successfully.', 'success')
            return redirect(url_for('roomdesign'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating room: {str(e)}', 'danger')

    return render_template('newRoom.html', username=current_user.username)

# save the image to the uploads folder
def save_room_image(image):
    if image:
        upload_folder = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(image.filename)
        filepath = os.path.join(upload_folder, filename)
        image.save(filepath)
        return os.path.relpath(filepath, current_app.root_path)

    return 'placeholder.jpg'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)