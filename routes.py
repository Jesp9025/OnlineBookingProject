from flask import Flask, render_template, flash, request, redirect, session, url_for
import Project
import os
import functools, operator # To convert tuple to list
import EmailConfirm

# To get methods from classes
res = Project.Resource()
user = Project.User()
booking = Project.Booking()

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f275asdasd6352567d441f2b6176a'

@app.route("/")
def mainpage():
    return render_template("mainpage.html")

@app.route("/authors")
def authors():
    return render_template("authors.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name=request.form['name']
        name=name.lower()
        password=request.form['password']
        
        if user.verifyLogin(name, password):
            session['name'] = name
            return redirect(url_for("welcome"))
        else:
            flash('Error: Wrong username or password')
    if "name" in session:
        return redirect(url_for("welcome"))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    if "name" not in session:
        return redirect(url_for("login"))
    session.pop("name", None)
    return redirect(url_for("login"))

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        userID = user.IDGenerator("user_id", "User")
        username=request.form['username']
        username=username.lower()
        password=request.form['password']
        email=request.form['email']
        email=email.lower()
        if email == "" or username == "" or password == "":
            flash("Error: You must fill out every form")
        else:
            user.createUser(userID, username, password, email, True, True)
            print(userID, username, password, email)
            return redirect(url_for("login"))
    return render_template('registration.html')

@app.route("/resources")
def resources():
    if "name" not in session:
        return redirect(url_for("login"))
    booking.deleteOldBookings()
    lst = res.readResource()
    print(lst)
    #print(user.checkIfAdmin(session['name'])) # Test to see if user in session is admin
    return render_template("resources.html", data=lst)

@app.route("/bookings")
def bookings():
    if "name" not in session:
        return redirect(url_for("login"))
    booking.deleteOldBookings()
    lst = booking.readBooking()
    return render_template("bookings.html", data=lst)

@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    if "name" not in session:
        return redirect(url_for("login"))
    
    if request.method == 'POST':
        resourceID=request.form['ID']
        quantity=request.form['quantity']
        bookingID = user.IDGenerator("booking_id", "Booking")
        print(bookingID)
        
        try:
            quantity = int(quantity)
        except (TypeError, ValueError) as e:
            print(e)
        print(quantity)
        if booking.createBooking(quantity, resourceID, bookingID): # If resources are not available
            return redirect(url_for("reservation"))
        EmailConfirm.sendEmail(user.readUserEmail(session['name'])) # Sends an email to users email address
        booking.setUsernameBooking(session['name'], bookingID)
        booking.setQuantityBooking(quantity, bookingID)
        booking.setResourceIDinBooking(resourceID, bookingID)
        return redirect(url_for("confirm"))
    lst = res.readResource()
    return render_template("reservation.html", data=lst)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/confirm")
def confirm():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("confirm.html")
    
@app.route("/welcome")
def welcome():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("welcome.html")

@app.route("/denied")
def denied():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("denied.html")

@app.route("/deleteresource", methods=['GET', 'POST'])
def deleteresource():
    if "name" not in session:
        return redirect(url_for("login"))

    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    if request.method == 'POST':
            resourceID=request.form['ID']
            res.deleteResource("resource_ID", resourceID)


    booking.deleteOldBookings()
    lst = res.readResource()
    print(lst)
    #print(user.checkIfAdmin(session['name'])) # Test to see if user in session is admin
    return render_template("deleteresource.html", data=lst)

@app.route("/deletebooking", methods=['GET', 'POST'])
def deletebooking():
    if "name" not in session:
        return redirect(url_for("login"))

    try:
        if request.method == 'POST':
            bookingID=request.form['ID']
            if user.checkIfAdmin(session['name']) == True:
                booking.deleteBooking("booking_id", bookingID)
            else:
                booking.deleteOwnBooking("booking_id", bookingID, session['name'])

        if user.checkIfAdmin(session['name']) == False:
            booking.deleteOldBookings()
            lst = booking.readSpecificBooking("booking_user_username", session['name'])
        else:
            booking.deleteOldBookings()
            lst = booking.readBooking()
            
        return render_template("deletebooking.html", data=lst)
    except TypeError as e:
        print(e)
        return render_template("deletebooking.html")

if __name__ == "__main__":
    app.run()