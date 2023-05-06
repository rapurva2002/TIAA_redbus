from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from geopy.geocoders import Nominatim
import haversine as hs
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.pdfgen import canvas
from flask_mail import Message
app = Flask(__name__)


app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.config['SECRET_KEY'] = 'bus'
app.config['SESSION_TYPE'] = 'filesystem'



mysql = MySQL(app)


@app.route('/user/login', methods =['GET', 'POST'])
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
	if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
		name = request.form['name']
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


@app.route('/operator/login', methods =['GET', 'POST'])
def operatorlogin():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM registration WHERE email = % s AND password = % s', (email, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['email'] = account['email']
			msg = 'Logged in successfully !'
			return render_template('index1.html', msg = msg)
		else:
			msg = 'Incorrect email / password !'
	return render_template('operatorlogin.html')

@app.route('/operator/logout')
def operatorlogout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/operator/register', methods=['GET', 'POST'])
def operatorregister():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'dob' in request.form and 'email' in request.form and 'password' in request.form and 'mobilenumber' in request.form and 'gender' in request.form and 'idtype' in request.form and 'idnumber' in request.form and 'authority' in request.form and 'issuedstate' in request.form and 'issueddate' in request.form and 'expirydate' in request.form and 'addresstype' in request.form and 'nationality' in request.form and 'state' in request.form and 'district' in request.form and 'city' in request.form and 'pincode' in request.form:
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        mobilenumber = request.form['mobilenumber']
        gender = request.form['gender']
        idtype = request.form['idtype']
        idnumber = request.form['idnumber']
        authority = request.form['authority']
        issuedstate = request.form['issuedstate']
        issueddate = request.form['issueddate']
        expirydate = request.form['expirydate']
        addresstype = request.form['addresstype']
        nationality = request.form['nationality']
        state = request.form['state']
        district = request.form['district']
        city = request.form['city']
        pincode = request.form['pincode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM registration WHERE email = %s', (email,))
        registration = cursor.fetchone()
        if registration:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Name must contain only characters and numbers!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO registration (name, dob, email, password, mobilenumber, gender, idtype, idnumber, authority, issuedstate, issueddate, expirydate, addresstype, nationality, state, district, city, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, dob, email, password, mobilenumber, gender, idtype, idnumber, authority, issuedstate, issueddate, expirydate, addresstype, nationality, state, district, city, pincode))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            
    return render_template('operatorregister.html', msg=msg)

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
        print(boarding)
        print(destination)
        
        geolocator = Nominatim(user_agent="https: my_application")
        boarding_location = geolocator.geocode(boarding)
        destination_location = geolocator.geocode(destination)

        boarding_latitude = boarding_location.latitude
        boarding_longitude = boarding_location.longitude
        destination_latitude = destination_location.latitude
        destination_longitude = destination_location.longitude
        print(boarding_latitude)
        print(boarding_longitude)
        print(destination_latitude)
        print(destination_longitude)
        sourcevalue=(boarding_latitude,boarding_longitude)
        destinationvalue=(destination_latitude,destination_longitude)
        distance = hs.haversine(sourcevalue,destinationvalue)
        print(distance)
        discount=0
        price=1000
        # create data list for table with form data
        DATA = [
            ["Date", "Name", "Source", "Destination", "Adults", "Children","Discount", "Price (Rs.)"],
            [departing, "Mayur Sampat Bhore", boarding, destination, adults,children,discount, price],
            ["Total", "", "", "", "", "", (int(price) - int(discount))],
        ]

        # create PDF object and set page size
        pdf = SimpleDocTemplate("receipt.pdf", pagesize=A4)

        # set stylesheet for text styles
        styles = getSampleStyleSheet()

        # set style for title text
        title_style = styles["Heading1"]
        title_style.alignment = 1

        # create title paragraph with appropriate text and style
        title = Paragraph("GoBus", title_style)

        # create table style with appropriate formatting
        style = TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 0), (6, 4), 1, colors.black),
                ("BACKGROUND", (0, 0), (6, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )

        # create table object with data and style
        table = Table(DATA, style=style)

        # build the PDF document with title and table
        pdf.build([title, table])
        
        # buffer = BytesIO()
        # p = canvas.Canvas(buffer)
        # p.drawString(100, 750, "Hello World")
        # p.save()
        # buffer.seek(0)

        # # Create a Message object
        # msg = Message('PDF Test', recipients=[request.form['mayur.bhore07@gmail.com']])

        # # Attach the PDF to the message
        # msg.attach("receipt.pdf", buffer.getvalue())

        # # Send the email
        # mail.send(msg)

        # Insert data into the database
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            query = "INSERT INTO booking (boarding, destination, departing, seat_type, adults, children, travel_class) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (boarding, destination, departing, seat_type, adults, children, travel_class)
            cursor.execute(query, values)
            mysql.connection.commit()
            msg = "Your booking has been saved successfully!"
            return render_template('reservation.html')
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

@app.route('/reservation')
def reservation():
    if session.get('username') is not None:
         return render_template('reservation.html')

@app.route('/operator/vehicle', methods=['GET', 'POST'])
def vehicle():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        model = request.form['model']
        chassis_number = request.form['chassis_number']
        total_capacity = request.form['total_capacity']
        economy_capacity = request.form['economy_capacity']
        elderly_capacity = request.form['elderly_capacity']
        seat_type = request.form['seat_type']
        ac_non_ac = request.form['ac_non_ac']
        sitting_sleeping = request.form['sitting_sleeping']
        remaining_seats = request.form['remaining_seats']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO vehicles (vehicle_number, model, chassis_number, total_capacity, Economy_Capacity, Elderly_Capacity, seat_type, ac_non_ac, sitting_sleeping, remaining_seats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (vehicle_number, model, chassis_number, total_capacity, economy_capacity, elderly_capacity, seat_type, ac_non_ac, sitting_sleeping, remaining_seats))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('busroute'))
    return render_template('vehicle.html')

@app.route('/operator/route_details', methods=['GET', 'POST'])
def busroute():
    msg = ''
    if request.method == 'POST' and 'source' in request.form and 'destination' in request.form and 'distance' in request.form:
        source = request.form['source']
        destination = request.form['destination']
        distance = request.form['distance']
        stop = request.form['stop']
        stop1 = request.form['stop1']
        stop2 = request.form['stop2']
        stop3 = request.form['stop3']
        stop4 = request.form['stop4']
        stop5 = request.form['stop5']
        stop6 = request.form['stop6']
        stop7 = request.form['stop7']
        stop8 = request.form['stop8']
        stop9 = request.form['stop9']
        stop10 = request.form['stop10']
        stop11 = request.form['stop11']
        stop12 = request.form['stop12']
        stop13 = request.form['stop13']
        
        distance = request.form['distance']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO bus_routes VALUES (NULL,%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (source, destination, distance , stop , stop1,stop2,stop3,stop4,stop5,stop6,stop7,stop8,stop9,stop10,stop11,stop12,stop13))
        mysql.connection.commit()
        msg = 'Success!'
        return render_template('index1.html',msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('route_details.html',msg=msg)

@app.route('/payments', methods=['GET', 'POST'])
def payments():
    msg = ''
    if request.method == 'POST' and 'customerName' in request.form and 'address' in request.form and 'amount' in request.form and 'paymentDate' in request.form:
        custname = request.form['customerName']
        add = request.form['address']
        noc = request.form['noc']
        Cno = request.form['Cno']
        CVV = request.form['CVV']
        amount = request.form['amount']
        paymentDate = request.form['paymentDate']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO payment VALUES (%s, %s, %s, %s, %s, %s, %s)', (custname, add, noc, Cno, CVV, amount, paymentDate))
        mysql.connection.commit()
        msg = 'Payment Success!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('payments.html', msg=msg)

@app.route('/receipt')
def generate_receipt():
    # Get the booking ID from the query string parameters
    booking_id = request.args.get('booking_id')
    if not booking_id:
        return 'Booking ID not specified', 400
    
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    
    # Retrieve the booking details from the database
    cur.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,))
    booking = cur.fetchone()
    if not booking:
        return 'Booking not found', 404
    
    # Parse the booking details
    num_seats = booking[1]
    seat_type = booking[2]
    distance = booking[3]
    is_frequent_traveler = bool(booking[5])  # assume column index 5 is the frequent traveler flag
    
    # Define the base fare based on the seat type and distance
    if seat_type.lower() == "economy":
        base_fare = distance * 10
    elif seat_type.lower() == "business":
        base_fare = distance * 15
    elif seat_type.lower() == "luxury":
        base_fare = distance * 20
    else:
        return 'Invalid seat type', 400
    
    # Calculate the total cost including taxes and fees
    tax_rate = 0.05
    taxes_and_fees = (base_fare * tax_rate) + 5 # assume a fixed fee of Rs. 5
    total_cost = num_seats * (base_fare + taxes_and_fees)
    
    # Calculate the dynamic pricing based on the seating capacity, but exclude frequent travelers
    if not is_frequent_traveler:
        capacity_percent = (num_seats / 100)
        if capacity_percent <= 0.5:
            dynamic_price = base_fare * 0.1
        elif capacity_percent <= 0.75:
            dynamic_price = base_fare * 0.15
        elif capacity_percent >= 0.9:
            dynamic_price = base_fare * 0.2
        else:
            dynamic_price = 0
    else:
        dynamic_price = 0
    
    # Apply any discounts or promo codes
    discount = 0
    promo_code = booking[4]
    if promo_code.lower() == "save10":
        discount = total_cost * 0.1
    elif promo_code.lower() == "save20":
        discount = total_cost * 0.2
    
    # Calculate the final cost after applying discounts and dynamic pricing
    final_cost = total_cost + dynamic_price - discount
    
    # Render the receipt HTML page with the booking and cost details
    return render_template('receipt.html', num_seats=num_seats, seat_type=seat_type, distance=distance,
                           base_fare=base_fare, dynamic_price=dynamic_price, taxes_and_fees=taxes_and_fees, 
                           total_cost=total_cost, promo_code=promo_code, discount=discount, final_cost=final_cost)



if __name__ == '__main__':
    app.run(debug=True)
