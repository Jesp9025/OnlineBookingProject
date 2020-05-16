from flask import Flask, render_template, flash, request, redirect, session, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import Project
import os
import functools, operator # To convert tuple to list

# To get methods from classes
res = Project.Resource()
user = Project.User()

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f275asdasd6352567d441f2b6176a'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Jesper/Desktop/New/databaseProject.db' # Define where database is located
#db = SQLAlchemy(app) # Initialize SQLAlchemy

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
            
        if user.verifyLogin(name, password):
            session['name'] = name
            return redirect(url_for("welcome"))
        else:
            flash('Error: Wrong username or password')
    if "name" in session:
        return redirect(url_for("welcome"))
    else:
        return render_template('index.html')

@app.route("/logout")
def logout():
    if "name" not in session:
        return redirect(url_for("login"))
    session.pop("name", None)
    return redirect(url_for("login"))

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        userID=request.form['ID']
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        user.createUser(userID, username, password, email, True, True)

        print(userID, password)
        return redirect(url_for("login"))  
    return render_template('registration.html')

@app.route("/resources")
def resources():
    '''This will print out a table
    '''
    if "name" not in session:
        return redirect(url_for("login"))
    lst = res.readResource("Resource")
    data = lst
    return render_template("resources.html", data=data)

@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    if "name" not in session:
        return redirect(url_for("login"))
    
    if request.method == 'POST':
        resourceID=request.form['ID']
        quantity=request.form['quantity']
        try:
            quantity = int(quantity)
        except TypeError as e:
            print(e)

        temp = res.readSpecific("SELECT resource_quantity FROM Resource WHERE resource_id = {}".format(resourceID))
        toList = functools.reduce(operator.add, (temp))
        for item in toList:
            if quantity > item:
                print("No can do..")
                return redirect(url_for("reservation"))
            elif quantity <= 0:
                print("No can do again")
                return redirect(url_for("reservation"))
            else:
                newValue = item - quantity
                res.updateResource("Resource", "resource_quantity", newValue, "resource_id", resourceID)
        return redirect(url_for("confirm"))

    return render_template("reservation.html")

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


if __name__ == "__main__":
    app.run()