from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import forms
import yaml
import datetime
import itertools
import random 
book_iter = 0
class Booking:
    def __init__(self, full_name, nationality, gender, passport_number, age):
        self.full_name = full_name
        self.nationality = nationality
        self.gender = gender
        self.passport_number = passport_number
        self.age = age
        self.flight_no = session['flight']
        self.travel_class = session['travel_class']
        self.checkin_status = 0
        self.seat_no = None
        self.customer_id = session['userid']
        self.price = 0
    def add_seat_no(self, seat_no):
        self.seat_no = seat_no
    def add_price(self, price):
        self.price = price


app = Flask(__name__)
db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SECRET_KEY'] = 'password'

mysql = MySQL(app)

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/customer')
def customer():
    return render_template("customer.html", fname=session['fname'], lname=session['lname'])

@app.route('/signup' ,methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        gender = form.gender.data
        nationality = form.nationality.data
        passport_number = form.passport_number.data
        phone_number = form.phone_number.data
        age = form.age.data
        account_no = form.account_no.data
        discount = 0
        flyer_points = 0
        cur = mysql.connection.cursor()
        
        cur.execute("INSERT INTO customers( first_name, last_name, email, gender, password, phone_number, nationality, age, flyer_points, account_number, discount, passport_number ) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                                          (  first_name,last_name, email, gender, password, phone_number, nationality, age, flyer_points, account_no, discount, passport_number))
        
        mysql.connection.commit()
        cur.close()
        return "Successfully Signed up!"
    else:
        return render_template("signup.html", form = form)


@app.route('/customerlogin' ,methods=['GET', 'POST'])
def customerlogin():
    form = forms.LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        cur = mysql.connection.cursor()

        value = cur.execute("SELECT first_name, last_name, customer_id from customers where password = %s and email = %s", (password,email))
        if value >0:
            details = cur.fetchone()
            session["userid"] = details[2]
            session["fname"] = details[0]
            session["lname"] = details[1]
            return render_template("customer.html",fname=details[0], lname=details[1], userid = details[2])
        else:
            return render_template("customerlogin.html", form=form, message= "Invalid LogIn")
        mysql.connection.commit()
        cur.close()
    else:
        return render_template("customerlogin.html", form=form)
@app.route('/agentlogin' ,methods=['GET', 'POST'])
def agentlogin():
    form = forms.LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        cur = mysql.connection.cursor()

        value = cur.execute("SELECT first_name, last_name from agents where password = %s and email = %s", (password,email))
        
        if value >0:
            details = cur.fetchone() 
            return render_template("agents.html" ,fname=details[0], lname=details[1])
        else:
            return "Invalid Login"
        mysql.connection.commit()
        cur.close()
    else:
        return render_template("agentlogin.html", form=form)

@app.route('/searchflights', methods = ['GET', 'POST'] )
def searchflights():
    global book_iter
    book_iter = 0
    form = forms.SearchFlightsForm()
    check = True
    while (check == True):
        temp_book_id = random.randrange(10000, 99999)
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT DISTINCT(Booking_ID) FROM Bookings WHERE Booking_ID = %s", (str(temp_book_id),))
        
        if value > 0:
            pass
        else:
            break
        mysql.connection.commit()
        cur.close()
    session['booking_id'] = temp_book_id
    session['booking'] = []

    if form.validate_on_submit():
        dep = form.dep.data
        arr = form.arr.data
        dep_time = form.dep_time.data
        travel_class = form.travel_class.data
        num_pass = form.num_passengers.data
        session["num_pass"] = int(num_pass)
        search_filter = form.search_filter.data
        if search_filter == "Cheapest":
            cur = mysql.connection.cursor()
            value = cur.execute("SELECT * FROM (Uraan.Flights natural join `Flight Price`) WHERE arrival=%s and departure=%s and travel_class = %s and departure_time >=%s and departure_time <= DATE_ADD(%s, INTERVAL 8 DAY)ORDER BY price ASC;", 
                                                                                                (arr,dep ,travel_class,dep_time, dep_time))  
            if value >0:
                detail = cur.fetchall()
                return render_template("searchflights.html", form=form, display = detail)
            else:
                return render_template("searchflights.html",message = "NO FLIGHTS FOUND!!!", form=form)
            mysql.connection.commit()
            cur.close()
        elif search_filter == "Earliest Finish":
            cur = mysql.connection.cursor()
            value = cur.execute("SELECT * FROM (Uraan.Flights natural join `Flight Price`) WHERE arrival=%s and departure=%s and travel_class = %s and departure_time >=%s and departure_time <= DATE_ADD(%s, INTERVAL 8 DAY)ORDER BY arrival_time ASC;", 
                                                                                                (arr,dep ,travel_class,dep_time, dep_time))  
            if value >0:
                detail = cur.fetchall()
                return render_template("searchflights.html", form=form, display = detail)
            else:
                return render_template("searchflights.html",message = "NO FLIGHTS FOUND!!!", form=form)
            mysql.connection.commit()
            cur.close()
        elif search_filter == "Earliest Start":
            cur = mysql.connection.cursor()
            value = cur.execute("SELECT * FROM (Uraan.Flights natural join `Flight Price`) WHERE arrival=%s and departure=%s and travel_class = %s and departure_time >=%s and departure_time <= DATE_ADD(%s, INTERVAL 8 DAY)ORDER BY departure_time ASC;", 
                                                                                                (arr,dep ,travel_class,dep_time, dep_time))  
            if value >0:
                detail = cur.fetchall()
                return render_template("searchflights.html", form=form, display = detail)
            else:
                return render_template("searchflights.html",message = "NO FLIGHTS FOUND!!!", form=form)
            mysql.connection.commit()
            cur.close()
        elif search_filter == "Quickest":
            cur = mysql.connection.cursor()
            value = cur.execute("SELECT * FROM (Uraan.Flights natural join `Flight Price`) WHERE arrival=%s and departure=%s and travel_class = %s and departure_time >=%s and departure_time <= DATE_ADD(%s, INTERVAL 8 DAY)ORDER BY (arrival_time - departure_time) ASC;", 
                                                                                                (arr,dep ,travel_class,dep_time, dep_time))  
            if value >0:
                detail = cur.fetchall()
                return render_template("searchflights.html", form=form, display = detail)
            else:
                return render_template("searchflights.html",message = "NO FLIGHTS FOUND!!!", form=form)
            mysql.connection.commit()
            cur.close()
        
    return render_template("searchflights.html", form=form)

@app.route('/bookflight/<int:flight_no>/<string:travel_class>', methods = ['GET', 'POST'] )
def bookflight(flight_no, travel_class):
    global book_iter
    print("I am herrrrrreeeee")
    session["flight"] = flight_no
    session["travel_class"] = travel_class
    num_pass = int(session['num_pass'])
    print(num_pass)
    print("KHABEES", session['travel_class'])
    book_iter = book_iter + 1 
    print("HI", book_iter)
   
    if book_iter != (num_pass + 1):
        form = forms.BookFlightsForm()
        if form.validate_on_submit():
            fname = form.first_name.data
            lname = form.last_name.data
            name = fname + lname
            nationality = form.nationality.data
            passport_number = form.passport_number.data
            age = form.age.data

            print("bye", book_iter)
            if book_iter == (num_pass):
                return render_template("home.html")
        else:
            msg = "Please enter detail of Passenger " + str(book_iter)
            book_iter = book_iter - 1
            return render_template("bookflight.html", form = form, message = msg)
    else:
        return render_template("home.html")
    return redirect("url_for('bookflight', flight_no = session['flight'], travel_class=session['travel_class'])")



@app.route('/onlineCheckIn', methods=['GET','POST'])
def onlineCheckIn():
    form = forms.onlineCheckIn()
    if form.validate_on_submit():
        booking_id = form.booking_id.data
        num_pass = form.num_passengers.data
        num = int(num_pass)
        pass_name = []
        
        pass_name.append(form.passenger_name1.data)
        pass_name.append(form.passenger_name2.data)
        pass_name.append(form.passenger_name3.data)
        pass_name.append(form.passenger_name4.data)
        pass_name.append(form.passenger_name5.data)
        pass_name.append(form.passenger_name6.data)
        pass_name.append(form.passenger_name7.data)
        pass_name.append(form.passenger_name8.data)
        pass_name.append(form.passenger_name9.data)
        pass_name.append(form.passenger_name10.data)

        cur = mysql.connection.cursor()
        value = cur.execute("SELECT flight_number from bookings where booking_id = %s", (booking_id))
        if value >0:
            detail = cur.fetchall()
            flight = detail[0]
            mysql.connection.commit()
          
            value = cur.execute("SELECT departure_time from flights where flight_number = %s", (flight))
            if value > 0:
                detail = cur.fetchone()
                dep_time = detail[0]
                mysql.connection.commit()
                #check if not already checkedin
                checkedin_already = []
                valid_passenger = []

                #find passengers who have already checkedin
                value = cur.execute("SELECT passenger_name from bookings where booking_id=%s and checkin_status=%s and flight_number=%s", (booking_id,1,flight))
                mysql.connection.commit()
                if value > 0:
                    detail = cur.fetchall()
                    for i in detail:
                        checkedin_already.append(i)
                checkedin_already = list(itertools.chain(*checkedin_already)) 
                
                # find out valid passengers associated with current booking and flight
                value = cur.execute("SELECT passenger_name from bookings where booking_id=%s and flight_number=%s", (booking_id,flight)) 
                mysql.connection.commit()
                if value > 0:
                    detail = cur.fetchall()
                    for i in detail:
                        valid_passenger.append(i)
                
                valid_passenger = list(itertools.chain(*valid_passenger))
                valid_passenger = [x.lower() for x in valid_passenger]
                checkedin_already = [x.lower() for x in checkedin_already]
                print("checkedin_already", checkedin_already)
                print("valid_passenger:" , valid_passenger)

                time_now = datetime.datetime.now()
                value = cur.execute("SELECT timediff(%s, %s)", (dep_time, time_now))
                hour_diff = cur.fetchone()
                mysql.connection.commit()
                hour_diff = hour_diff[0] 
                if value > 0 :
                    check1 = datetime.timedelta(hours=12)
                    check2 = datetime.timedelta(hours=48)
                    if hour_diff >= check1 and hour_diff<= check2:
                        checking_in = []
                        not_checking = []
                        invalid = []
                        for name in pass_name:
                            name = name.lower()
                            if (name not in checkedin_already) and (name in valid_passenger):
                                cur.execute("UPDATE bookings set checkin_status = %s where booking_id=%s and passenger_name=%s", (1,booking_id,name))
                                mysql.connection.commit()
                                checking_in.append(name)  
                            elif name in valid_passenger:
                                if name != "":
                                    not_checking.append(name)
                            else:
                                if name != "":
                                    invalid.append(name)
                        return render_template("customer.html",fname=session['fname'], lname=session['lname'], display= [checking_in, not_checking, invalid])
                        cur.close()
                    else:
                        return render_template("customer.html",fname=session['fname'], lname=session['lname'], message="Sorry, your time of check-in is not valid. Please check-in between 40 and 48 hours of the flight")
            else:
                render_template("customer.html", fname=session['fname'], lname=session['lname'], message="FLIGHT NOT FOUND")
        else:
            return render_template("customer.html", fname=session['fname'], lname=session['lname'], message="FLIGHT NOT FOUND")
    else:
        return render_template("onlineCheckIn.html", form=form)

if __name__ == '__main__':
    app.run(debug = True)

