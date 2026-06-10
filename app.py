from flask import *
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
# initalize the app
app = Flask (__name__)

ROLES = ['admin', 'supplier', 'customer']

# DATABASE CONNECTION
def get_connection():
    return pymysql.connect(host="localhost", user="root", password="", database="phamarcy_management",cursorclass=pymysql.cursors.DictCursor)


# define your route/endpoint
@app.route("/api/register" , methods=["POST"])
# define function to register
def register():
    fullname = request.form["fullname"]
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    # validate if its correct role inserted
    if role not in ROLES :
        return jsonify({ "message" : "Role not allowed" }), 400
    # connection to database
    connection = get_connection()
    # define cursor
    cursor = connection.cursor()
    # check if email exist and avoid dublicate emails
    sql = "select * from users where email = %s"
    data= (email , )
    # execute/run query
    cursor.execute(sql, data)

    if cursor.fetchone() :
        return jsonify({ "message" : "Email already exists!" }) , 400
    

    # After checking, now we can insert the user to database
    sql1 = "insert into users (fullname, email, password, role) values(%s, %s, %s, %s)"
    data1 = (fullname, email, generate_password_hash(password), role)
    # execute/run query
    cursor.execute(sql1, data1)

    # commit/save changes
    connection.commit()


    return jsonify({ "message" :"user registered successfully" })


# login
@app.route("/api/login", methods = ["POST"] )
# define the function
def login() :
    email = request.form["email"]
    password = request.form["password"]
    # define connection to database
    connection = get_connection()
    # define the cursor
    cursor = connection.cursor()
    sql = "select * from users where email = %s"
    data = (email, )
    # execute/run query
    cursor.execute(sql, data)
    # fetch user with the email if it exist
    user = cursor.fetchone()
    if not user :
        return jsonify({ "message" : "User does not exist" })
    if not check_password_hash(user["password"] , password) :
        return jsonify({"message" : "Invalid email or password" })
    # if email and password correct
    return jsonify({ "message" : "Login successful" , "user" : user})
# fetch all the users
@app.route("/api/users")
# define the function
def users():
    # connection to database
    connection = get_connection()
    # edfine the cursor
    cursor = connection.cursor()
    sql = "select * from users"
    # execute/run query
    cursor.execute(sql)
    # fetch all users
    users = cursor.fetchall()
    return jsonify(users)

# run the app
app.run(debug=True)
