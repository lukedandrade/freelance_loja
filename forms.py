from flask_wtf import FlaskForm as FF
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms import FloatField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange

class LoginForm(FF):
    username = StringField('username', validators=[DataRequired(), Length(16)])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Log in')

class RegisterForm(FF):
    username = StringField('username', validators=[DataRequired(), Length(16)])
    password = PasswordField('password', validators=[DataRequired()])
    c_password = PasswordField('confirm password', validators=[DataRequired()])
    loja_associada = SelectField('loja', validators=[DataRequired()], choices=[('salvo', 'Loja n X')])
    tipo = SelectField('permissions', validators=[DataRequired()], choices=[(0, 'Admin'),
                                                                            (1, 'Funcionário'),
                                                                            (2, 'Matriz')
                                                                            ]
                       )
    submit = SubmitField('Register new account')

class EnterForm(FF):
    product_name = StringField('p_name', validators=[DataRequired(), Length(64)])
    product_unit = SelectField('p_unit_type', validators=[DataRequired()], choices=[('Caixa', 'Caixa')
                                                                                    ]
                               )
    product_price = FloatField('p_price', validators=[DataRequired()])
    product_type = SelectField('p_type', validators=[DataRequired()], choices=[('Bebida', 'Bebida')
                                                                               ]
                               )
    product_stock = IntegerField('p_stock', validators=[DataRequired()])
    submit = SubmitField('Insert new product')

class EditForm(FF):
    product_type = SelectField('p_type', validators=[DataRequired()], choices=[('Bebida', 'Bebida')
                                                                               ]
                               )
    product_price = FloatField('p_price')
    product_unit = SelectField('p_unit_type', validators=[DataRequired()], choices=[('Caixa', 'Caixa')
                                                                                    ]
                               )
    product_stock = IntegerField('p_stock')
    submit = SubmitField('Save changes')
