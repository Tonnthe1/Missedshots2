from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    linkedin = db.Column(db.String(150), nullable=True)
    facebook = db.Column(db.String(150), nullable=True)
    twitter = db.Column(db.String(150), nullable=True)
    github = db.Column(db.String(150), nullable=True)
    phone_visible = db.Column(db.Boolean, default=True)
    linkedin_visible = db.Column(db.Boolean, default=True)
    facebook_visible = db.Column(db.Boolean, default=True)
    twitter_visible = db.Column(db.Boolean, default=True)
    github_visible = db.Column(db.Boolean, default=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    return redirect(url_for('index'))

@app.route('/my_events')
def my_events():
    if 'user_id' in session:
        return render_template('my_events.html')
    return redirect(url_for('index'))

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if request.method == 'POST':
            user.email = request.form['email']
            user.phone_number = request.form['phone_number']
            user.linkedin = request.form['linkedin']
            user.facebook = request.form['facebook']
            user.twitter = request.form['twitter']
            user.github = request.form['github']
            user.phone_visible = 'phone_visible' in request.form
            user.linkedin_visible = 'linkedin_visible' in request.form
            user.facebook_visible = 'facebook_visible' in request.form
            user.twitter_visible = 'twitter_visible' in request.form
            user.github_visible = 'github_visible' in request.form
            if request.form['password']:
                user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
            db.session.commit()
        return render_template('my_account.html', user=user)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
