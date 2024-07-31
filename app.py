from flask import Flask, render_template, url_for, request, flash, redirect
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.utils import MongoConn
import os
from werkzeug.security import generate_password_hash, check_password_hash
from models.appointments import get_appointments

app = Flask(__name__)
app.secret_key = 'hmsd_rishma'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mongo_user = os.getenv('MONGO_USER')
mongo_pass = os.getenv('MONGO_PASS')
print(mongo_user,mongo_pass)

users_collection = MongoConn().connect()['Users']
print("connected to DB!!!")


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": user_id})
        if user_data:
            return User(user_data['_id'], user_data['email'], user_data['password'])
        return None


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/home")
def home():
    appointment = get_appointments('Appointments')
    return render_template('home.html', appointment=appointment)

    
@app.route('/',  methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = users_collection.find_one({"email": email})
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['_id'], user_data['email'], user_data['password'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        if users_collection.find_one({"email": email}):
            flash('Username already exists')
        else:
            user_id = str(users_collection.insert_one({"email": email, "password": hashed_password, "first_name": fname, "last_name": lname, "phone": phone}).inserted_id)
            flash(f'Registration successful! Please login. User ID:  {user_id}')
            return redirect(url_for('login'))
    return render_template('register.html')



if __name__ == "__main__":
    app.run(debug=True, port=5555, host='0.0.0.0')