from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import exc


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/lowes2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Creating model table for our CRUD database
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(10))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

# This engine just used to query for list of databases
mysql_engine = create_engine('mysql://root:''@localhost:3306')

# Query for existing databases
mysql_engine.execute("CREATE DATABASE IF NOT EXISTS lowes2 ")

#Get all our user data
@app.route('/')
def Index():
    try:
        all_data = User.query.all()
    except exc.SQLAlchemyError:
        db.create_all()
        all_data = User.query.all()
    return render_template("index.html", records = all_data)

# insert data to mysql db via FE
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        my_data = User(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        flash("User Inserted Successfully")
        return redirect(url_for('Index'))


#edit/update user
@app.route('/update', methods = ['POST'])
def update():

    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        db.session.commit()
        flash("User Updated Successfully")
        return redirect(url_for('Index'))


#This route is for deleting our User
@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Deleted Successfully")
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)