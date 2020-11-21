from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class SignUpForm(FlaskForm):
    password = PasswordField('Password', validators = [InputRequired(message = 'Field cannot be empty'), Length(min = 8, max = 8, 
        message= 'Password should be of length 8')])
    first_name = StringField('First Name', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 20)])
    last_name = StringField('Last Name', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 20)])
    email = StringField('Email', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 30), 
        Email(message = 'Please enter a valid email address')])
    confirm_password = PasswordField('Confirm Password', validators = [InputRequired(message = 'Field cannot be empty'), 
        EqualTo('password')])
    gender = SelectField('Gender', choices = ['Male', 'Female', 'Other'], validators = [InputRequired(message = 'Please select an option')])
    nationality = StringField('Nationality', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 60)])
    passport_number = StringField('Passport Number', validators = [InputRequired(message = 'Field cannot be empty'), Length(min = 9, max = 9, 
        message= 'Passport number should be of length 9')])
    phone_number = StringField('Phone Number', validators = [InputRequired(message = 'Field cannot be empty')])
    age = IntegerField('Age', validators = [InputRequired(message = 'Field cannot be empty')])
    account_no = StringField('IBAN number', validators = [InputRequired(message = 'Field cannot be empty'), Length(min = 10, max = 10, message = 'Enter a valid account number of 10 characters')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators = [InputRequired(message = 'Field cannot be empty')])
    email = StringField('Email', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 30), 
        Email(message = 'Please enter a valid email address')])
    submit = SubmitField('Log In')