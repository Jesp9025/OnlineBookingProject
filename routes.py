from flask import Flask, render_template, flash, request, redirect, session, url_for
import Project
import functools, operator # To convert tuple to list
import EmailConfirm
from werkzeug.security import generate_password_hash
import datetime


'''Self reflection: May or may not have been easier to use flask-login and similar modules
'''


# To get methods from classes
res = Project.Resource()
user = Project.User()
booking = Project.Booking()
bookingData = Project.BookingData()
updateUserData = Project.UpdateUserData()


# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f275asdasd6352567d441f2b6176a'


@app.route("/")
def index():
    return render_template("presite.html")


@app.route("/mainpage")
def mainpage():
    return render_template("mainpage.html")


@app.route("/authors")
def authors():
    return render_template("authors.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name=request.form['Username']
        name=name.lower()
        password=request.form['password']
        
        if user.verifyLogin(name, password):
            if user.verifyUserActiveStatus(name) == False:
                flash("Error: Your account has been deactivated by an admin")
            else:
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
    if "name" in session:
        flash("Error: You are already logged in.")
        return redirect(url_for("welcome"))

    # Prevent spam registration
    try:
        time = datetime.datetime.utcnow()
        newTime = time - session['timereg']
        if newTime <= datetime.timedelta(seconds=30):
            flash("Error: You must wait before making another account!")
            return redirect(url_for("login"))
    except KeyError as e:
        print(e)

    if request.method == 'POST':
        userID = user.IDGenerator("user_id", "User")
        username=request.form['username']
        username=username.lower()
        password=request.form['password']
        email=request.form['email']
        email=email.lower()
        
        if "@gmail.com" not in email:
            flash("Error: You must use gmail!")
        else:
            try:
                temp = user.readUserAnything("SELECT user_username FROM User")
                temp = functools.reduce(operator.add, (temp))
                for item in temp:
                    print(item)
                    if username == item:
                        flash("Error: Username already taken")
                        return redirect(url_for("registration"))
                temp = user.readUserAnything("SELECT user_email FROM User")
                temp = functools.reduce(operator.add, (temp))
                for item in temp:
                    print(item)
                    if email == item:
                        flash("Error: Email already taken")
                        return redirect(url_for("registration"))

                user.createUser(userID, username, password, email, False, True)
                flash("Success: New user created")
                session['timereg'] = datetime.datetime.utcnow()
                return redirect(url_for("login"))
            except (ValueError, TypeError) as e:
                print(e)
                return redirect(url_for("registration"))
    return render_template('registration.html')

@app.route("/bugsubmit", methods=['GET', 'POST'])
def bugsubmit():
    if "name" not in session:
        return redirect(url_for("login"))

    if request.method=="POST":
        bug=request.form['bug']
        EmailConfirm.sendEmailBugSubmit(session['name'], bug)
        flash("Success: Bug has been submitted. Thank you.")
        return redirect(url_for("welcome"))

    return render_template("bugsubmit.html", username=session['name'])
@app.route("/resources")
def resources():
    if "name" not in session:
        return redirect(url_for("login"))
    booking.deleteOldBookings()
    lst = res.readResource()
    return render_template("resources.html", data=lst, username=session['name'])


@app.route("/bookings")
def bookings():
    if "name" not in session:
        return redirect(url_for("login"))
    booking.deleteOldBookings()
    lst = booking.readBooking()
    return render_template("bookings.html", data=lst, username=session['name'])


@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    if "name" not in session:
        return redirect(url_for("login"))
    try:
        booking.deleteOldBookings()
        # Prevent spam booking
        time = datetime.datetime.utcnow()
        newTime = time - session['time']
        if newTime <= datetime.timedelta(seconds=30):
            flash("Error: You must wait before making another reservation!")
            return redirect(url_for("welcome"))

        if request.method == 'POST':
            resourceID=request.form['ID']
            quantity=request.form['quantity']
            bookingID = user.IDGenerator("booking_id", "Booking")
            #date=request.form['date']

            try:
                quantity = int(quantity)
            except (TypeError, ValueError) as e:
                print(e)

            if booking.createBooking(quantity, resourceID, bookingID): # If resources are not available
                flash("Error: You can't reserve that many")
                return redirect(url_for("reservation"))
            
            session['time'] = datetime.datetime.utcnow()
            EmailConfirm.sendEmailConfirm(user.readUserEmail(session['name']), bookingID) # Sends an email to users email address
            booking.setUsernameBooking(session['name'], bookingID)
            booking.setQuantityBooking(quantity, bookingID)
            booking.setResourceIDinBooking(resourceID, bookingID)
            bookingData.createBookingData(bookingID, session['name'], resourceID, quantity)
            flash("Success: Booking confirmed. An email has been sent to registered email address.")
            return redirect(url_for("welcome"))
        lst = res.readResource()
    except TypeError as e:
        flash("Error: Something is not right. Did you input a resource ID that doesn't exist?")
        print(e.args[0])
        lst = res.readResource()
    return render_template("reservation.html", data=lst, username=session['name'])


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/confirm")
def confirm():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("confirm.html", username=session['name'])


@app.route("/welcome")
def welcome():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("welcome.html", username=session['name'])


@app.route("/denied")
def denied():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("denied.html", username=session['name'])


@app.route("/deleteresource", methods=['GET', 'POST'])
def deleteresource():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))
    try:
        if request.method == 'POST':
                resourceID=request.form['ID']
                if res.deleteResource("resource_ID", resourceID): # If resource id exists in database
                    flash("Success: Resource has been deleted")
                    return redirect(url_for("deleteresource"))
                else: # If resource doesnt exist in database
                    flash("Error: You can't delete that")

        booking.deleteOldBookings()
        lst = res.readResource()
    except TypeError as e:
        flash("Error: You can't delete that")
        print(e.args[0])

    return render_template("deleteresource.html", data=lst, username=session['name'])


@app.route("/deletebooking", methods=['GET', 'POST'])
def deletebooking():
    if "name" not in session:
        return redirect(url_for("login"))

    booking.deleteOldBookings()

    try:
        if request.method == 'POST':
            bookingID=request.form['ID']
            if user.checkIfAdmin(session['name']) == True:
                booking.deleteBooking("booking_id", bookingID)
            else:
                booking.deleteOwnBooking("booking_id", bookingID, session['name'])
            flash("Success: Booking has been deleted")
            return redirect(url_for("deletebooking"))
            
        if user.checkIfAdmin(session['name']) == False:
            lst = booking.readSpecificBooking("booking_user_username", session['name'])
        else:
            lst = booking.readBooking()
    except TypeError as e:
        flash("Error: You can't delete that")
        print(e.args[0])
        lst = booking.readBooking()
    
    return render_template("deletebooking.html", data=lst, username=session['name'])


@app.route("/updateuser")
def updateuser():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    return render_template("updateuser.html", username=session['name'])


@app.route("/updateusername", methods=['GET', 'POST'])
def updateusername():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            currentUsername=request.form['Username']
            currentUsername=currentUsername.lower()
            newUsername=request.form['Username2']
            newUsername=newUsername.lower()

            # Check if current username & new username exists in database
            if user.checkUserExist(currentUsername):
                if user.checkUserExist(newUsername) == False:
                    user.updateUserAnything("UPDATE User SET user_username = '{}' WHERE user_username = '{}'".format(newUsername, currentUsername))
                    updateUserData.createUpdateUserData(session['name'], currentUsername, "Changed username to {}".format(newUsername))
                    flash("Success: Username has been updated")
                    if currentUsername == session['name']:
                        session['name'] = newUsername
                    return redirect(url_for("updateuser"))
                else:
                    flash("Error: New username already exists in database")
            else:
                flash("Error: Couldn't find current username in database")
    except (TypeError, ValueError) as e:
        return e

    return render_template("updateusername.html", data=lst, username=session['name'])


@app.route("/updatepassword", methods=['GET', 'POST'])
def updatepassword():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            username=request.form['Username']
            username=username.lower()
            password=request.form['password']
            password2=request.form['password2']

            if user.checkUserExist(username):
                if password == password2:
                    newPassword = generate_password_hash(password)
                    user.updateUserAnything("UPDATE User SET user_password = '{}' WHERE user_username = '{}'".format(newPassword, username))
                    updateUserData.createUpdateUserData(session['name'], username, "Changed password")
                    flash("Success: User password has been updated")
                    return redirect(url_for("updateuser"))
                else:
                    flash("Error: Passwords didn't match")
            else:
                flash("Error: Couldn't find username in database")
    except (TypeError, ValueError) as e:
        return e
    return render_template("updatepassword.html", data=lst, username=session['name'])


@app.route("/updateemail", methods=['GET', 'POST'])
def updateemail():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            username=request.form['Username']
            username=username.lower()
            email=request.form['email']
            email=email.lower()

            if user.checkUserExist(username):
                user.updateUserAnything("UPDATE User SET user_email = '{}' WHERE user_username = '{}'".format(email, username))
                updateUserData.createUpdateUserData(session['name'], username, "Changed email to {}".format(email))
                flash("Success: User Email has been updated")
                return redirect(url_for("updateuser"))
            else:
                flash("Error: Couldn't find username in database")
    except (TypeError, ValueError) as e:
        return e
    return render_template("updateemail.html", data=lst, username=session['name'])


@app.route("/updateadminstatus", methods=['GET', 'POST'])
def updateadminstatus():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUserAnything("SELECT user_username, user_is_admin FROM User;")
    try:
        if request.method == 'POST':
            username=request.form['Username']
            username=username.lower()
            admin=request.form['status']

            if user.checkUserExist(username):
                user.updateUserAnything("UPDATE User SET user_is_admin = '{}' WHERE user_username = '{}'".format(admin, username))
                updateUserData.createUpdateUserData(session['name'], username, "Changed Admin Status to {}".format(admin))
                flash("Success: User Admin Status has been updated")
                return redirect(url_for("updateuser"))
            else:
                flash("Error: Couldn't find username in database")
    except (TypeError, ValueError) as e:
        return e
    return render_template("updateadminstatus.html", data=lst, username=session['name'])


@app.route("/deleteuser", methods=['GET', 'POST'])
def deleteuser():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUsername()
    try:
        if request.method == 'POST':
            username=request.form['Username']
            username=username.lower()
            if username == session['name']:
                flash("Error: You can't delete your own user")
                return redirect(url_for("deleteuser"))
            if user.checkUserExist(username):
                user.updateUserAnything("DELETE FROM User WHERE user_username = '{}'".format(username))
                updateUserData.createUpdateUserData(session['name'], username, "Deleted user")
                booking.deleteBooking("booking_user_username", username) # Delete bookings that the user may have   
                flash("Success: User has been deleted")
                return redirect(url_for("updateuser"))
            else:
                flash("Error: Couldn't find username in database")
    except (TypeError, ValueError) as e:
        return e
    return render_template("deleteuser.html", data=lst, username=session['name'])

@app.route("/updateuseractivestatus", methods=['GET', 'POST'])
def updateuseractivestatus():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))

    lst = user.readUserAnything("SELECT user_username, user_account_is_active FROM User;")
    try:
        if request.method == 'POST':
            username=request.form['Username']
            username=username.lower()
            active=request.form['status']

            if user.checkUserExist(username):
                user.updateUserAnything("UPDATE User SET user_account_is_active = '{}' WHERE user_username = '{}'".format(active, username))
                updateUserData.createUpdateUserData(session['name'], username, "Changed Active Status to {}".format(active))
                flash("Success: User Active Status has been updated")
                return redirect(url_for("updateuser"))
            else:
                flash(" Error: Couldn't find username in database")
    except (TypeError, ValueError) as e:
        return e
    return render_template("updateuseractivestatus.html", data=lst, username=session['name'])

@app.route("/logs")
def logs():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))
    return render_template("logs.html", username=session['name'])

@app.route("/userdatalog")
def userdatalog():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))
    lst = updateUserData.readUserDataLog()
    return render_template("userdatalog.html", data=lst, username=session['name'])

@app.route("/bookingdatalog")
def bookingdatalog():
    if "name" not in session:
        return redirect(url_for("login"))
    if user.checkIfAdmin(session['name']) == False:
        return redirect(url_for("denied"))
    lst = bookingData.readBookingData()
    return render_template("bookingdatalog.html", data=lst, username=session['name'])

if __name__ == "__main__":
    app.run()