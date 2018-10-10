from flask import Flask, render_template
from flask_login import LoginManager
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

from forms import EnterForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EnterForm()
    if form.validate_on_submit():
        print(type(form.prod_type_testq.data))
        return '{}'.format(form.prod_type_testq.data)

    return render_template("test.html", form=form)