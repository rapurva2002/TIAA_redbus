from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

'''
@app.route('/')
def index():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sample')
    results = cursor.fetchall()
    return str(results)

@app.route('/admin/login')
def login():
    return "login page"

@app.route('/register')
def register():
    return "registration page"

@app.route('/home')
def home():
    return "home page"
'''
@app.route('/landing')
def home():
    return render_template('landing.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        boarding = request.form['boarding']
        destination = request.form['destination']
        departing = request.form['departing'] # Should be date data type
        seat_type = request.form['seat_type']
        adults = int(request.form['adults']) # Should be int data type
        children = int(request.form['children']) # Should be int data type
        travel_class = request.form['travel_class']

        # Insert data into the database
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "INSERT INTO booking (boarding, destination, departing, seat_type, adults, children, travel_class) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (boarding, destination, departing, seat_type, adults, children, travel_class)
            cursor.execute(query, values)
            mysql.connection.commit()
            msg = "Your booking has been saved successfully!"
        except Exception as e:
            msg = "Error occurred while saving your booking: " + str(e)
    else:
        msg = ""

    return render_template('booking.html', msg=msg)

@app.route('/bookings')
def bookings():
    # Fetch all bookings from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM booking')
    bookings = cursor.fetchall()

    # Render the bookings template with the bookings data
    return render_template('bookings.html', bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True)
