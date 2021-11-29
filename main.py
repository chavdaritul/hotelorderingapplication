from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import yaml

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '92b1e1bfefb207d960945555065173bf'
bcrypt = Bcrypt()

# Config DB
db = yaml.safe_load(open('db.yaml'))
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
    return render_template('menu.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Request Data from HTML file from
        userDetails = request.form
        userid = userDetails['name']
        emailid = userDetails['emailid']
        password = userDetails['password']
        confirmpassword = userDetails['confirmpassword']

        SpecialSym = ['$', '@', '#', '%']

        cur.execute("SELECT * FROM `customers` WHERE emailid='%s'" % emailid)
        data = cur.fetchone()
        if data:
            flash('Email Id already Exist.')
            return render_template('register.html')

        if len(password) >= 8:
            return render_template('register.html')

        if not any(char.isdigit() for char in password):
            return render_template('register.html')

        if not any(char.isupper() for char in password):
            return render_template('register.html')

        if not any(char.islower() for char in password):
            return render_template('register.html')

        if not any(char in SpecialSym for char in password):
            return render_template('register.html')

        if password == confirmpassword:
            # Create cursor to connect to database and execute CRUD (insert, update and delete) operations
            password = bcrypt.generate_password_hash(password).decode('UTF-8')

            cur.execute('INSERT into customers(userid, emailid, password) values(%s, %s, %s)',
                        (userid, emailid, password))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('menu'))
        else:
            return render_template('register.html')

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    print('\n')
    if request.method == 'POST':
        userDetails = request.form
        emailId = userDetails['emailId']
        password = userDetails['password']
        cur.execute("SELECT * FROM `customers` WHERE emailid='%s'" % emailId)
        data = cur.fetchone()
        cur.close()
        if data:
            print(data)
            print(bcrypt.check_password_hash(data[3], password))
            if bcrypt.check_password_hash(data[3], password):
                session['userid'] = data[1]
                return redirect(url_for('menu'))
            else:
                flash("Incorrect Password")
                return render_template('login.html')
        elif data is None:
            flash("Email ID not Found!")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if session.get('userid') is None:
        return redirect(url_for('login'))
    else:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            # Request Data from HTML file from
            userDetails = request.form
            userid = session['userid']
            emailid = userDetails['emailid']
            address = userDetails['address']
            phone = userDetails['phone']
            cur.execute('UPDATE customers SET emailid = %s , address = %s , phone = %s where userid == %s',
                        (emailid, address, phone, userid))
            mysql.connection.commit()
            cur.close()
        print(session['userid'])
        user = session['userid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `customers` WHERE userid='%s'" % user)
        data = cur.fetchall()
        return render_template('customer.html', data=data)


@app.route("/logout")
def logout():
    session.pop('userid', None)
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
