from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import forms
import yaml

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

        value = cur.execute("SELECT first_name, last_name from customers where password = %s and email = %s", (password,email))
        if value >0:
            details = cur.fetchone()
           
            return render_template("customer.html",fname=details[0], lname=details[1])
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

        
if __name__ == '__main__':
    app.run(debug = True)

