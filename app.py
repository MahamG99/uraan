from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import forms
import yaml
import datetime
import itertools
import random 
# book_iter = 0
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

@app.route('/agent')
def agent():
    return render_template("agents.html", fname=session['fname'], lname=session['lname'], userid=session['userid'], airlinen = session["airline_name"])

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

        value = cur.execute("SELECT first_name, last_name, agent_id,airline_name from agents where password = %s and email = %s", (password,email))
        
        if value >0:
            details = cur.fetchone()
            mysql.connection.commit()
            cur.close()
            session["userid"] = details[2]
            session["airline_name"] = details[3]
            session["fname"] = details[0]
            session["lname"] = details[1]
            return render_template("agents.html" ,fname=details[0], lname=details[1], userid=details[2], airlinen =details[3])
        else:
            return render_template("agentlogin.html" ,form=form, message="Invalid Login")
    else:
        return render_template("agentlogin.html", form=form)

@app.route('/searchflights', methods = ['GET', 'POST'] )
def searchflights():
    # global book_iter
    session["book_iter"] = 0
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
    # global book_iter
    print("I am herrrrrreeeee")
    if session["book_iter"] ==0:
        session["travel_class"] = travel_class
        session["flight"] = flight_no
    num_pass = int(session['num_pass'])
    session["book_iter"] = session["book_iter"] + 1 
   
    if session["book_iter"] != (num_pass + 1):
        form = forms.BookFlightsForm()
        if form.validate_on_submit():
            fname = form.first_name.data
            lname = form.last_name.data
            name = fname +" "+ lname
            nationality = form.nationality.data
            passport_number = form.passport_number.data
            age = form.age.data
            gender = form.gender.data
            pass_dict = {}
            pass_dict["name"] = name
            pass_dict["nationality"] = nationality
            pass_dict["age"] = age
            pass_dict["gender"] = gender
            pass_dict["passport_number"] = passport_number
            pass_dict["customer_id"] = session["userid"]
            pass_dict["travel_class"] = travel_class
            pass_dict["flight_no"] = flight_no
            session["booking"].append(pass_dict)
            if session["book_iter"] == (num_pass):
                return render_template('confirmbooking.html')
        else:
            msg = "Please enter detail of Passenger " + str(session["book_iter"])
            session["book_iter"] = session["book_iter"] - 1
            return render_template("bookflight.html", form = form, message = msg)
    else:
        return render_template('confirmbooking.html')
    return redirect("url_for('bookflight', flight_no = session['flight'], travel_class=session['travel_class'])")

@app.route('/confirmbooking', methods = ['GET', 'POST'] )
def confirmbooking():
    print("HI1")
    check = False
    for i in range(len(session["booking"])):
        print("HI2")
        for j in range(i+1,len(session["booking"])):
            if (session["booking"][i]["name"] == session["booking"][j]["name"]) or session["booking"][i]["passport_number"] == session["booking"][j]["passport_number"]:
                return render_template("confirmbooking.html", message = "Booking Information of two Passengers Matches")

    for people in session["booking"]:
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT * from bookings where passport_number = %s and flight_number = %s", (people["passport_number"], people["flight_no"]))
        if value > 0:
            # detail = cur.fetchall()
            cur.close()
            return render_template("confirmbooking.html", message = "Booking for Some Passenger Already Made")
        else:
            cur.close()

    
    '''CHANGE IT INTO AFTER ONLINE PAYMENT'''
    
    for people in session["booking"]:
        print("HI3")
        check = True
        cur = mysql.connection.cursor()
        print("HEYYYY",session['travel_class'], "BYE")
        cur.execute("INSERT INTO bookings( booking_id, flight_number, passenger_name, customer_id, checkin_status, travel_class, passport_number, gender, nationality, age) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)",
                                            ( session["booking_id"], people["flight_no"], people["name"], people["customer_id"], "0", session["travel_class"], people["passport_number"], people["gender"], people["nationality"] ,people["age"] ) )
        mysql.connection.commit()
        cur.close()
    
    if check == True:
        return render_template("home.html")


    return render_template("confirmbooking.html")


@app.route('/flightstatus', methods = ['GET', 'POST'])
def flightstatus():
    form = forms.FlightStatusForm()
    if form.validate_on_submit():
        flight_no = form.flight_no.data
        curr_date = datetime.date.today()
        cur = mysql.connection.cursor()
        value = cur.execute('SELECT * from Flights WHERE Flight_Number=%s',(flight_no,))
        if value > 0:
            detail = cur.fetchone()
            mysql.connection.commit()
            dep_time = detail[3].date()
            if dep_time < curr_date:
                cur.close()
                return render_template("flightstatus.html", form=form, message = 'Enter Flight Number of Active Flights')                
               
            else:
                cur.close()
                return render_template("flightstatus.html", form=form, display = detail)
        else:
            return render_template("flightstatus.html", form=form, message = "Enter Valid Flight Number")
    else:
        return render_template("flightstatus.html", form=form)

    
@app.route('/onlinePayment', methods=['GET','POST'])
def onlinePayment():
    form = forms.onlinePayment()
    if form.validate_on_submit():
        booking_id = form.booking_id.data
        account_no = form.account_no.data
        security_key = form.security_key.data
        cur = mysql.connection.cursor()

        value = cur.execute("SELECT account_balance, expiry_date from bank where account_number = %s and Security_Key = %s", (account_no, int(security_key)))
        if value > 0:
            details = cur.fetchone()
            mysql.connection.commit()
            user_balance = int(details[0])
            expiry_date = details[1]
            today = datetime.date.today() ############################3 check if this works, comparing card expiry date
            if today > expiry_date: #deletes booking for all passengers associated with that bookingID
                cur.execute("DELETE FROM Bookings where Booking_ID = %s and customer_id=%s", (booking_id, session['userid']))
                mysql.connection.commit()
                return render_template("customer.html", fname=session['fname'],lname=session['lname'], message= "YOUR CARD IS EXPIRED. YOUR BOOKING HAS BEEN REMOVED")
            else:
                value = cur.execute("SELECT price, flight_number from Bookings where Booking_ID = %s", (booking_id,)) ####### needs editing based on number of tickets
                if value > 0:
                    details = cur.fetchall()
                    details = list(details)
                    # print("DETAILS:", details)
                    mysql.connection.commit()
                    price = 0
                    for x in details:
                        price += x[0]

                    flight_no = details[0][1]
                    # print("flight", flight_no)
                    # print("total amount", price)
                    if user_balance < price: #cannot perform transaction
                        cur.execute("DELETE from Bookings where Booking_ID = %s and customer_id=%s", (booking_id, session['userid']))
                        mysql.connection.commit()
                        return render_template("customer.html", fname=session['fname'],lname=session['lname'], message="NOT ENOUGH FUNDS FOR TRANSACTION. YOUR BOOKING HAS BEEN REMOVED")
                    else:
                        value = cur.execute("SELECT airline_name from flights where flight_number = %s", (flight_no,))
                        
                        if value > 0:
                            details = cur.fetchone()
                            mysql.connection.commit()
                            airline_n = details[0]
                            value = cur.execute("SELECT account_number from airline where airline_name = %s", (airline_n,))
                            if value > 0:
                                details = cur.fetchone()
                                mysql.connection.commit()
                                airline_account = details[0] #get airline account number
                                value = cur.execute("SELECT account_balance from bank where account_number = %s", (airline_account,))
                                if value > 0:
                                    details = cur.fetchone()
                                    mysql.connection.commit()
                                    airline_balance = int(details[0])
                                    airline_balance += price
                                    user_balance = user_balance - price
                                    cur.execute("UPDATE bank SET account_balance = %s where account_number = %s", (user_balance, account_no))
                                    mysql.connection.commit()
                                    cur.execute("UPDATE bank SET account_balance = %s where account_number = %s", (airline_balance, airline_account))
                                    mysql.connection.commit()
                                    cur.close()
                                    #add payment_complete
                                    return render_template("customer.html", fname=session['fname'],lname=session['lname'], message="PAYMENT COMPLETE")
                                else:
                                    return "bank does not have this account"
                            else:
                                return "airline does not have bank account number stored"
                        else:
                            return render_template("customer.html", fname=session['fname'],lname=session['lname'], message="Invalid flight")
                else:
                    return render_template("onlinePayment.html",form=form, message="No Matching Booking Found. Please Try Again")
        else:
            return render_template("onlinePayment.html", form=form, message="invalid credentials. Please try again")
    else:
        return render_template("onlinePayment.html", form=form)

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
     
        value = cur.execute("SELECT flight_number from bookings where booking_id = %s and customer_id=%s", (booking_id, session['userid']))
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
            return render_template("customer.html", fname=session['fname'], lname=session['lname'], message="BOOKING NOT FOUND")
    else:
        return render_template("onlineCheckIn.html", form=form)

@app.route('/cancelFlight', methods=['GET','POST'])
def cancelFlight():
    form = forms.cancelFlight()
    if form.validate_on_submit():
        flight_no = form.flight_number.data
        departure = form.departure.data
        arrival = form.arrival.data
        agent = session["userid"]

        cur = mysql.connection.cursor()
        value = cur.execute("SELECT airline_name from agents where Agent_id = %s", (agent,))
        if value > 0:
            details = cur.fetchone()
            mysql.connection.commit()
            airline = details[0]
            print("AIRLINE", airline)
            print("flight_no", flight_no)
            print(flight_no == "PK313")

            value = cur.execute("SELECT departure_time from flights where airline_name = %s and flight_number = %s", (airline, flight_no))
            if value > 0:
                details = cur.fetchone()
                mysql.connection.commit()
                departure_time = details[0]
                print("departure time:", departure_time)
                
                time_now = datetime.datetime.now()
                value = cur.execute("SELECT timediff(%s, %s)", (departure_time, time_now))
                if value >0:
                    hour_diff = cur.fetchone()
                    mysql.connection.commit()
                    hour_diff = hour_diff[0]
                    if value > 0 :
                        check2 = datetime.timedelta(hours=48)
                        if hour_diff > check2: #check if more than 48 hours till flight. if not, can not cancel flight
                            ### CALL DELETE BOOKINGS FOR ALL BOOKINGS FOR THE FLIGHT NUMBER ###
                            cur.execute("DELETE from bookings where flight_number =%s", (flight_no,))
                            mysql.connection.commit()
                            cur.execute("DELETE from flights where flight_number = %s and departure_time=%s", (flight_no, departure_time)) #casacding effect?!?!?
                            mysql.connection.commit()
                            cur.close()
                            return render_template("agents.html", fname=session['fname'], lname=session['lname'], message="FLIGHT CANCELLED SUCCCESSFULLY!")
                        else:
                            return render_template("agents.html",fname=session['fname'], lname=session['lname'], message="YOU CANNOT CANCEL A FLIGHT WITHIN 48 HOURS")
                    else:
                        return "error in getting time difference"
                else:
                    return "TIME DIFF ERROR"
            else:
                return render_template("agents.html", fname=session['fname'], lname=session['lname'], message="FLIGHT NOT FOUND")
        else:
            return render_template("agents.html", fname=session['fname'], lname=session['lname'], message="invaid agent for this task")
    else:
        return render_template("cancelFlight.html", form=form)

@app.route('/cancelBooking',methods=['POST', 'GET'])
def cancelBooking():
    form = forms.cancelBooking()
    if form.validate_on_submit():
        booking_id = form.booking_id.data
        flight_no = form.flight_number.data

        cur = mysql.connection.cursor()
        result = cur.execute("DELETE from bookings where booking_id=%s and flight_number=%s and customer_id = %s", (booking_id, flight_no, session["userid"]))
        mysql.connection.commit()
        cur.close()
        if result > 0:
            return render_template("customer.html", fname=session['fname'], lname=session['lname'], message="YOUR BOOKING HAS BEEN REMOVED")
        else:
            return render_template("customer.html", fname=session['fname'], lname=session['lname'], message="ERROR: COULD NOT REMOVE BOOKING")
    else:
        return render_template("cancelBooking.html", form=form)

@app.route('/addFlight',methods = ['GET','POST'])
def addFlight():
    form = forms.addFlight()
    if form.validate_on_submit():
        flight_no = form.flight_number.data
        departure = form.departure.data
        arrival = form.arrival.data
        departure_time = form.departure_time.data
        arrival_time = form.arrival_time.data
        plane = form.plane_type.data
        status = form.status.data
        econ_price = form.economy_price.data
        buis_price = form.buisness_price.data
        first_price = form.first_class_price.data
        airline_name = session['airline_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO flights(flight_number,departure,arrival, departure_time, arrival_time,airline_name,plane_type,status) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)",
            (flight_no,departure,arrival,departure_time,arrival_time,airline_name,plane,status))
        cur.execute("INSERT INTO `flight price`(flight_number,travel_class,price) VALUES (%s,%s,%s)", (flight_no,'Economy',econ_price))
        cur.execute("INSERT INTO `flight price`(flight_number,travel_class,price) VALUES (%s,%s,%s)", (flight_no,'Buisness',buis_price))
        cur.execute("INSERT INTO `flight price`(flight_number,travel_class,price) VALUES (%s,%s,%s)", (flight_no,'First-Class',first_price))
        mysql.connection.commit()
        cur.close()
        return render_template("agents.html" ,fname= session['fname'], lname=session['lname'], airlinen = session['airline_name'], message = 'Flight Successfully Added')
    else:
        return render_template('addFlight.html',form= form)

@app.route('/updateFlight', methods = ['GET','POST'])
def updateFlight():
    form = forms.updateFlight()
    if form.validate_on_submit():
        flight_no = form.flight_number.data
        departure_time = form.departure_time.data
        arrival_time = form.arrival_time.data
        status = form.status.data
        econ_price = form.economy_price.data
        buis_price = form.buisness_price.data
        first_price = form.first_class_price.data
        cur = mysql.connection.cursor()
        cur.execute("UPDATE flights set departure_time = %s, arrival_time = %s, status = %s where flight_number=%s", (departure_time,arrival_time,status,flight_no))
        cur.execute("UPDATE `flight price` set price = %s where flight_number=%s and travel_class = %s", (econ_price,flight_no,'Economy'))
        cur.execute("UPDATE `flight price` set price = %s where flight_number=%s and travel_class = %s", (buis_price,flight_no,'Buisness'))
        cur.execute("UPDATE `flight price` set price = %s where flight_number=%s and travel_class = %s", (first_price,flight_no,'First-Class'))
        mysql.connection.commit()
        cur.close()
        return render_template("agents.html" ,fname= session['fname'], lname=session['lname'], airlinen = session['airline_name'], message = 'Flight Successfully Updated')
    else:
        return render_template('updateFlight.html',form= form)

if __name__ == '__main__':
    app.run(debug = True)


# @app.route('/history', methods = ['GET', 'POST'])
# def history():
#     cur = mysql.connection.cursor()
#     value = cur.execute('SELECT distinct(Booking_ID), distinct(flight_no) from Bookings WHERE Customer_ID = %s ',(session['userid']))
#     if value > 0:
#         detail = cur.fetchall()

