from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import yaml

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = '92b1e1bfefb207d960945555065173bf'
bcrypt = Bcrypt()

# Config DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Request Data from HTML file from
        userDetails = request.form
        userid = userDetails['userid']
        emailid = userDetails['emailid']
        password = userDetails['password']
        confirmpassword = userDetails['confirmpassword']

        if password == confirmpassword:
            # Create cursor to connect to database and execute CRUD (insert, update and delete) operations
            password = bcrypt.generate_password_hash(password).decode('UTF-8')
            
            cur.execute('INSERT into customers(userid, emailid, password) values(%s, %s, %s)', (userid, emailid, password))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
        else:
            print('Error')
    return render_template('register.html')
            

@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        userDetails = request.form
        userid = userDetails['userid']
        password = userDetails['password']
        cur.execute("SELECT * FROM `customers` WHERE userid='%s'" % userid)
        data = cur.fetchone()
        cur.close()
        if data:
            print(bcrypt.check_password_hash(data[3], password))
            if bcrypt.check_password_hash(data[3], password):
                session['usedid'] = data[1]
                return redirect(url_for('customer'))
            else:
                return '<b>Incorrect Password</b>'
        elif data == None:
            return '<b>No User ID Found!</b>'
    else:
        return render_template('login.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

if __name__ == '__main__':
    app.run(debug=True)
