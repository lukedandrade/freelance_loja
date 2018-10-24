from flask_wtf import FlaskForm as FF
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms import FloatField
from wtforms_alchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange
from models import Produto, Loja

def Prodquery():
    return Produto.query

def Lojaquery():
    return Loja.query

class LoginForm(FF):
    username = StringField('username', validators=[DataRequired(), Length(max=16)])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Log in')

class RegisterForm(FF):
    username = StringField('username', validators=[DataRequired(), Length(max=16)])
    password = PasswordField('password', validators=[DataRequired()])
    c_password = PasswordField('confirm password', validators=[DataRequired()])
    loja_associada = QuerySelectField('loja', validators=[DataRequired()], query_factory=Lojaquery, allow_blank=False,
                                      get_label='store_name')
    tipo = SelectField('permissions', validators=[DataRequired()], choices=[(0, 'Admin'),
                                                                            (1, 'Funcionário'),
                                                                            (2, 'Matriz')
                                                                            ]
                       )
    submit = SubmitField('Register new account')

class EnterForm(FF):
    product_name = StringField('p_name', validators=[DataRequired(), Length(max=64)])
    product_unit = SelectField('p_unit_type', validators=[DataRequired()], choices=[('Caixa', 'Caixa')
                                                                                    ]
                               )
    product_price = FloatField('p_price', validators=[DataRequired()])
    prod_id = IntegerField('p_id', validators=[DataRequired()])
    product_type = QuerySelectField('p_type', query_factory=Prodquery, allow_blank=False, get_label='prod_type')
    product_stock = IntegerField('p_stock', validators=[DataRequired()])
    submit = SubmitField('Insert new product')

class EditForm(FF):
    product_name = StringField('p_name', validators=[DataRequired(), Length(max=64)])
    product_type = QuerySelectField('p_type', query_factory=Prodquery, allow_blank=False, get_label='prod_type')
    product_price = FloatField('p_price')
    product_unit = QuerySelectField('p_unit_type', validators=[DataRequired()], query_factory=Prodquery, allow_blank=False, get_label='prod_unit_scale')
    product_stock = IntegerField('p_stock')
    submit = SubmitField('Save changes')


#primeira tentativa do form de pedidos
class PedidoForm(FF):
    product_name = StringField('p_name', validators=[DataRequired(), Length(max=64)])
    units = IntegerField('p_units', validators=[DataRequired()])
    submit = SubmitField('Fazer pedido')
