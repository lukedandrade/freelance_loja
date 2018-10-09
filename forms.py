from flask_wtf import FlaskForm as FF
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange