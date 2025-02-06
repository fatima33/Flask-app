from flask import Flask,  flash,jsonify, request , Response, json
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fatimaroot'
app.config['MYSQL_DB'] = 'flaskapp'
app.secret_key = "super secret key"
mysql = MySQL(app)


@app.route('/salesdet')
def get_salesdets():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sales_det')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)
    
@app.route('/salesdet/get-bill-data', methods=['GET'])
def get_salesdet():
    
    resp = jsonify(success=False)   # Returns False by default 
    
    bill_no = request.args.get('bill_no')
          
    if bill_no is not None:
        cur = mysql.connection.cursor()
        sqlst="SELECT * FROM sales_det WHERE bill_no = %s"
        values=[(bill_no)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        data = cur.fetchall()
        print("hello")

        flash('One Bill data shown')
        resp = jsonify(data)
        cur.close()
    
    return resp

@app.route('/salesdet/add-product', methods=['POST'])
def add_product_salesdet():
 
    bill_no = request.args.get('bill_no')
    prod_code = request.args.get('prod_code')
    quantity = request.args.get('quantity')
    rate = request.args.get('rate')
    disc = request.args.get('disc')
    net_rate = request.args.get('net_rate')
    amount = request.args.get('amount')

    resp = jsonify(success=False)

    if bill_no is not None and prod_code is not None:
        cur = mysql.connection.cursor()
        sqlst="insert into sales_det (bill_no,prod_code,quantity,rate,disc,net_rate,amount) values (%s, %s, %s,%s, %s, %s, %s)"
        values=[(bill_no),(prod_code),(quantity),(rate),(disc), (net_rate),(amount)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()

        flash('You have successfully inserted sales details')
        resp = jsonify(success=True)

    return resp

@app.route('/salesdet/delete-product', methods=['PUT'])
def delete_product_salesdet():
 
    bill_no = request.args.get('bill_no')
    prod_code = request.args.get('prod_code')

    resp = jsonify(success=False)

    if bill_no is not None and prod_code is not None:
        cur = mysql.connection.cursor()
  
        sqlst="DELETE FROM sales_det WHERE bill_no = %s and prod_code = %s"
        values=[(bill_no),(prod_code)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()

        flash('You have successfully deleted sales details')
        resp = jsonify(success=True)
        cur.close()
    
    return resp

@app.route('/salesdet/update-product', methods=['PUT'])
def update_product_salesdet():
      
    bill_no = request.args.get('bill_no')
    prod_code = request.args.get('prod_code')
    quantity = request.args.get('quantity')
    rate = request.args.get('rate')
    disc = request.args.get('disc')
    net_rate = request.args.get('net_rate')
    amount = request.args.get('amount')

    cur = mysql.connection.cursor()
    sqlst="SELECT * FROM sales_det WHERE bill_no=%s and prod_code=%s"
    values=[(bill_no),(prod_code)]
    cur.execute(sqlst ,values)
    data = cur.fetchall()

    resp = jsonify(success=False)

    if data is not None:
        sqlst="update sales_det SET quantity = %s, rate = %s, disc = %s, net_rate = %s, amount = %s WHERE bill_no = %s and prod_code = %s"
        values=[(bill_no),(prod_code),(quantity),(rate),(disc), (net_rate),(amount)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash("updated sales details successfully")
        resp = jsonify(success=True)
    elif data is None and bill_no is not None and prod_code is not None:
        sqlst="insert into sales_det (bill_no,prod_code,quantity,rate,disc,net_rate,amount) values (%s, %s, %s,%s, %s, %s, %s)"
        values=[(bill_no),(prod_code),(quantity),(rate),(disc), (net_rate),(amount)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash("inserted sales details successfully")
        resp = jsonify(success=True)

    
    cur.close()
    return resp


if __name__ == '__main__':
    app.run(debug=True)
