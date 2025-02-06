from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fatimaroot'
app.config['MYSQL_DB'] = 'flaskapp'
app.secret_key = "super secret key"
mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    cur.close()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)
