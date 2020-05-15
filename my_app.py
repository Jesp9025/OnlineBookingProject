from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import Project
import os

# Test if we can read from database
res = Project.resource()
#lst = res.readResource('Resource')
#for row in lst:
#    print(row)
#print(res.readResource("Resource"))

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Jesper/Desktop/New/databaseProject.db' # Define where database is located
db = SQLAlchemy(app) # Initialize SQLAlchemy

## A TEST FOR SQLAlchemy ##
class Test(db.Model):
    lalalaid = db.Column(db.Integer, primary_key=True)
## ##

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST':
            name=request.form['name']
            password=request.form['password']
            email=request.form['email']
            print(name, " ", email, " ", password)

        if form.validate():
        # Save the comment here.
            print(res.createResource(2, name, "DX850", "d231213sddsa")) # For  testing purposes
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')

        return render_template('index.html', form=form)
    @app.route("/about")
    def getTable():
        '''This will print out a table
        '''
        lst = res.readResource("Resource")
        data = lst
        return render_template("about.html", data=data)

if __name__ == "__main__":
    app.run()