from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import yaml
from werkzeug.utils import secure_filename
import os
import datetime
from flask_mail import Message
import smtplib, ssl, secrets, string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

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

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/menu')
def menu():
    try:
        title = 'Menu'
        cur = mysql.connection.cursor()
        cur.execute('Select `pid`, `name`, `image`, `category`, `price`, `description` from menu ORDER BY category')
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
            cur.execute("SELECT id FROM `customers` WHERE emailid='%s'" % emailid)
            data = cur.fetchone()
            if data:
                session['id'] = data[0]
            cur.close()
            return render_template('login.html')
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
                session['emailid'] = data[1]
                if data[0] == 1:
                    return redirect(url_for('admin'))
                else: 
                    return redirect(url_for('menu', id=session['id']))
            else:
                flash("Incorrect Password")
                return render_template('login.html')
        elif data == None:
            flash('No Data Found!')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    cur = mysql.connection.cursor()
    sta = None
    if request.method == 'POST':
        userDetails = request.form
        emailid = userDetails['emailid']
        cur.execute("SELECT `emailid` FROM `customers` WHERE emailid='%s'" % emailid)
        data = cur.fetchone()
        print(data)
        if data != None:
            smtp_server = "smtp.gmail.com"
            port = 587  # For starttls
            sender_email = "hotelorderingapplication@gmail.com"
            receiver_email = emailid
            password = 'HotelOrderingApplication@112233'

            new_user_pass = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
            password_enc = bcrypt.generate_password_hash(new_user_pass).decode('UTF-8')

            cur.execute("UPDATE customers SET password=%s where emailid=%s", (password_enc, emailid))
            mysql.connection.commit()
            cur.close()

            message = MIMEMultipart("alternative")
            message["Subject"] = "Change Password Request"
            message["From"] = 'Hotel Ordering Application <hotelorderingapplication@gmail.com>' #str(Header('Elearn <supelearn@gmail.com>'))
            message["To"] = receiver_email

    ###############################################
            text = """\
            Hello,

            We have sent you this email in response to your request to reset your password on your Elearn account.
            This is your new password: """+new_user_pass+"""

            Please change your password to more secure credentials once you are logged in.

            Please ignore this email if you did not request a password change."""

            html = '''\
            <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
                <head>
                    <style>
                        *{
                            font-size: 1.2rem;
                            font-family: Bebas Neue;
                        }
                        table{
                            text-align: center;
                        }
                        .logo{
                            width: 30%;
                        }
                        .td-otp{
                            text-align: right;
                            width: 30%;
                        }
                        .td-password, p{
                            font-family: Raleway;
                            font-size: 1rem;
                        }
                        .table-border-div{
                            border: 2px solid #ffd000;
                            width: 30%;
                            padding: 1%;
                            border-radius: 30px;
                            margin-left: auto;
                            margin-right: auto;
                        }
                    </style>
                </head>
                <body>
                    <div class='table-border-div'>
                        <table>
                            <tr>
                                <th colspan="2">
                                    <img src="cid:image1" class='logo'>
                                </th>
                            </tr>
                            <tr><th colspan="2">&nbsp;</th></tr>
                            <tr>
                                <td colspan="2">
                                    <p>
                                        Here is your new password to login. Change it immediately after login for security purpose. And dont share this OTP with anyone.
                                    </p>
                                </td>
                            </tr>
                            <tr><th colspan="2">&nbsp;</th></tr>
                            <tr>
                                <td class='td-otp'>
                                    Password : 
                                </td>
                                <td class='td-password'>
                                    '''+new_user_pass+'''
                                </td>
                            </tr>
                            <tr>
                                <td class="td-otp">
                                    Contact Us: 
                                </td>
                                <td class='td-password'>
                                    hotelorderingapplication@gmail.com
                                </td>
                            </tr>
                        </table>
                    </div>
                </body>
            </html>
            '''
    ###############################################

            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            fp = open('static/images/logo.png', 'rb')
            image = MIMEImage(fp.read())
            fp.close()

            image.add_header('Content-ID', '<image1>')
            message.attach(image)
            context = ssl.create_default_context()

            server = smtplib.SMTP(smtp_server, port)
            server.starttls(context=context) # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            flash('Password Send on E-Mail!')
            sta = True
            return render_template('forgotpassword.html', status=sta)
        else:
            sta = False
            flash('No Email ID Found!')
    return render_template('forgotpassword.html', status=sta)


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
            if userDetails['dob'] != '':
                dob = datetime.datetime.strptime(userDetails['dob'],'%Y-%m-%d')
            else:
                dob = ''
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

@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    if session.get('id') == None:
        return redirect(url_for('login'))
    else:
        title = 'Change Password'
        sts = None
        if request.method == 'POST':
            userDetails = request.form
            id = session.get('id')
            oldp = userDetails['oldpassword']
            newp = userDetails['newpassword']
            cnewp = userDetails['cnewpassword']
            cur = mysql.connection.cursor()
            cur.execute("SELECT password FROM `customers` WHERE id='%s'" % id)
            db_oldp = cur.fetchall()
            if bcrypt.check_password_hash(db_oldp[0][0], oldp):
                if newp == cnewp:
                    newp = bcrypt.generate_password_hash(newp).decode('UTF-8')
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE customers SET password=%s where id=%s", (newp, id))
                    mysql.connection.commit()
                    cur.close()
                    sts = True
                    flash("Password Changed")
                    return render_template('changepassword.html', id=session['id'], title=title, status=sts)
                else:
                    sts = False
                    flash("Password does not match!")
                    return render_template('changepassword.html', id=session['id'], title=title, status=sts)
            else:
                sts = False
                flash("Old Password did not match!")
                return render_template('changepassword.html', id=session['id'], title=title, status=sts)
        return render_template('changepassword.html', id=session['id'], title=title, status=sts)


@app.route('/payment')
def payment():
    if session.get('id') == None:
        return redirect(url_for('login'))
    else:
        title = 'Payment'
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, emailid, balance FROM `customers` WHERE id='%s'" % session.get('id'))
        data = cur.fetchall()
        cur.execute("SELECT id, emailid FROM `bank_details` WHERE emailid='%s'" % session.get('emailid'))
        checkbankbal = cur.fetchall()
        print(checkbankbal)
        cur.execute("SELECT id, emailid FROM `card_details` WHERE emailid='%s'" % session.get('emailid'))
        checkcardbal = cur.fetchall()
        print(checkcardbal)
        return render_template('payment.html', title=title, data=data, checkbankbal=checkbankbal, checkcardbal=checkcardbal)


@app.route('/paymentoption')
def paymentoption():
    if session.get('id') == None:
        return redirect(url_for('login'))
    else:
        title = 'Payment'
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, emailid, balance FROM `customers` WHERE id='%s'" % session.get('id'))
        data = cur.fetchall()
        return render_template('paymentoption.html', title=title, data=data)


@app.route('/addmoney/<addmoney>', methods = ['GET', 'POST'])
def addmoney(addmoney):
    if session.get('id') == None:
        return redirect(url_for('login'))
    else:
        title = 'Payment'
        if addmoney == 'Saving Account':
            addmoney = 'Saving Account'
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, emailid, balance FROM `customers` WHERE id='%s'" % session.get('id'))
            bal = cur.fetchall()

            if request.method == 'POST':
                bankdetails = request.form
                bankamount = bankdetails['bankamount']
                banknumber = bankdetails['banknumber']
                bankpassword = bankdetails['bankpassword']
                cur.execute("SELECT * FROM `bank_details` WHERE emailid='%s'" % session.get('emailid'))
                bank_data = cur.fetchall()
                if int(bank_data[0][5]) >= int(bankamount) and bank_data[0][2] == banknumber and bank_data[0][6] == bankpassword:
                    remain = int(bank_data[0][5]) - int(bankamount)
                    addbal = int(bal[0][2]) + int(bankamount)
                    cur.execute("UPDATE customers SET balance=%s where id=%s", (addbal, session.get('id')))
                    cur.execute("UPDATE `bank_details` SET `account_balance`='%s' WHERE `account_no`=%s", (remain, banknumber))
                    mysql.connection.commit()
                    return redirect(url_for('payment'))
                else:
                    flash('Data Incorrect!')
            
            cur.execute("SELECT * FROM `bank_details` WHERE emailid='%s'" % session.get('emailid'))
            data = cur.fetchall()
            return render_template('addmoney.html', title=title, data=data, balance=bal, addmoney=addmoney)
        elif addmoney == 'Credit Card':
            cur = mysql.connection.cursor()
            addmoney = 'Credit Card'
            cur.execute("SELECT id, emailid, balance FROM `customers` WHERE id='%s'" % session.get('id'))
            bal = cur.fetchall()

            if request.method == 'POST':
                carddetails = request.form
                cardamount = carddetails['cardamount']
                cardnumber = carddetails['cardnumber']
                cardcvv = carddetails['cardcvv']
                cur.execute("SELECT * FROM `card_details` WHERE emailid='%s'" % session.get('emailid'))
                card_data = cur.fetchall()
                if int(card_data[0][6]) >= int(cardamount) and card_data[0][2] == cardnumber and card_data[0][5] == cardcvv:
                    remain = int(card_data[0][6]) - int(cardamount)
                    addbal = int(bal[0][2]) + int(cardamount)
                    cur.execute("UPDATE customers SET balance=%s where id=%s", (addbal, session.get('id')))
                    cur.execute("UPDATE `card_details` SET `card_balance`='%s' WHERE `card_number`=%s", (remain, cardnumber))
                    mysql.connection.commit()
                    return redirect(url_for('payment'))
                else:
                    flash('Data Incorrect!')

            cur.execute("SELECT * FROM `card_details` WHERE emailid='%s'" % session.get('emailid'))
            data = cur.fetchall()
            return render_template('addmoney.html', title=title, balance=bal, addmoney=addmoney)
        return render_template('addmoney.html', title=title)


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
    directory = str(data[0][0])
    path = os.path.join(app.config['UPLOAD_FOLDER'], directory)
    if status == 'Not-Uploaded':
        for x in os.listdir(path):
            x = path + '/' + x
            os.unlink(x)
    return render_template('documentcheck.html', title=title, emailid=emailid, data=data)


@app.route("/logout")
def logout():
    session.pop('id', '')
    session.pop('emailid', '')
    session.clear()
    return redirect(url_for('login'))   

if __name__ == '__main__':
    app.run(debug=True)