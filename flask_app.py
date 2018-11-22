from flask import Flask, render_template, flash, redirect, url_for, session, request, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mail import Mail, Message


app = Flask(__name__)
app.config.from_object('configurations')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

btrp = Bootstrap(app)

mail = Mail(app)

from forms import EnterForm, LoginForm, RegisterForm, EditForm, PedidoForm, MessageForm
from models import User, Produto, Pedido, Loja
from datetime import datetime


def send_sync_mail(to, subject, text_body, html_body):
    msg = Message('[DA_teste]' + subject,
                  sender='placeholder', recipients=[to])
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

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
    edit_form.product_name.render_kw = {'placeholder' : old_prod.prod_name}
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

#rota para demostracao de todos os produtos, idealmente, cada produto sera mostrado junto com um link direto
#para sua edicao
@app.route('/all_products', methods=['GET', 'POST'])
@login_required
def all_products():
    page = request.args.get('page', 1, type=int)
    pagination = Produto.query.order_by(Produto.prod_type).paginate(page, error_out=True)
    produtos = pagination.items
    return render_template('all_products.html',
                           produtos=produtos,
                           pagination=pagination)

#rota para form dos pedidos
@app.route('/pedido', methods=['GET', 'POST'])
@login_required
def pedido():
    pedidoform = PedidoForm()

    if pedidoform.validate_on_submit():
        #salvar o pedido em formato de texto
        loja_atual = Loja.query.filter_by(id=current_user.id_loja).first_or_404()
        text = "Loja: %s, pedido de %s, %s unidades" %(loja_atual.store_name,
                                                       pedidoform.product_name,
                                                       pedidoform.units)
        new_pedido = Pedido(date=datetime.utcnow(),
                            request=text,
                            situation=0)
        db.session.add(new_pedido)
        db.commit()
        flash("Novo pedido registrado")
        return redirect(url_for('index'))
    return render_template('pedido.html',
                           form = pedidoform)

@app.route('/contact_us', methods=['GET', 'POST'])
@login_required
def contact_us():
    message_form = MessageForm()
    message_form.textao.render_kw = {'placeholder': 'Digite sua mensagem aqui'}
    if message_form.validate_on_submit():
        try:
            loja = Loja.query.filter_by(id=current_user.id_loja).first_or_404()
            today = datetime.utcnow()
            send_sync_mail('example@gmail.com', 'Report de erro',
                           render_template('pass_email.txt', user=current_user,
                                           loja=loja, day=today.day, month=today.month,
                                           year=today.year),
                           render_template('pass_email.html', user=current_user,
                                           loja=loja, day=today.day, month=today.month,
                                           year=today.year)
                           )
            flash("Aviso de erro realizado.")
            return redirect(url_for('contact_us'))
        except:
            flash("Aviso de erro não realizado, bug.")
            return redirect(url_for('contact_us'))
    else:
        flash("Erro no formulário enviado.")
        return redirect(url_for('contact_us'))
    return render_template('contact.html', form=message_form)