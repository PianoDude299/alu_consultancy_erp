from flask import Flask, render_template, request, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask.json import jsonify
import MySQLdb.cursors
import os
import json
import streamlit as st

app = Flask(__name__)

app.secret_key = 'pass'

app.config['MYSQL_HOST'] = 'alusql.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'ConsultancyERP'
app.config['MYSQL_PASSWORD'] = 'AzureSQL123'
app.config['MYSQL_DB'] = 'vitproject'


mysql = MySQL(app)

DB_HOST = "alusql.mysql.database.azure.com"
DB_USER = "ConsultancyERP"
DB_PASS = "AzureSQL123"
DB_NAME = "vitproject"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/manager_login', methods=['GET','POST'])
def manager_login():
    msg = ''
    if request.method == 'POST' and 'sitenum' in request.form and 'username' in request.form and 'password' in request.form:
        global sitenum
        sitenum = request.form['sitenum']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE Site =%s AND username = %s AND password = %s', (sitenum, username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['password'] = account['password']
            session['username'] = account['username']
            return render_template('manager_home.html',user=session['username'], site=sitenum)
        else:
            msg = 'Incorrect username/password!'
        
    return render_template('manager_login.html',msg=msg)

@app.route('/director_login', methods=['GET', 'POST'])
def director_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE Site = %s AND username = %s AND password = %s', (0, username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['password'] = account['password']
            session['username'] = account['username']
            return render_template('director_home.html', user=session['username'])
        else:
            msg = 'Incorrect username/password!'

    return render_template('director_login.html', msg=msg)


@app.route('/d_material_purchase', methods=['GET', 'POST','PUT'])
def d_material_purchase():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'purchase-date' in request.form and 'material-input' in request.form and 'quantity-input' in request.form and 'price-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        date = request.form['purchase-date']
        material = request.form['material-input']
        quantity = request.form['quantity-input']
        price = request.form['price-input']
        choice = request.form['HiddenField']
        tid = request.form['tid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM purchase WHERE T_ID=%s", (tid,))
        record = cursor.fetchone()
        if choice=='1':
            cursor.execute("ALTER TABLE vitproject.purchase AUTO_INCREMENT = 1")
            mysql.connection.commit()
            
            #if 'bill-image' in request.files:
                #bill_image = request.files['bill-image']
                #if bill_image.filename != '':
                    #filename = secure_filename(bill_image.filename)
                    # Directory where files are saved
                    #purchase_dir = os.path.join(os.getcwd(), 'uploads', 'purchase')

                    # Get the count of files in the 'purchase' folder
                    #file_count = len([name for name in os.listdir(purchase_dir) if os.path.isfile(os.path.join(purchase_dir, name))])

                    # Construct the new filename
                    #new_filename = f'Purchase_{file_count}{os.path.splitext(filename)[1]}'

                    # Construct the full file path
                    #file_path = os.path.join(purchase_dir, new_filename)

                   # bill_image.save(file_path)
                    #insert_query = "insert into vitproject.purchase (Site, DOB, Material, Quantity, Price,Bill) values (%s, %s, %s, %s, %s, %s)"
                    #data = (sitenum,date,material,quantity,price, file_path)
                    #cursor.execute(insert_query, data)
                    #mysql.connection.commit()
                #else:
            insert_query = "insert into vitproject.purchase (Site, DOB, Material, Quantity, Price) values (%s, %s, %s, %s, %s)"
            data = (sitenum,date,material,quantity,price)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful!'
            return render_template('d_material_purchase.html',msg=msg)
        else:
            if tid is not None and tid != "":
                if record:
                    #if 'bill-image' in request.files:
                        #bill_image = request.files['bill-image']
                        #if bill_image.filename != '':
                            #old_bill=record['Bill']
                            #if old_bill and os.path.exists(old_bill):
                                #os.remove(old_bill)
                            #filename = secure_filename(bill_image.filename)
                            # Directory where files are saved
                            #purchase_dir = os.path.join(os.getcwd(), 'uploads', 'purchase')

                            # Get the count of files in the 'purchase' folder
                            #file_count = len([name for name in os.listdir(purchase_dir) if os.path.isfile(os.path.join(purchase_dir, name))])

                            # Construct the new filename
                            #new_filename = f'Purchase_{file_count}{os.path.splitext(filename)[1]}'

                            # Construct the full file path
                            #file_path = os.path.join(purchase_dir, new_filename)

                            #bill_image.save(file_path)
                            #update_query = "UPDATE vitproject.purchase SET Quantity=%s, Price=%s, Site=%s, DOB=%s, Material=%s, Bill=%s WHERE T_ID=%s"
                            #data = (quantity,price,sitenum, date, material,file_path,tid)
                            #cursor.execute(update_query, data)
                            #mysql.connection.commit()
                        #else:
                    update_query = "UPDATE vitproject.purchase SET Quantity=%s, Price=%s, Site=%s, DOB=%s, Material=%s WHERE T_ID=%s"
                    data = (quantity,price,sitenum, date, material,tid)
                    cursor.execute(update_query, data)
                    mysql.connection.commit()
                    msg = 'Updation Successful!'
                else:
                    msg = 'Record not found in Site {}!'.format(sitenum)
            else:
                msg = 'Enter T_ID for Updation!'
        
    return render_template('d_material_purchase.html',msg=msg)

@app.route('/m_material_purchase', methods=['GET', 'POST','PUT'])
def m_material_purchase():
    msg=''
    if request.method == 'POST' and 'purchase-date' in request.form and 'material-input' in request.form and 'quantity-input' in request.form and 'price-input' in request.form:
        date = request.form['purchase-date']
        material = request.form['material-input']
        quantity = request.form['quantity-input']
        price = request.form['price-input']
        choice = request.form['HiddenField']
        tid = request.form['tid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.purchase WHERE T_ID=%s AND Site=%s', (tid,sitenum))
        record = cursor.fetchone()
        if choice=='1':
            cursor.execute("ALTER TABLE vitproject.purchase AUTO_INCREMENT = 1")
            mysql.connection.commit()
            #if 'bill-image' in request.files:
                #bill_image = request.files['bill-image']
                #if bill_image.filename != '':
                    #filename = secure_filename(bill_image.filename)
                    # Directory where files are saved
                    #purchase_dir = os.path.join(os.getcwd(), 'uploads', 'purchase')

                    # Get the count of files in the 'purchase' folder
                    #file_count = len([name for name in os.listdir(purchase_dir) if os.path.isfile(os.path.join(purchase_dir, name))])

                    # Construct the new filename
                    #new_filename = f'Purchase_{file_count}{os.path.splitext(filename)[1]}'

                    # Construct the full file path
                    #file_path = os.path.join(purchase_dir, new_filename)

                    #bill_image.save(file_path)
                    #insert_query = "insert into vitproject.purchase (Site, DOB, Material, Quantity, Price,Bill) values (%s, %s, %s, %s, %s, %s)"
                    #data = (sitenum,date,material,quantity,price, file_path)
                    #cursor.execute(insert_query, data)
                    #mysql.connection.commit()
                #else:
            insert_query = "insert into vitproject.purchase (Site, DOB, Material, Quantity, Price) values (%s, %s, %s, %s, %s)"
            data = (sitenum,date,material,quantity,price)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful!'
            return render_template('m_material_purchase.html',msg=msg, Site=sitenum)
        else:
            if tid is not None and tid != "":
                if record:
                    #if 'bill-image' in request.files:
                        #bill_image = request.files['bill-image']
                        #if bill_image.filename != '':
                            #old_bill=record['Bill']
                           # if old_bill and os.path.exists(old_bill):
                                #os.remove(old_bill)
                            #filename = secure_filename(bill_image.filename)
                            # Directory where files are saved
                            #purchase_dir = os.path.join(os.getcwd(), 'uploads', 'purchase')

                            # Get the count of files in the 'purchase' folder
                            #file_count = len([name for name in os.listdir(purchase_dir) if os.path.isfile(os.path.join(purchase_dir, name))])

                            # Construct the new filename
                            #new_filename = f'Purchase_{file_count}{os.path.splitext(filename)[1]}'

                            # Construct the full file path
                            #file_path = os.path.join(purchase_dir, new_filename)

                            #bill_image.save(file_path)
                            #update_query = "UPDATE vitproject.purchase SET Quantity=%s, Price=%s, Site=%s, DOB=%s, Material=%s, Bill=%s WHERE T_ID=%s"
                            #data = (quantity,price,sitenum, date, material,file_path,tid)
                            #cursor.execute(update_query, data)
                            #mysql.connection.commit()
                        #else:
                    update_query = "UPDATE vitproject.purchase SET Quantity=%s, Price=%s, Site=%s, DOB=%s, Material=%s WHERE T_ID=%s"
                    data = (quantity,price,sitenum, date, material,tid)
                    cursor.execute(update_query, data)
                    mysql.connection.commit()
                    msg = 'Updation Successful!'
                else:
                    msg = 'Record not found in Site {}!'.format(sitenum)
            else:
                msg = 'Enter T_ID for Updation!'
        
    return render_template('m_material_purchase.html',msg=msg, Site=sitenum)


@app.route('/d_local_expenditure', methods=['GET', 'POST','PUT'])
def d_local_expenditure():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'exp-date' in request.form and 'activity-input' in request.form and 'amount-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        date = request.form['exp-date']
        activity = request.form['activity-input']
        amount = request.form['amount-input']
        choice = request.form['HiddenField']
        tid = request.form['tid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.expenditure WHERE T_ID=%s', (tid,))
        record = cursor.fetchone()
        if choice=='1':
            cursor.execute("ALTER TABLE vitproject.expenditure AUTO_INCREMENT = 1")
            mysql.connection.commit()
            #if 'bill-image' in request.files:
                #bill_image = request.files['bill-image']
                #if bill_image.filename != '':
                    #filename = secure_filename(bill_image.filename)
                    # Directory where files are saved
                    #expenditure_dir = os.path.join(os.getcwd(), 'uploads', 'expenditure')

                    # Get the count of files in the 'expenditure' folder
                    #file_count = len([name for name in os.listdir(expenditure_dir) if os.path.isfile(os.path.join(expenditure_dir, name))])

                    # Construct the new filename
                    #new_filename = f'Expenditure_{file_count}{os.path.splitext(filename)[1]}'

                    # Construct the full file path
                    #file_path = os.path.join(expenditure_dir, new_filename)

                    #bill_image.save(file_path)
                    #insert_query = "insert into vitproject.expenditure (Site, DOB, Activity, Amount, Bill) values (%s, %s, %s, %s, %s)"
                    #data = (sitenum,date,activity,amount, file_path)
                    #cursor.execute(insert_query, data)
                    #mysql.connection.commit()
                #else:
            insert_query = "insert into vitproject.expenditure (Site, DOB, Activity, Amount) values (%s, %s, %s, %s)"
            data = (sitenum,date,activity,amount)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful!'
            return render_template('d_local_expenditure.html',msg=msg)
        else:
            if tid is not None and tid != "":
                if record:
                    #if 'bill-image' in request.files:
                        #bill_image = request.files['bill-image']
                        #if bill_image.filename != '':
                            #old_bill=record['Bill']
                            #if old_bill and os.path.exists(old_bill):
                                #os.remove(old_bill)
                            #filename = secure_filename(bill_image.filename)
                            # Directory where files are saved
                            #expenditure_dir = os.path.join(os.getcwd(), 'uploads', 'expenditure')

                            # Get the count of files in the 'expenditure' folder
                            #file_count = len([name for name in os.listdir(expenditure_dir) if os.path.isfile(os.path.join(expenditure_dir, name))])

                            # Construct the new filename
                            #new_filename = f'Expenditure_{file_count}{os.path.splitext(filename)[1]}'

                            # Construct the full file path
                            #file_path = os.path.join(expenditure_dir, new_filename)

                            #bill_image.save(file_path)
                            #update_query = "UPDATE vitproject.expenditure SET Amount=%s, Site=%s, DOB=%s, Activity=%s, Bill=%s WHERE T_ID=%s"
                            #data = (amount,sitenum, date, activity,file_path,tid)
                            #cursor.execute(update_query, data)
                            #mysql.connection.commit()
                        #else:
                    update_query = "UPDATE vitproject.expenditure SET Amount=%s, Site=%s, DOB=%s, Activity=%s WHERE T_ID=%s"
                    data = (amount,sitenum, date, activity,tid)
                    cursor.execute(update_query, data)
                    mysql.connection.commit()
                    msg = 'Updation Successful!'
                else:
                    msg='Record not found in Site {}!'.format(sitenum)
            else:
                msg = 'Enter T_ID for Updation!'
    
    return render_template('d_local_expenditure.html',msg=msg)

@app.route('/m_local_expenditure', methods=['GET', 'POST','PUT'])
def m_local_expenditure():
    msg=''
    if request.method == 'POST' and 'exp-date' in request.form and 'activity-input' in request.form and 'amount-input' in request.form:
        date = request.form['exp-date']
        activity = request.form['activity-input']
        amount = request.form['amount-input']
        choice = request.form['HiddenField']
        tid=request.form['tid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.expenditure WHERE T_ID=%s AND Site=%s', (tid,sitenum))
        record = cursor.fetchone()
        if choice=='1':
            cursor.execute("ALTER TABLE vitproject.expenditure AUTO_INCREMENT = 1")
            mysql.connection.commit()
            #if 'bill-image' in request.files:
                #bill_image = request.files['bill-image']
                #if bill_image.filename != '':
                    #filename = secure_filename(bill_image.filename)
                    # Directory where files are saved
                    #expenditure_dir = os.path.join(os.getcwd(), 'uploads', 'expenditure')

                    # Get the count of files in the 'expenditure' folder
                    #file_count = len([name for name in os.listdir(expenditure_dir) if os.path.isfile(os.path.join(expenditure_dir, name))])

                    # Construct the new filename
                    #new_filename = f'Expenditure_{file_count}{os.path.splitext(filename)[1]}'

                    # Construct the full file path
                    #file_path = os.path.join(expenditure_dir, new_filename)

                    #bill_image.save(file_path)
                    #insert_query = "insert into vitproject.expenditure (Site, DOB, Activity, Amount, Bill) values (%s, %s, %s, %s, %s)"
                    #data = (sitenum,date,activity,amount, file_path)
                    #cursor.execute(insert_query, data)
                    #mysql.connection.commit()
                #else:
            insert_query = "insert into vitproject.expenditure (Site, DOB, Activity, Amount) values (%s, %s, %s, %s)"
            data = (sitenum,date,activity,amount)
            cursor.execute(insert_query, data)
            mysql.connection.commit()
            msg = 'Insertion Succesful!'
            return render_template('m_local_expenditure.html',msg=msg, Site=sitenum)
        else:
            if tid is not None and tid != "":
                if record:
                    #if 'bill-image' in request.files:
                        #bill_image = request.files['bill-image']
                        #if bill_image.filename != '':
                            #old_bill=record['Bill']
                            #if old_bill and os.path.exists(old_bill):
                                #os.remove(old_bill)
                            #filename = secure_filename(bill_image.filename)
                            # Directory where files are saved
                            #expenditure_dir = os.path.join(os.getcwd(), 'uploads', 'expenditure')

                            # Get the count of files in the 'expenditure' folder
                            #file_count = len([name for name in os.listdir(expenditure_dir) if os.path.isfile(os.path.join(expenditure_dir, name))])

                            # Construct the new filename
                            #new_filename = f'Expenditure_{file_count}{os.path.splitext(filename)[1]}'

                            # Construct the full file path
                            #file_path = os.path.join(expenditure_dir, new_filename)
                            
                            #bill_image.save(file_path)
                            #update_query = "UPDATE vitproject.expenditure SET Amount=%s, Site=%s, DOB=%s, Activity=%s, Bill=%s WHERE T_ID=%s"
                            #data = (amount,sitenum, date, activity,file_path, tid)
                            #cursor.execute(update_query, data)
                            #mysql.connection.commit()
                        #else:
                    update_query = "UPDATE vitproject.expenditure SET Amount=%s, Site=%s, DOB=%s, Activity=%s WHERE T_ID=%s"
                    data = (amount,sitenum, date, activity,tid)
                    cursor.execute(update_query, data)
                    mysql.connection.commit()
                    msg = 'Updation Successful!'
                else:
                    msg='Record not found in Site {}!'.format(sitenum)
            else:
                msg = 'Enter T_ID for Updation!'
    
    return render_template('m_local_expenditure.html',msg=msg, Site=sitenum)

@app.route('/d_staff_salary', methods=['GET', 'POST','PUT'])
def d_staff_salary():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'name-input' in request.form and 'empid-input' in request.form and 'salary-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        name = request.form['name-input']
        empid = request.form['empid-input']
        salary = request.form['salary-input']
        choice = request.form['HiddenField']
        tid = request.form['tid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.salary WHERE EmpID=%s AND Site=%s', (empid, sitenum))
        record = cursor.fetchone()
        if choice=='1':
            if not record:
                cursor.execute('SELECT * FROM vitproject.labour WHERE EmpID=%s AND Site=%s', (empid, sitenum))
                record2 = cursor.fetchone()
                if record2:
                    cursor.execute("ALTER TABLE vitproject.salary AUTO_INCREMENT = 1")
                    mysql.connection.commit()
                    insert_query = "insert into vitproject.salary (Site, Name, EmpID, Salary) values (%s, %s, %s, %s)"
                    data = (sitenum,name,empid,salary)
                    cursor.execute(insert_query, data)
                    mysql.connection.commit()
                    msg = 'Insertion Succesful!'
                    return render_template('d_staff_salary.html',msg=msg)
                else:
                    msg = 'Record with Employee ID not found in Site {} labour records!'.format(sitenum)
            else:
                msg = 'Record with Employee ID already exists in Site {}!'.format(sitenum)
        else:
                if tid is not None and tid != "":
                    cursor.execute('SELECT * FROM vitproject.login WHERE T_ID=%s', (tid,))
                    record1 = cursor.fetchone()
                    if record1:
                        update_query = "UPDATE vitproject.salary SET Name=%s, Salary=%s, Site=%s, EmpID=%s WHERE T_ID=%s"
                        data = (name, salary,sitenum,empid,tid)
                        cursor.execute(update_query, data)
                        mysql.connection.commit()
                        msg = 'Updation Successful!'
                    else:
                        msg = 'Record not found!'
                else:
                    msg = 'Enter T_ID for Updation!'
        
    return render_template('d_staff_salary.html',msg=msg)

@app.route('/m_staff_salary', methods=['GET', 'POST','PUT'])
def m_staff_salary():
    msg=''
    if request.method == 'POST' and 'name-input' in request.form and 'empid-input' in request.form and 'salary-input' in request.form:
        name = request.form['name-input']
        empid = request.form['empid-input']
        salary = request.form['salary-input']
        choice = request.form['HiddenField']
        tid = request.form['tid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.salary WHERE EmpID=%s AND Site=%s', (empid, sitenum))
        record = cursor.fetchone()
        if choice=='1':
            if not record:
                cursor.execute('SELECT * FROM vitproject.labour WHERE EmpID=%s AND Site=%s', (empid, sitenum))
                record2 = cursor.fetchone()
                if record2:
                    cursor.execute("ALTER TABLE vitproject.salary AUTO_INCREMENT = 1")
                    mysql.connection.commit()
                    insert_query = "insert into vitproject.salary (Site, Name, EmpID, Salary) values (%s, %s, %s, %s)"
                    data = (sitenum,name,empid,salary)
                    cursor.execute(insert_query, data)
                    mysql.connection.commit()
                    msg = 'Insertion Succesful!'
                    return render_template('m_staff_salary.html',msg=msg, Site=sitenum)
                else:
                    msg = 'Record with Employee ID not found in Site {} labour records!'.format(sitenum)
            else:
                msg = 'Record with Employee ID already exists in Site {}!'.format(sitenum)
        else:
                if tid is not None and tid != "":
                    cursor.execute('SELECT * FROM vitproject.login WHERE T_ID=%s AND Site=%s', (tid,sitenum))
                    record1 = cursor.fetchone()
                    if record1:
                        print(name,salary,sitenum,empid)
                        update_query = "UPDATE vitproject.salary SET Name=%s, Salary=%s, Site=%s, EmpID=%s WHERE T_ID=%s"
                        data = (name, salary,sitenum,empid,tid)
                        cursor.execute(update_query, data)
                        mysql.connection.commit()
                        msg = 'Updation Successful!'
                    else:
                        msg = 'Record not found in Site {}!'.format(sitenum)
                else:
                    msg = 'Enter T_ID for Updation!'
        
    return render_template('m_staff_salary.html',msg=msg, Site=sitenum)

@app.route('/d_manager_accounts', methods=['GET', 'POST','PUT'])
def d_manager_accounts():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'username-input' in request.form and 'password-input' in request.form:
        global sitenum
        sitenum = request.form['site-num']
        username = request.form['username-input']
        password = request.form['password-input']
        choice = request.form['HiddenField']
        tid = request.form['tid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vitproject.login WHERE Username=%s AND Site=%s', (username, sitenum))
        record = cursor.fetchone()
        if choice=='1':
            if not record:
                cursor.execute("ALTER TABLE vitproject.login AUTO_INCREMENT = 1")
                mysql.connection.commit()
                insert_query = "insert into vitproject.login (Site, Username, Password) values (%s, %s, %s)"
                data = (sitenum,username,password)
                cursor.execute(insert_query, data)
                mysql.connection.commit()
                msg = 'Insertion Succesful!'
                return render_template('d_manager_accounts.html',msg=msg)
            else:
                msg = 'Manager account already exists!'
        else:
            if tid is not None and tid != "":
                cursor.execute('SELECT * FROM vitproject.login WHERE T_ID=%s', (tid,))
                record1 = cursor.fetchone()
                if record1:
                    update_query = "UPDATE vitproject.login SET Site=%s, Username=%s AND Password=%s WHERE T_ID=%s"
                    data = (sitenum, username, password,tid)
                    cursor.execute(update_query, data)
                    mysql.connection.commit()
                    msg = 'Updation Successful!'
                else:
                    msg = 'Manager account not found!'
            else:
                msg = 'Enter T_ID for Updation!'

    return render_template('d_manager_accounts.html',msg=msg)

@app.route('/d_labour', methods=['GET', 'POST','PUT'])
def d_labour():
    msg=''
    if request.method == 'POST' and 'site-num' in request.form and 'name-input' in request.form and 'empid-input' in request.form and 'joining-date' in request.form and 'gender-input' in request.form and 'address-input' in request.form and 'designation-input' in request.form:
        languages = request.form.getlist('languages-input')
        if len(languages) != 0: 
            global sitenum
            sitenum = request.form['site-num']
            name = request.form['name-input']
            empid = request.form['empid-input']
            joining_date = request.form['joining-date']
            gender = request.form['gender-input']
            languages = request.form.getlist('languages-input')
            address = request.form['address-input']
            designation = request.form['designation-input']
            choice = request.form['HiddenField']
            tid = request.form['tid']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM vitproject.labour WHERE Site=%s AND empid=%s', (sitenum, empid))
            record = cursor.fetchone()
            if choice=='1':
                if not record:
                    cursor.execute("ALTER TABLE vitproject.labour AUTO_INCREMENT = 1")
                    mysql.connection.commit()
                    insert_query = "INSERT INTO vitproject.labour (Site, Name, EmpID, DOB, Gender, Languages, Address, Designation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    data = (sitenum, name, empid, joining_date, gender, ",".join(languages), address, designation)
                    cursor.execute(insert_query, data)
                    mysql.connection.commit()
                    msg = 'Insertion Successful!'
                else:
                    msg = 'Record with Employee ID already exists in Site {}!'.format(sitenum)
            else:
                    if tid is not None and tid != "":
                        cursor.execute('SELECT * FROM vitproject.labour WHERE T_ID=%s', (tid,))
                        record1 = cursor.fetchone()
                        if record1:
                            update_query = "UPDATE vitproject.labour SET Name=%s, DOB=%s, Gender=%s, Languages=%s, Address=%s, Designation=%s, Site=%s, EmpID=%s WHERE T_ID=%s"
                            data = (name, joining_date, gender, ",".join(languages), address, designation,sitenum, empid,tid)
                            cursor.execute(update_query, data)
                            mysql.connection.commit()
                            msg = 'Updation Successful!'
                        else:
                             msg = 'Record not found!'
                    else:
                        msg = 'Enter T_ID for Updation!'
        else:
            msg= 'Select atleast one language!'

    return render_template('d_labour.html', msg=msg)

@app.route('/m_labour', methods=['GET', 'POST','PUT'])
def m_labour():
    msg=''
    if request.method == 'POST' and 'name-input' in request.form and 'empid-input' in request.form and 'joining-date' in request.form and 'gender-input' in request.form and 'address-input' in request.form and 'designation-input' in request.form:
        languages = request.form.getlist('languages-input')
        if len(languages) != 0: 
            name = request.form['name-input']
            empid = request.form['empid-input']
            joining_date = request.form['joining-date']
            gender = request.form['gender-input']
            languages = request.form.getlist('languages-input')
            address = request.form['address-input']
            designation = request.form['designation-input']
            choice = request.form['HiddenField']
            tid=request.form['tid']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM vitproject.labour WHERE Site=%s AND EmpID=%s', (sitenum,empid))
            record = cursor.fetchone()

            if choice=='1':

                if not record:
                    cursor.execute("ALTER TABLE vitproject.labour AUTO_INCREMENT = 1")
                    mysql.connection.commit()
                    insert_query = "INSERT INTO vitproject.labour (Site, Name, EmpID, DOB, Gender, Languages, Address, Designation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    data = (sitenum, name, empid, joining_date, gender, ",".join(languages), address, designation)
                    cursor.execute(insert_query, data)
                    mysql.connection.commit()
                    msg = 'Insertion Successful!'
                else:
                    msg = 'Record with Employee ID already exists in Site {}!'.format(sitenum)
            else:
                    if tid is not None and tid != "":
                        cursor.execute('SELECT * FROM vitproject.labour WHERE T_ID=%s AND Site=%s', (tid,sitenum))
                        record1 = cursor.fetchone()
                        if record1:
                            update_query = "UPDATE vitproject.labour SET Name=%s, DOB=%s, Gender=%s, Languages=%s, Address=%s, Designation=%s, Site=%s, EmpID=%s WHERE T_ID=%s"
                            data = (name, joining_date, gender, ",".join(languages), address, designation,sitenum, empid,tid)
                            cursor.execute(update_query, data)
                            mysql.connection.commit()
                            msg = 'Updation Successful!'
                        else:
                             msg = 'Record not found in Site {}!'.format(sitenum)
                    else:
                        msg = 'Enter T_ID for Updation!'
                
        else:
            msg = 'Select atleast one language!'
        
    return render_template('m_labour.html', msg=msg, Site=sitenum)

@app.route('/d_report', methods=['GET', 'POST','PUT'])
def d_report():
    msg=''
    data = None
    if request.method=='POST' and 'site-num' in request.form and 'year' in request.form and 'month' in request.form:
        global sitenum
        sitenum=request.form['site-num']
        category=request.form['category']
        year=request.form['year']
        month=request.form['month']

        if category == "Expenditure":
            table_name = "expenditure"
            column_name = "Amount"
        elif category == "Purchase":
            table_name = "purchase"
            column_name = "Price"

        if year == "All Years":
                year_condition = "1"  # Always true
        else:
            year_condition = f"YEAR(DOB) = {year}"

        if month == "Overall":
            month_condition = ""
        else:
            month_condition = f"AND MONTH(DOB) = {month}"  # Extract the month number

        query = f"SELECT SUM({column_name}) FROM {table_name} WHERE {year_condition} {month_condition} AND Site = {sitenum}"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT SUM(%s) FROM %s WHERE %s %s AND Site = %s', (column_name, table_name, year_condition, month_condition, sitenum))
        cursor.execute(query)
        if category == "Expenditure":
            result = cursor.fetchone()['SUM(Amount)']
        else:
            result = cursor.fetchone()['SUM(Price)']

        month_dict = {
            'Overall': 'Overall',
            '1': 'January',
            '2': 'February',
            '3': 'March',
            '4': 'April',
            '5': 'May',
            '6': 'June',
            '7': 'July',
            '8': 'August',
            '9': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December'
        }

        if result is not None: 
            msg =f"Total {category} amount for Site {sitenum} {month_dict[month]} {year}: {result} Rs"
        else:
            msg = f"No {category} data available for Site {sitenum} {month_dict[month]} {year}"
        
        cursor.execute(f'SELECT * FROM {table_name} WHERE {year_condition} {month_condition} AND Site = {sitenum}')
        data = cursor.fetchall()
    return render_template('d_report.html', msg=msg, data=data)

@app.route('/m_report', methods=['GET', 'POST','PUT'])
def m_report():
    msg=''
    data=None
    global sitenum
    if request.method=='POST' and 'year' in request.form and 'month' in request.form:
        category=request.form['category']
        year=request.form['year']
        month=request.form['month']

        if category == "Expenditure":
            table_name = "expenditure"
            column_name = "Amount"
        elif category == "Purchase":
            table_name = "purchase"
            column_name = "Price"

        if year == "All Years":
                year_condition = "1"  # Always true
        else:
            year_condition = f"YEAR(DOB) = {year}"

        if month == "Overall":
            month_condition = ""
        else:
            month_condition = f"AND MONTH(DOB) = {month}"  # Extract the month number

        query = f"SELECT SUM({column_name}) FROM {table_name} WHERE {year_condition} {month_condition} AND Site = {sitenum}"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        if category == "Expenditure":
            result = cursor.fetchone()['SUM(Amount)']
        else:
            result = cursor.fetchone()['SUM(Price)']

        month_dict = {
            'Overall': 'Overall',
            '1': 'January',
            '2': 'February',
            '3': 'March',
            '4': 'April',
            '5': 'May',
            '6': 'June',
            '7': 'July',
            '8': 'August',
            '9': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December'
        }

        if result is not None: 
            msg =f"Total {category} amount for Site {sitenum} {month_dict[month]} {year}: {result} Rs"
        else:
            msg = f"No {category} data available for Site {sitenum} {month_dict[month]} {year}"

        cursor.execute(f'SELECT * FROM {table_name} WHERE {year_condition} {month_condition} AND Site = {sitenum}')
        data = cursor.fetchall()
    return render_template('m_report.html', msg=msg, Site=sitenum, data=data)

@app.route('/view_table/<table_name>', methods=['GET', 'POST'])
def view_table(table_name):
    msg = ''
    prev_page = request.args.get('prev_page', '/')  # Default to '/home' if not provided

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM vitproject.{table_name}')
        data = cursor.fetchall()

        if request.method == 'POST':
            if 'delete-record' in request.form and 't-id-input' in request.form:
                t_id = request.form['t-id-input']
                cursor.execute(f'SELECT * FROM vitproject.{table_name} WHERE T_ID=%s', (t_id,))
                record = cursor.fetchone()
                #if record and ('Bill' in record):
                    #old_bill=record['Bill']
                    #if old_bill and os.path.exists(old_bill):
                        #os.remove(record['Bill'])
                delete_query = f'DELETE FROM vitproject.{table_name} WHERE T_ID = %s'
                cursor.execute(delete_query, (t_id,))
                mysql.connection.commit()
                msg = 'Record deleted!'

        if data:
            return render_template('view_table.html', table_name=table_name, data=data, msg=msg, prev_page=prev_page)
        else:
            msg = f'No data found in the {table_name} table.'
    except Exception as e:
        msg = f'Error: {str(e)}'

    return render_template('view_table.html', table_name=table_name, msg=msg, prev_page=prev_page)


@app.route('/m_view_table/<table_name>', methods=['GET', 'POST'])
def m_view_table(table_name):
    msg = ''
    prev_page = request.args.get('prev_page', '/')  # Default to '/home' if not provided

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM vitproject.{table_name} where Site = {sitenum}')
        data = cursor.fetchall()

        if request.method == 'POST':
            if 'delete-record' in request.form and 't-id-input' in request.form:
                t_id = request.form['t-id-input']
                cursor.execute('SELECT * FROM vitproject.%s WHERE T_ID=%s', (table_name,t_id))
                record = cursor.fetchone()
                #if record and ('Bill' in record):
                    #old_bill=record['Bill']
                    #if old_bill and os.path.exists(old_bill):
                        #os.remove(record['Bill'])
                delete_query = f'DELETE FROM vitproject.{table_name} WHERE T_ID = %s'
                cursor.execute(delete_query, (t_id,))
                mysql.connection.commit()
                msg = 'Record deleted!'

        if data:
            return render_template('m_view_table.html', table_name=table_name, data=data, msg=msg, prev_page=prev_page)
        else:
            msg = f'No data found in the {table_name} table.'
    except Exception as e:
        msg = f'Error: {str(e)}'

    return render_template('m_view_table.html', table_name=table_name, msg=msg, prev_page=prev_page)





@app.route('/d_get_chart_data/<selectedYear>/<sitenum>')
def d_get_chart_data(selectedYear,sitenum):
    # Query database to get expenditure and purchase data for the selected year
    # Use the SQL query you provided earlier to retrieve the data
    # Replace the placeholder with the actual SQL query

    # Example query (modify according to your database schema):
    query = f"""
        SELECT 
            MONTHS.month_number AS month,
            COALESCE(SUM(expenditure.Amount), 0) AS total_expenditure,
            COALESCE(SUM(purchase.Price), 0) AS total_purchase
        FROM 
            (SELECT 1 AS month_number
             UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
             UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12) AS MONTHS
        LEFT JOIN 
            expenditure ON MONTHS.month_number = MONTH(expenditure.DOB) AND YEAR(expenditure.DOB) = {selectedYear} AND expenditure.Site = {sitenum}
        LEFT JOIN 
            purchase ON MONTHS.month_number = MONTH(purchase.DOB) AND YEAR(purchase.DOB) = {selectedYear} AND purchase.Site = {sitenum}
        GROUP BY 
            MONTHS.month_number
        ORDER BY 
            month;
    """

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    chart_data = cursor.fetchall()

    # Process the data into a format suitable for the chart
    expenditure_data = {entry['month']: entry['total_expenditure'] for entry in chart_data}
    purchase_data = {entry['month']: entry['total_purchase'] for entry in chart_data}

    return jsonify({'expenditure': expenditure_data, 'purchase': purchase_data})


'''
@app.route('/get_chart_data/<selectedYear>', methods=['GET'])
def get_chart_data(selectedYear):
    # Execute your query to fetch chart data based on the selected year
    # ...

    # For demonstration purposes, I'll provide sample data
    expenditure_data = {'January': 500, 'February': 700, 'March': 900, 'April': 300, 'May': 600, 'June': 800, 'July': 400, 'August': 100, 'September': 300, 'October': 500, 'November': 700, 'December': 900}
    purchase_data = {'January': 200, 'February': 400, 'March': 600, 'April': 800, 'May': 1000, 'June': 1200, 'July': 1400, 'August': 1600, 'September': 1800, 'October': 2000, 'November': 2200, 'December': 2400}

    chart_data = {'expenditure': expenditure_data, 'purchase': purchase_data}

    return jsonify(chart_data)
'''
@app.route('/m_get_chart_data/<selectedYear>')
def m_get_chart_data(selectedYear):
    # Query database to get expenditure and purchase data for the selected year
    # Use the SQL query you provided earlier to retrieve the data
    # Replace the placeholder with the actual SQL query

    # Example query (modify according to your database schema):
    query = f"""
        SELECT 
            MONTHS.month_number AS month,
            COALESCE(SUM(expenditure.Amount), 0) AS total_expenditure,
            COALESCE(SUM(purchase.Price), 0) AS total_purchase
        FROM 
            (SELECT 1 AS month_number
             UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6
             UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12) AS MONTHS
        LEFT JOIN 
            expenditure ON MONTHS.month_number = MONTH(expenditure.DOB) AND YEAR(expenditure.DOB) = {selectedYear} AND expenditure.Site = {sitenum}
        LEFT JOIN 
            purchase ON MONTHS.month_number = MONTH(purchase.DOB) AND YEAR(purchase.DOB) = {selectedYear} AND purchase.Site = {sitenum}
        GROUP BY 
            MONTHS.month_number
        ORDER BY 
            month;
    """

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    chart_data = cursor.fetchall()

    # Process the data into a format suitable for the chart
    expenditure_data = {entry['month']: entry['total_expenditure'] for entry in chart_data}
    purchase_data = {entry['month']: entry['total_purchase'] for entry in chart_data}

    return jsonify({'expenditure': expenditure_data, 'purchase': purchase_data})

@app.route('/m_graph_data')
def m_graph_data():
    return render_template('m_graph_data.html', Site=sitenum)

@app.route('/d_graph_data')
def d_graph_data():
    return render_template('d_graph_data.html')

@app.route('/m_calendar')
def m_calendar():
    return render_template('m_calendar.html')

@app.route('/m_calendar_events')
def m_calendar_events():
    global sitenum
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT date,
       SUM(total_amount_expenditure) AS total_amount_expenditure,
       SUM(total_amount_purchase) AS total_amount_purchase
FROM (
    SELECT DOB AS date,
           SUM(Amount) AS total_amount_expenditure,
           0 AS total_amount_purchase
    FROM expenditure
    WHERE Site = %s
    GROUP BY DOB
    UNION ALL
    SELECT DOB AS date,
           0 AS total_amount_expenditure,
           SUM(Price) AS total_amount_purchase
    FROM purchase
    WHERE Site = %s
    GROUP BY DOB
) AS combined_data
GROUP BY date''', (sitenum, sitenum))
    m_calendar = cursor.fetchall()
    return jsonify(m_calendar)

#d_calendar
@app.route('/calendar')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT DISTINCT Site as site_number FROM expenditure")
    sites = cursor.fetchall()
    return render_template('calendar.html', sites=sites)

@app.route('/calendar_events/<site_number>')
def calendar_events(site_number):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT date,
       SUM(total_amount_expenditure) AS total_amount_expenditure,
       SUM(total_amount_purchase) AS total_amount_purchase
FROM (
    SELECT DOB AS date,
           SUM(Amount) AS total_amount_expenditure,
           0 AS total_amount_purchase
    FROM expenditure
    WHERE Site = %s
    GROUP BY DOB
    UNION ALL
    SELECT DOB AS date,
           0 AS total_amount_expenditure,
           SUM(Price) AS total_amount_purchase
    FROM purchase
    WHERE Site = %s
    GROUP BY DOB
) AS combined_data
GROUP BY date''', (site_number, site_number))
    calendar = cursor.fetchall()
    return jsonify(calendar)

@app.route('/streamlit')
def streamlit():
    st.set_page_config(page_title="My Streamlit App")
if __name__ == '__main__':
    app.run(debug=True)
