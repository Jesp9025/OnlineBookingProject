from flask import Flask, render_template, flash, request, redirect, session, url_for
import Project
import os
import functools, operator # To convert tuple to list
import EmailConfirm
from werkzeug.security import generate_password_hash

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
def index():
    return redirect(url_for("mainpage"))


@app.route("/mainpage")
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
            user.createUser(userID, username, password, email, False, True)
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


@app.route("/updateuser")
def updateuser():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    return render_template("updateuser.html")


@app.route("/updateusername", methods=['GET', 'POST'])
def updateusername():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            currentUsername=request.form['name']
            newUsername=request.form['name2']
            if currentUsername == "" or newUsername == "":
                flash("Error: Fill out the forms")
            else:
                user.updateUserAnything("UPDATE User SET user_username = '{}' WHERE user_username = '{}'".format(newUsername, currentUsername))
                flash("Success: Username has been updated")
                return redirect(url_for("welcome"))
    except (TypeError, ValueError) as e:
        return e

    return render_template("updateusername.html", data=lst)


@app.route("/updatepassword", methods=['GET', 'POST'])
def updatepassword():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            username=request.form['name']
            password=request.form['password']
            password2=request.form['password2']

            if password == password2:
                if username == "" or password == "" or password2 == "":
                    flash("Error: Fill out the forms")
                else:
                    newPassword = generate_password_hash(password)
                    user.updateUserAnything("UPDATE User SET user_password = '{}' WHERE user_username = '{}'".format(newPassword, username))
                    flash("Success: User password has been updated")
                    return redirect(url_for("welcome"))
            else:
                flash("Error: Passwords didn't match")
    except (TypeError, ValueError) as e:
        return e
    return render_template("updatepassword.html", data=lst)


@app.route("/updateemail", methods=['GET', 'POST'])
def updateemail():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            username=request.form['name']
            email=request.form['email']
            if username == "" or email == "":
                flash("Error: Fill out the forms")
            else:
                user.updateUserAnything("UPDATE User SET user_email = '{}' WHERE user_username = '{}'".format(email, username))
                flash("Success: User Email has been updated")
                return redirect(url_for("welcome"))
    except (TypeError, ValueError) as e:
        return e
    return render_template("updateemail.html", data=lst)


@app.route("/updateadminstatus", methods=['GET', 'POST'])
def updateadminstatus():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            username=request.form['name']
            admin=request.form['status']
            if username == "":
                flash("Error: Enter a username")
            else:
                user.updateUserAnything("UPDATE User SET user_is_admin = '{}' WHERE user_username = '{}'".format(admin, username))
                flash("Success: User Admin Status has been updated")
                return redirect(url_for("welcome"))
    except (TypeError, ValueError) as e:
        return e
    return render_template("updateadminstatus.html", data=lst)


@app.route("/deleteuser", methods=['GET', 'POST'])
def deleteuser():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            username=request.form['name']
            if username == "":
                flash("Error: Enter a username")
            else:
                user.updateUserAnything("DELETE FROM User WHERE user_username = '{}'".format(username))
                flash("Success: User has been deleted")
                return redirect(url_for("welcome"))
    except (TypeError, ValueError) as e:
        return e
    return render_template("deleteuser.html", data=lst)
if __name__ == "__main__":
    app.run()