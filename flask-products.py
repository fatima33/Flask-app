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


@app.route('/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)
    
@app.route('/products/get-one', methods=['GET'])
def get_product():
 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    # Convert tuple to subscribable dictionary
   
    resultDict = dict((x, [y,z]) for x, y,z in data)
    print("The result dictionary:", resultDict)
    
    resp = jsonify(success=False)   # Returns False by default 
    prod_code = request.args.get('prod_code')
    if(prod_code is not None):
        prod_code1 = int(prod_code)
        
        if resultDict.get(prod_code1) is not None:
            sqlst="SELECT * FROM products WHERE prod_code = %s"
            values=prod_code
            cur.execute(sqlst ,values)
            mysql.connection.commit()
            data = cur.fetchall()

            flash('One product shown')
            resp = jsonify(data)
          
    cur.close()
    
    return resp

@app.route('/products/delete', methods=['PUT'])
def delete_products():
 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    # Convert tuple to subscribable dictionary
   
    #res = {key: value for key, value in a}
    resultDict = dict((x, [y,z]) for x, y,z in data)
    print("The result dictionary:", resultDict)
    
    prod_code = request.args.get('prod_code')
    prod_code1 = int(prod_code)
    resp = jsonify(success=False)

    if resultDict.get(prod_code1) is not None:
  
        sqlst="DELETE FROM products WHERE prod_code = %s"
        values=prod_code
        cur.execute(sqlst ,values)
        mysql.connection.commit()

        flash('You have successfully deleted product')
        resp = jsonify(success=True)
        
    cur.close()
    
    return resp

@app.route('/products/update', methods=['PUT'])
def update_products():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    data = cur.fetchall()
    # Convert tuple to JSON
    #json_data = json.dumps(data)
    print(type(data))
    #res = {key: value for key, value in a}
    resultDict = dict((x, [y,z]) for x, y,z in data)
    print("The result dictionary:", resultDict)

    
    prod_code = request.args.get('prod_code')
    description = request.args.get('description')
    rate = request.args.get('rate')
    
    if(prod_code is not None)
        prod_code1 = int(prod_code)

    resp = jsonify(success=False)

    if prod_code is not None and resultDict.get(prod_code1) is not None:
        sqlst="update products SET description = %s, rate = %s WHERE prod_code = %s"
        values=[ (description), (rate),(prod_code)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash("updated product successfully")
        resp = jsonify(success=True)
    elif prod_code is not None and resultDict.get(prod_code1) is None:
        sqlst="insert into products (prod_code,description, rate) values (%s, %s, %s) "
        values=[ (prod_code),(description), (rate)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash("inserted product successfully")
        resp = jsonify(success=True)

    
    cur.close()
    return resp

@app.route('/products/insert', methods=['POST'])
def insert_products():
    
    cur = mysql.connection.cursor()
    
    prod_code = request.args.get('prod_code')
    description = request.args.get('description')
    rate = request.args.get('rate')

    resp = jsonify(success=False)

    if prod_code is not None and resultDict.get(prod_code1) is not None:
        sqlst="insert into products (prod_code,description, rate) values (%s, %s, %s) "
        values=[ (prod_code),(description), (rate)]
        cur.execute(sqlst ,values)
        mysql.connection.commit()
        flash('You have successfully inserted product')
        resp = jsonify(success=True)
   
    cur.close()
    return resp


if __name__ == '__main__':
    app.run(debug=True)
