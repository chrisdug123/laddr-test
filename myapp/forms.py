from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class LocationForm(FlaskForm):
    location_name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')

class CheckinForm(FlaskForm):
    location_name=StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Checkin')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')
        
    #def validate_email(self,email):
    #    user = User.query.filter_by(email=email.data).first()
    #    if user:
    #        raise ValidationError('Please user a different email address')
        

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


    
#class RecipeForm(FlaskForm):
#    title = StringField('Title', validators=[DataRequired()])
#    description = TextAreaField('Description', validators=[DataRequired()])
#    submit = SubmitField('Post')
