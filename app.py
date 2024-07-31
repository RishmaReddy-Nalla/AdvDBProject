from flask import Flask, render_template, url_for, request, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'hmsd_rishma'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mongo_user = os.getenv('MONGO_USER')
mongo_pass = os.getenv('MONGO_PASS')

# Mongo Connection Management
client = MongoClient(f'mongodb+srv://{mongo_user}:{mongo_pass}@hmsd.oajv2rn.mongodb.net/?retryWrites=true&w=majority&appName=HMSD')
db = client['HMSD']
users_collection = db['Users']


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": user_id})
        if user_data:
            return User(user_data['_id'], user_data['username'], user_data['password'])
        return None


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.config['MONGO_URI'] = 'mongodb+srv://rishmareddynalla:Reddy040700@hmsd.oajv2rn.mongodb.net/?retryWrites=true&w=majority&appName=HMSD'
mongo = PyMongo(app)
print("Connected to MongoDB")

@app.route("/home")
def index():
    return render_template('home.html')

    
@app.route('/',  methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = users_collection.find_one({"email": email})
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['_id'], user_data['username'], user_data['password'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register')
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        if users_collection.find_one({"username": email}):
            flash('Username already exists')
        else:
            user_id = str(users_collection.insert_one({"username": username, "password": hashed_password}).inserted_id)
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
    return render_template('register.html')



if __name__ == "__main__":
    app.run(debug=True, port=5555, host='0.0.0.0')