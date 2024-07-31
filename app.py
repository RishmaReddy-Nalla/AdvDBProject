from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.secret_key = 'hmsd_rishma'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


users = {}


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


app.config['MONGO_URI'] = 'mongodb+srv://rishmareddynalla:Reddy040700@hmsd.oajv2rn.mongodb.net/?retryWrites=true&w=majority&appName=HMSD'
mongo = PyMongo(app)
print("Connected to MongoDB")

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')




if __name__ == "__main__":
    app.run(debug=True, port=5555, host='0.0.0.0')