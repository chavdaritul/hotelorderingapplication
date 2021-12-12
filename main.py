from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import yaml
from tkinter import *
from tkinter import messagebox
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = '92b1e1bfefb207d960945555065173bf'
bcrypt = Bcrypt()
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Config DB
db = yaml.safe_load(open('db.yaml'))
# db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    try:
        title = 'Menu'
        cur = mysql.connection.cursor()
        cur.execute('Select * from menu')
        rows = cur.fetchall()
        return render_template('menu.html', products = rows, title=title)
    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Request Data from HTML file from
        userDetails = request.form
        name = userDetails['name']
        emailid = userDetails['emailid']
        password = userDetails['password']
        confirmpassword = userDetails['confirmpassword']

        SpecialSym =['$', '@', '#', '%']
        val = True

        cur.execute("SELECT * FROM `customers` WHERE emailid='%s'" % emailid)
        data = cur.fetchone()
        if data:
            flash('Email Id already Exist.')
            return render_template('register.html')

        for i in name.split(' '):
            if i.isalpha() == False:
                flash('Name should be alphabets only.')
                return render_template('register.html')

        if len(password) < 8:
            flash('Password too Short.')
            return render_template('register.html')

        if not any(char.isdigit() for char in password):
            flash('Must contain Digit.')
            return render_template('register.html')

        if not any(char.isupper() for char in password):
            flash('Must contain Upper Case.')
            return render_template('register.html')

        if not any(char.islower() for char in password):
            flash('Must contain Lower Case.')
            return render_template('register.html')

        if not any(char in SpecialSym for char in password):
            flash('Must contain Special Character.')
            return render_template('register.html')

        if password == confirmpassword:
            # Create cursor to connect to database and execute CRUD (insert, update and delete) operations
            password = bcrypt.generate_password_hash(password).decode('UTF-8')

            cur.execute('INSERT into customers(name, emailid, password) values(%s, %s, %s)',
                        (name, emailid, password))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')

    return render_template('register.html')
            

@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    print('\n')
    if request.method == 'POST':
        userDetails = request.form
        emailid = userDetails['emailid']
        password = userDetails['password']
        cur.execute("SELECT `id`, `emailid`, `password` FROM `customers` WHERE emailid='%s'" % emailid)
        data = cur.fetchone()
        cur.close()
        if data:
            if bcrypt.check_password_hash(data[2], password):
                session['id'] = data[0]
                if data[0] == 1:
                    return redirect(url_for('admin'))
                else: 
                    return redirect(url_for('customer'))
            else:
                flash("Incorrect Password")
                return render_template('login.html')
        elif data == None:
            flash('No Data Found!')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if session.get('id') == None:
        return redirect(url_for('login'))
    else:
        title = 'Customer'
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            # Request Data from HTML file from
            userDetails = request.form
            id = session['id']
            address = userDetails['address']
            phone = userDetails['phone']
            dob = datetime.datetime.strptime(userDetails['dob'],'%Y-%m-%d')
            cur.execute("SELECT * FROM `customers` WHERE id='%s'" % id)
            temp = cur.fetchall()
            directory = str(temp[0][0])
            path = os.path.join(app.config['UPLOAD_FOLDER'], directory)
            if temp[0][7] == 'Verified' or temp[0][7] == 'Not-Verified':
                pass
            else:
                if os.path.isdir(path) != True:
                    os.mkdir(path)
                for x in os.listdir(path):
                    x = path + '/' + x
                    os.unlink(x)
                if 'document_kyc' not in request.files:
                    print('################# No File Part #################')
                file = request.files['document_kyc']
                if file.filename == '':
                    print('################# No File Selected #################')
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    src = os.path.join(app.config['UPLOAD_FOLDER']+str(temp[0][0])+'/', filename)
                    file.save(src)
                    dest = os.path.join(app.config['UPLOAD_FOLDER']+str(temp[0][0])+'/', str(temp[0][0])+'.jpg')
                    os.rename(src, dest)
                    cur.execute("UPDATE customers SET document_verified=%s where id=%s", ('Not-Verified', id))
            cur.execute("UPDATE customers SET address=%s,phone=%s, dob=%s where id=%s", (address, phone, dob, id))
            mysql.connection.commit()
            cur.close()
        id = session['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `customers` WHERE id='%s'" % id)
        data = cur.fetchall()
        return render_template('customer.html', data=data, title=title)

@app.route('/admin')
def admin():
    if session.get('id') == None:
        return redirect(url_for('login'))
    else: 
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `customers` WHERE id='%s'" % id)
        data = cur.fetchall()
        return render_template('admin.html', data=data)

@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if session.get('id') == None:
        return redirect(url_for('login'))
    else: 
        title = 'User Data'
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `customers`")
        data = cur.fetchall()
        return render_template('userdata.html', data=data, title=title)

@app.route("/documentcheck/<emailid>", methods=['GET', 'POST'])
def documentcheck(emailid):
    title = 'User Data'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `customers` WHERE emailid='%s'" % emailid)
    data = cur.fetchall()
    print(data)
    return render_template('documentcheck.html', emailid=emailid, title=title, data=data)

@app.route("/documentstatus/<emailid>/<status>", methods=['GET', 'POST'])
def documentstatus(emailid, status):
    title = 'User Data'
    cur = mysql.connection.cursor()
    cur.execute("UPDATE customers SET document_verified=%s where emailid=%s", (status, emailid))
    mysql.connection.commit()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `customers` WHERE emailid='%s'" % emailid)
    data = cur.fetchall()
    print(data)
    return render_template('documentcheck.html', title=title, emailid=emailid, data=data)

@app.route("/logout")
def logout():
    session.pop('id', None)
    session.clear()
    return redirect(url_for('home'))   

if __name__ == '__main__':
    app.run(debug=True)
