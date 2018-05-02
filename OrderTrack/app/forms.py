from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, IntegerField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.models import User

class OrderForm(FlaskForm):
    orderName = StringField('Name of the Order', validators=[DataRequired()])
    dueDate = DateField('Due Date', validators=[DataRequired()])
    carrier = SelectField(u'Available Carriers', validators=[DataRequired()]) #In the view function include: form.carrier.choices = ['Maersk Line']
    container = StringField('Container Number', validators=[DataRequired()])
    po = IntegerField('PO Number', validators=[DataRequired()])
    submit = SubmitField('Track !')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DeleteButton(FlaskForm):
	order_id = HiddenField()
	submit = SubmitField('Delete Order')

class UpdateButton(FlaskForm):
	order_id = HiddenField()
	submit = SubmitField('Update Order')