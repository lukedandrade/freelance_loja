from flask import Flask, render_template, flash, redirect, url_for, session, request, g
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('configurations')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

btrp = Bootstrap(app)

from forms import EnterForm, LoginForm, RegisterForm
from models import User


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EnterForm()
    if form.validate_on_submit():
        print(type(form.prod_type_testq.data))
        return '{}'.format(form.prod_type_testq.data)

    return render_template("test.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me)
            flash('Login do usuário %s' % user.username)
            return redirect(url_for('index'))
        flash('Username ou senha inválida')
    return render_template('login_pg.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if register_form.password.data == register_form.c_password.data:
            new_user = User(permissions=register_form.tipo.data,
                            username=register_form.username.data,
                            password=register_form.password.data,
                            id_loja=register_form.loja_associada.data.id
                            )
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário %s criado com sucesso' % new_user.username)
            return redirect(url_for('login'))
        else:
            flash('Senhas digitadas não estão iguais')
            return redirect(url_for('register'))
    return render_template('register_pg.html', form=register_form)