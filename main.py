from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__, static_url_path='')

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
    if request.method == 'POST':
        # Request Data from HTML file from
        userDetails = request.form
        userid = userDetails['userid']
        emailid = userDetails['emailid']
        password = userDetails['password']

        # Create cursor to connect to database and execute CRUD (insert, update and delete) operations
        cur = mysql.connection.cursor()
        cur.execute('INSERT into customers(userid, emailid, password) values(%s, %s, %s)', (userid, emailid, password))
        mysql.connection.commit()
        cur.close()
        return 'Success'
    return render_template('register.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

if __name__ == '__main__':
    app.run(debug=True)
