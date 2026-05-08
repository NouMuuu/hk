from flask import Flask, render_template, request, url_for, redirect, session
import database
from werkzeug.security import generate_password_hash,  check_password_hash
app = Flask(__name__)
app.secret_key = "fdsdfefwfsd"

database.create_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            login = request.form.get('login', '').strip()
            password = request.form.get('password', '')
            repassword = request.form.get('repassword', '')

            if not email or not login or not password:
                return render_template("register.html", error="Пожалуйста, заполните все поля")

            if password == repassword:
                hashed_pw = generate_password_hash(password)
                database.add_user(email, login, hashed_pw)
                return redirect(url_for('login'))
            else:
                return render_template("register.html", error="Пароли не совпадают")
        except Exception as e:
            return render_template("register.html", error=f"Ошибка: {str(e)}")
    
    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        
        user = database.get_user_by_login(login)
        
        if user:
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_login'] = user['login']
                return redirect(url_for('index'))
            else:
                return render_template("login.html", error="Неверный пароль")
        else:
            return render_template("login.html", error="Пользователь не найден")
            
    return render_template("login.html")

@app.route('/boss/<slug>')
def boss_page(slug):
    boss_templates = {
        'mother-moths': 'boss_mother_moths.html',
        'bell-beast': 'boss_bell_beast.html',
        'lais': 'boss_lais.html',
        'fourth-choir': 'boss_fourth_choir.html',
        'wild-fluttermoth': 'boss_wild_fluttermoth.html',
        'skypiercer': 'boss_skypiercer.html',
        'sister-luchina': 'boss_sister_luchina.html',
        'skull-tyrant': 'boss_skull_tyrant.html',
        'widow': 'boss_widow.html',
        'phantom': 'boss_phantom.html',
        'giant-shell-moths': 'boss_giant_shell_moths.html'
    }
    template_name = boss_templates.get(slug)
    if template_name:
        return render_template(template_name)
    return render_template('index.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)