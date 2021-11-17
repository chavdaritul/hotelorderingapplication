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
        userid = userDetails['userid']
        emailid = userDetails['emailid']
        password = userDetails['password']
        confirmpassword = userDetails['confirmpassword']

        SpecialSym =['$', '@', '#', '%']
        val = True

        cur.execute("SELECT * FROM `customers` WHERE userid='%s'" % userid)
        data = cur.fetchone()
        print('\n')
        if data:
            print('Username already Exist.')
            val = False

        if len(password) < 6:
            print('Length should be atleast 6.')
            val = False
            
        if len(password) > 20:
            print('Length should not be grater than 8.')
            val = False
            
        if not any(char.isdigit() for char in password):
            print('Atleast one numeric.')
            val = False
            
        if not any(char.isupper() for char in password):
            print('Atleast one uppercase.')
            val = False
            
        if not any(char.islower() for char in password):
            print('Atleast one lowercase.')
            val = False
            
        if not any(char in SpecialSym for char in password):
            print('Sould contain one of these symbol : $@#%.')
            val = False
        if val:
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
    print('\n')
    if request.method == 'POST':
        userDetails = request.form
        userid = userDetails['userid']
        password = userDetails['password']
        cur.execute("SELECT * FROM `customers` WHERE userid='%s'" % userid)
        data = cur.fetchone()
        cur.close()
        if data:
            if bcrypt.check_password_hash(data[5], password):
                session['userid'] = data[1]
                return redirect(url_for('customer'))
            else:
                return '<b>Incorrect Password</b>'
        elif data == None:
            return '<b>No User ID Found!</b>'
    else:
        return render_template('login.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if session.get('userid') == None:
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
            cur.execute('UPDATE customers SET emailid = %s , address = %s , phone = %s where userid == %s', (emailid, address, phone, userid))
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
