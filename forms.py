from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, IntegerField, DateField, FieldList, FormField, DateTimeField
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange
from flask_admin.form.widgets import DatePickerWidget
import csv
cities = []
classes= ["Economy", "Business", "First-Class"]
nums= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filter_choices = ["Cheapest", "Quickest", "Earliest Finish", "Earliest Start"]

with open('cities.csv', 'r') as fil:
    cities = fil.read().split('\n')
    cities = cities[1:-1]


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

class SearchFlightsForm(FlaskForm):
    dep = SelectField('Departure',choices = cities,validators = [InputRequired(message = 'Please select an option')])
    arr = SelectField('Arrival',choices = cities,validators = [InputRequired(message = 'Please select an option')] )
    dep_time= DateField('Departure Date (YYYY-MM-DD)',widget=DatePickerWidget(), validators = [InputRequired(message = 'Please select a date')])
    # within = SelectField('')
    travel_class = SelectField('Class',choices = classes ,validators = [InputRequired(message = 'Please select an option')]  )
   
    search_filter = SelectField('Sort By', choices = filter_choices,validators = [InputRequired(message = 'Please select an option')] )
    num_passengers = SelectField('No of Passengers',choices = nums ,validators = [InputRequired(message = 'Please select an option')])
    submit = SubmitField('Search')

class onlinePayment(FlaskForm):
    booking_id = StringField('Booking ID' , validators = [InputRequired(message = 'Field cannot be empty')])
    account_no = StringField('IBAN number', validators = [InputRequired(message = 'Field cannot be empty'), Length(min = 10, max = 10, message = 'Enter a valid account number of 10 characters')])
    security_key = PasswordField('Account Security Key',validators = [InputRequired(message = 'Field cannot be empty')])
    submit = SubmitField('Complete Transaction')

class onlineCheckIn(FlaskForm):
    booking_id = StringField('Booking ID' , validators = [InputRequired(message = 'Field cannot be empty')])
    num_passengers = SelectField('No of Passengers to check-in',choices = nums ,validators = [InputRequired(message = 'Please select an option')])
    passenger_name1 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name2 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name3 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name4 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name5= StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name6 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name7 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name8 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name9 = StringField('Passenger First Name', validators = [Length(max = 20)])
    passenger_name10 = StringField('Passenger First Name', validators = [Length(max = 20)])
    submit = SubmitField('Check In')

class BookFlightsForm(FlaskForm):
    first_name = StringField('First Name', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 20)])
    last_name = StringField('Last Name', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 20)])
    gender = SelectField('Gender', choices = ['Male', 'Female', 'Other'], validators = [InputRequired(message = 'Please select an option')])
    nationality = StringField('Nationality', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 60)])
    passport_number = StringField('Passport Number', validators = [InputRequired(message = 'Field cannot be empty'), Length(min = 9, max = 9, 
        message= 'Passport number should be of length 9')])
    age = IntegerField('Age', validators = [InputRequired(message = 'Field cannot be empty')])
    submit = SubmitField('Next')

# class TempForm(FlaskForm):
#     passenger = FieldList(FormField(BookFlightsForm), min_entries=1 , max_entries=10)
class FlightStatusForm(FlaskForm):
    flight_no = StringField('Flight Number',validators = [InputRequired(message = 'Field cannot be empty')])
    submit = SubmitField('Check Status')

class cancelFlight(FlaskForm):
    flight_number = StringField('Flight Number' , validators = [InputRequired(message = 'Field cannot be empty')])
    departure = SelectField('Departure',choices = cities,validators = [InputRequired(message = 'Please select an option')])
    arrival = SelectField('Arrival',choices = cities,validators = [InputRequired(message = 'Please select an option')] )
    submit= SubmitField('Cancel Flight')

class cancelBooking(FlaskForm):
    booking_id = StringField('Booking ID' , validators = [InputRequired(message = 'Field cannot be empty')])
    flight_number = StringField('Flight Number' , validators = [InputRequired(message = 'Field cannot be empty')])
    # passenger_name = StringField('First Name', validators = [InputRequired(message = 'Field cannot be empty'), Length(max = 20)])
    submit = SubmitField('Cancel Booking')

class addFlight(FlaskForm):
    flight_number = StringField('Flight Number' , validators = [InputRequired(message = 'Field cannot be empty')])
    departure = SelectField('Departure',choices = cities,validators = [InputRequired(message = 'Please select an option')])
    arrival = SelectField('Arrival',choices = cities,validators = [InputRequired(message = 'Please select an option')] )
    departure_time = DateTimeField('Time Departure', format = '%Y-%m-%d %H:%M:%S',validators = [InputRequired(message = 'Field cannot be empty')])
    arrival_time = DateTimeField('Time Arrival', format = '%Y-%m-%d %H:%M:%S',validators = [InputRequired(message = 'Field cannot be empty')])
    plane_type = SelectField('Plane Type', choices = ['Air-Bus','Normal'],validators = [InputRequired(message = 'Please select an option')])
    status = SelectField('Status', choices = ['On-time','Delayed','Cancelled'],validators = [InputRequired(message = 'Please select an option')])
    economy_price = IntegerField('Economy Price', validators = [InputRequired(message = 'Field cannot be empty'),NumberRange(min = 0,message= 'Has to be Positive')])
    buisness_price = IntegerField('Business Price', validators = [InputRequired(message = 'Field cannot be empty'),NumberRange(min = 0,message= 'Has to be Positive')])
    first_class_price = IntegerField('First Class Price', validators = [InputRequired(message = 'Field cannot be empty'),NumberRange(min = 0,message= 'Has to be Positive')])
    submit= SubmitField('Add Flight')

class updateFlight(FlaskForm):
    flight_number = StringField('Flight Number' , validators = [InputRequired(message = 'Field cannot be empty')])
    departure_time = DateTimeField('Time Departure (YYYY-MM-DD HH:MM:SS)', format = '%Y-%m-%d %H:%M:%S',validators = [InputRequired(message = 'Field cannot be empty')])
    arrival_time = DateTimeField('Time Arrival (YYYY-MM-DD HH:MM:SS)', format = '%Y-%m-%d %H:%M:%S',validators = [InputRequired(message = 'Field cannot be empty')])
    status = SelectField('Status', choices = ['On-time','Delayed','Cancelled'],validators = [InputRequired(message = 'Please select an option')])
    economy_price = IntegerField('Economy Price', validators = [InputRequired(message = 'Field cannot be empty'),NumberRange(min = 0,message= 'Has to be Positive')])
    buisness_price = IntegerField('Business Price', validators = [InputRequired(message = 'Field cannot be empty'),NumberRange(min = 0,message= 'Has to be Positive')])
    first_class_price = IntegerField('First Class Price', validators = [InputRequired(message = 'Field cannot be empty'),NumberRange(min = 0,message= 'Has to be Positive')])
    submit= SubmitField('Update Flight')    