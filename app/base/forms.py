# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])

class ProductForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = TextField('name', validators=[DataRequired()])
    price = TextField('price', validators=[DataRequired()])
    count = TextField('count', validators=[DataRequired()])
    image = TextField('image')
    is_refundable = BooleanField('is_refundable', default=False)
    submit = SubmitField('submit') 
