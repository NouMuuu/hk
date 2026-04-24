from flask import Flask, render_template, request, url_for, redirect, session
import database
from werkzeug.utils import generate_password_hash,  check_password_hash
app = Flask(__name__)
app.secret_key = "fdsdfefwfsd"

database.create_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        login = request.form['first']
        password = request.form['password']
        repassword = request.form['repassword']

        if password == repassword:
            hashed_pw = generate_password_hash(password)
            database.add_user(email, login, hashed_pw)
            return redirect(url_for('login'))
        else:
            return
    
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        
        user = database.get_user_by_login(login)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_login'] = user['login']
            return redirect(url_for('index'))
        else:
            return
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)