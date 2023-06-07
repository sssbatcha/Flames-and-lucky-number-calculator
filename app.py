from flask import Flask, render_template, request
from flask import Flask,request, render_template,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_DB']= "flames"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "python"
app.config['MYSQL_CURSORCLASS']="DictCursor"
app.secret_key="myapp"

conn = MySQL(app)

@app.route('/', methods = ['POST', 'GET'])
def signin():
    if request.method  == 'POST':
        user_name1 = request.form['user_name']
        password1 = request.form['password']
        con=conn.connection.cursor()
        sql = "select user_name, password from signup WHERE user_name= %s and  password=%s"
        result=con.execute(sql,(user_name1,password1))
        con.connection.commit()
        con.close()
        
        if result:
            return render_template('medium.html')
        else:
            error_message = "Invalid username or password"
            return render_template('login.html', error_message=error_message)
            
        
    return render_template('login.html')

@app.route('/index', methods = ['POST', 'GET'])
def index():
    if request.method  == 'POST':
        name1 = request.form['name1']
        name2 = request.form['name2']
        con=conn.connection.cursor()
        sql = "insert into names(name1,name2) values  (%s,%s)"
        result=con.execute(sql,(name1,name2))
        con.connection.commit()
        con.close()
        return render_template('result.html')
    return render_template('index.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method  == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']
        password = request.form['password']
        email= request.form['email']
        age = request.form['age']
        mobile = request.form['mobile']
        gender = request.form['gender']
        con=conn.connection.cursor()
        sql = "insert into signup(first_name,last_name,user_name,password,email,age,mobile,gender) values  (%s,%s,%s,%s,%s,%s,%s,%s)"
        result=con.execute(sql,(first_name,last_name,user_name,password,email,age,mobile,gender))
        con.connection.commit()
        con.close()
        return  redirect(url_for('signin'))
        
    return render_template('signup.html')



@app.route('/result', methods=['POST'])
def result():
    name1 = request.form['name1'].lower()
    name2 = request.form['name2'].lower()
    if request.method  == 'POST':
        name1 = request.form['name1']
        name2 = request.form['name2']
        con=conn.connection.cursor()
        sql = "insert into names(name1,name2) values  (%s,%s)"
        result=con.execute(sql,(name1,name2))
        


    # Remove common characters
    for char in name1:
        if char in name2:
            name1 = name1.replace(char, '', 1)
            name2 = name2.replace(char, '', 1)

    # Count remaining characters
    count = len(name1) + len(name2)

    # Mapping of FLAMES result
    flames = {
        0: 'Friends',
        1: 'Lovers',
        2: 'Affection',
        3: 'Marriage',
        4: 'Enemies',
        5: 'Siblings'
    }

    # Calculate the FLAMES result
    result = flames[count % 6]
    data = request.form.get('data')  # Assuming the data is sent in a form field named 'data'
    
    con=conn.connection.cursor()
    sql = "INSERT INTO names (result) VALUES (%s) "
    values = (result,)

    con.execute(sql, values)
    con.connection.commit()
    con.close()
    

    return render_template('result.html', name1=name1.capitalize(), name2=name2.capitalize(), result=result)





@app.route('/luck', methods=['GET', 'POST'])
def luck():
    if request.method == 'POST':
        con=conn.connection.cursor()
        dob = request.form['dob']
        lucky_number = calculate_lucky_number(dob)
        sql = "insert into luck(dob) values  (%s)"
        result=con.execute(sql,(dob,))
        con.connection.commit()
        return render_template('result2.html', dob=dob, lucky_number=lucky_number)
    return render_template('luck.html')
def calculate_lucky_number(dob):
    """Calculate the lucky number based on the date of birth."""
    # Remove any dashes from the DOB string
    dob = dob.replace('-', '')

    # Sum all the digits in the DOB
    lucky_number = sum(int(digit) for digit in dob)

    # Keep reducing the sum until it becomes a single digit
    while lucky_number > 9:
        lucky_number = sum(int(digit) for digit in str(lucky_number))
        data = request.form.get('data')  # Assuming the data is sent in a form field named 'data'
    
    con=conn.connection.cursor()
    sql = "INSERT INTO luck(lucky_number) VALUES (%s) "
    values = (result,)

    con.execute(sql, (lucky_number,))
    con.connection.commit()
    con.close()
    return lucky_number
if __name__ == '__main__':
    app.run(debug=True)