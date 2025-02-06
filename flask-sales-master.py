from flask import Flask,  flash,jsonify, request , Response, json
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '****'
app.config['MYSQL_DB'] = 'flaskapp'
app.secret_key = "super secret key"
mysql = MySQL(app)


@app.route('/salesmaster')
def get_salemasters():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sales_master')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)
    
@app.route('/salesmaster/get-one', methods=['GET'])
def get_salesmaster():
 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sales_master')
    data = cur.fetchall()
    # Convert tuple to subscribable dictionary
   
    resultDict = dict((a, [b,c,d,e,f]) for a, b,c,d,e,f in data)
    print("The result dictionary:", resultDict)
    
    resp = jsonify(success=False)   # Returns False by default 
    
    bill_no = request.args.get('bill_no')

    if(bill_no is not None):
        bill_no1 = int(bill_no)
        print(resultDict.get(bill_no1))
        
        if resultDict.get(bill_no1) is not None:
            sqlst="SELECT * FROM sales_master WHERE bill_no = %s"
            values=[(bill_no)]
            cur.execute(sqlst ,values)
            mysql.connection.commit()
            data = cur.fetchall()
            print("hello")

            flash('One Bill shown')
            resp = jsonify(data)
          
    cur.close()
    
    return resp

@app.route('/salesmaster/delete', methods=['PUT'])
def delete_salesmaster():
 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sales_master')
    data = cur.fetchall()
    # Convert tuple to subscribable dictionary
   
    resultDict = dict((a, [b,c,d,e,f]) for a, b,c,d,e,f in data)
    print("The result dictionary:", resultDict)
    
    bill_no = request.args.get('bill_no')
    bill_no1 = int(bill_no)
    resp = jsonify(success=False)

    if resultDict.get(bill_no1) is not None:
  
        sqlst="DELETE FROM sales_master WHERE bill_no = %s"
        values=bill_no
        cur.execute(sqlst ,values)
        mysql.connection.commit()

        flash('You have successfully deleted sales_master')
        resp = jsonify(success=True)
        
    cur.close()
    
    return resp

@app.route('/salesmaster/update', methods=['PUT'])
def update_salesmaster():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sales_master')
    data = cur.fetchall()
    
                                  # Convert tuple to subscribable dictionary

    resultDict = dict((a, [b,c,d,e,f]) for a, b,c,d,e,f in data)
    print("The result dictionary:", resultDict)

    
    bill_no = request.args.get('bill_no')
    date = request.args.get('date')
    total_qty = request.args.get('total_qty')
    total_amount = request.args.get('total_amount')
    disc = request.args.get('disc')
    net_amount = request.args.get('net_amount')
    
    if(bill_no is not None):
        bill_no1 = int(bill_no)

    resp = jsonify(success=False)

    if bill_no is not None and resultDict.get(bill_no1) is not None:
        sqlst="update sales_master SET date = %s, total_qty = %s, total_amount = %s, disc = %s, net_amount = %s WHERE bill_no = %s"
        values=[ (date),(total_qty),(total_amount), (disc),(net_amount),(bill_no)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash("updated salesmaster successfully")
        resp = jsonify(success=True)
    elif bill_no is not None and resultDict.get(bill_no1) is None:
        sqlst="insert into sales_master (bill_no,date,total_qty,total_amount,disc,net_amount) values (%s, %s, %s,%s, %s, %s)"
        values=[ (bill_no),(date),(total_qty),(total_amount), (disc),(net_amount)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash("inserted salesmaster successfully")
        resp = jsonify(success=True)

    
    cur.close()
    return resp

@app.route('/salesmaster/insert', methods=['POST'])
def insert_salesmaster():
    
    cur = mysql.connection.cursor()
    
    bill_no = request.args.get('bill_no')
    date = request.args.get('date')
    total_qty = request.args.get('total_qty')
    total_amount = request.args.get('total_amount')
    disc = request.args.get('disc')
    net_amount = request.args.get('net_amount')

    if(bill_no is not None):
        bill_no1 = int(bill_no)

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sales_master')
    data = cur.fetchall()
    # Convert tuple to subscribable dictionary
   
    resultDict = dict((a, [b,c,d,e,f]) for a, b,c,d,e,f in data)
    print("The result dictionary:", resultDict)

    resp = jsonify(success=False)

    if (bill_no is not None and bool(resultDict) is False) or (bill_no is not None and resultDict.get(bill_no1) is None): 
        sqlst="insert into sales_master (bill_no,date,total_qty,total_amount,disc,net_amount) values (%s, %s, %s,%s, %s, %s)"
        values=[(bill_no),(date),(total_qty),(total_amount), (disc),(net_amount)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash("inserted salesmaster successfully")
        resp = jsonify(success=True)


    cur.close()
    return resp


if __name__ == '__main__':
    app.run(debug=True)
