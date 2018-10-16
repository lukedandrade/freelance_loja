from flask import Flask, render_template, flash, redirect, url_for, session, request, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
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

from forms import EnterForm, LoginForm, RegisterForm, EditForm
from models import User, Produto


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
@login_required
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
            flash('Usuário %s criado com sucesso.' % new_user.username)
            return redirect(url_for('login'))
        else:
            flash('Senhas digitadas não estão iguais.')
            return redirect(url_for('register'))
    return render_template('register_pg.html', form=register_form)

@app.route('/new_prod', methods=['GET', 'POST'])
@login_required
def register_product():
    new_prod_form = EnterForm()
    if new_prod_form.validate_on_submit():
        try:
            tipo = new_prod_form.product_type.data.prod_type
            new_prod = Produto(id_produto=new_prod_form.prod_id.data,
                               prod_name=new_prod_form.product_name.data,
                               prod_unit_scale=new_prod_form.product_unit.data,
                               prod_value=new_prod_form.product_price.data,
                               prod_reserve=new_prod_form.product_stock.data,
                               prod_type=tipo)
            db.session.add(new_prod)
            db.session.commit()
            flash('Novo produto registrado com sucesso.')
            return redirect(url_for('index'))

        except:
            flash('Erro quanto ao registro do novo produto.')
            return redirect(url_for('new_prod'))

    return render_template('prod_register.html', form=new_prod_form)

@app.route('/edit_prod/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    old_prod = Produto.query.filter_by(id=id).first_or_404()
    edit_form = EditForm()
    edit_form.product_price.render_kw = {'placeholder' : old_prod.prod_value}
    edit_form.product_stock.render_kw = {'placeholder' : old_prod.prod_reserve}

    if edit_form.validate_on_submit():
        old_prod.prod_value = edit_form.product_price.data
        old_prod.prod_reserve = edit_form.product_stock.data
        old_prod.prod_type = edit_form.product_type.data.prod_type
        old_prod.prod_unit_scale = edit_form.product_unit.data.prod_unit_scale

        try:
            db.session.commit()
            flash('Atualização de produto realizada com sucesso.')
            return redirect(url_for('index'))

        except:
            flash('Atualização falhou')
            return redirect(url_for(('index')))

    return render_template('prod_edit.html', form=edit_form)