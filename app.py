from multiprocessing.dummy import active_children
import re
from flask import Flask, render_template, redirect, session,request,flash, url_for
from datetime import timedelta
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functions import check_if_active
from models import *
import smtplib
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename


##constants##
PORT = 4000
DB_FILENAME = 'database.db'
INIT_DB = True  # to create db file

def create_app():
    app = Flask(__name__)
    #profile_pic
    UPLOAD_FOLDER = 'static/images/Face image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #national_id
    UPLOADER_FOLDER = 'static/images/national id'
    app.config['UPLOADER_FOLDER'] = UPLOADER_FOLDER
    #national_id2
    app.secret_key = 'asdfads234egrg'
    app.permanent_session_lifetime = timedelta(minutes=5)


    # create database extension
    app.config['SQLALCHEMY_DATABASE_URI'] = ' postgres://sijdwycapytyfq:4c87c53f4aa45a43c75f2b59c4ef7ecabc5d4b93ec7712b0abcf19fd6c4ced96@ec2-52-207-90-231.compute-1.amazonaws.com:5432/d43nhqsi9g3ar7'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    

    db.init_app(app)

    # create flask cors extension
    CORS(app)

    return app, db
    
#to upload image
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
app = Flask(__name__)
mail= Mail(app)
# to send email gmail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'moustafasamy490@gmail.com'
app.config['MAIL_PASSWORD'] = 'twuhuyqcjijywwqx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app = Flask(__name__)


# create flask app
app, db = create_app()

# create db file on demand
if INIT_DB:
    db.create_all(app=app)


#routes
#home page
@app.route('/')
@app.route('/home')
def index():
    if 'username' in session:
        if not( check_if_active()):
            return render_template('main.html' , active_value = "Flase")
        else:
            return render_template('main.html' , active_value = "True")
    else:
            return render_template('main.html' , active_value = "False")
   
@app.route('/admin')
def admin_page():
    if "admin" in session:
        return render_template('admin.html')
    else:
        return redirect("/login_admin")

@app.route('/create_account')
def create_account():
    return render_template('creat account.html')

@app.route('/create_account' ,  methods=['POST'])
def POST_create_account():
     # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_pic = filename
        #national_id face

        file = request.files['files']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADER_FOLDER'], filename))
            national_id_face = filename
            #national_id_back
            

        file = request.files['filess']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADER_FOLDER'], filename))
            national_id_back = filename

        username = request.form['username']
        email = request.form['email']
        query1 = Castomers.getByUsername(username)
        query2 = Castomers.getByEmail(email)
        if (query1 == None) and (query2 == None):
            username_ok = username
            email_ok = email
            isactivated = False
            castomers=Castomers( request.form['name'],username_ok,request.form['phone'],email_ok,request.form['Password'] , profile_pic , national_id_face , national_id_back , isactivated = isactivated)
            db.session.add(castomers)
            db.session.commit()

#message to admin to notifi new registration ##
     
    #######
            message = "there is a new registration"
            msg = Message("there is a new registration from  %s " % (username), sender = 'moustafasamy490@gmail.com', recipients = ["moustafasamy490@gmail.com"])
            msg.body = message 
            mail.send(msg)

            return "account created"
        else:
            return"sorry the email  already exist in "

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login' , methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    query = Castomers.getByUsername(username)
    if query == None :
        return "<h1>wrong username</h1>"
    if query.password != password:
        # @TODO return a proper failure message
        return "<h1>wrong password</h1>"

    # save session
    print("LOGIN success")
    session.permanent = True
    session['username'] = username
    session['username'] = True
    

    if query.isactivated:
        session["isactivated"] = True
    else:
        session["isactivated"] = False
    return redirect('/')
@app.route('/buy', methods=['GET'] )
def GT_BUY_PAG():
    if not( check_if_active()):
        return "<h1>YOUR account is not acive</h1>"
    else:
        return render_template('buy.html')


@app.route('/buy' , methods=['POST'])
def POST_BUY_PAG():
    #check if active
    if not( check_if_active()):
        return "<h1>YOUR Account is not active</h1>"
    ####
    username = session['username']
    #####
    email = request.form['e_seller']

    query = Castomers.getByEmail(email)
    if query == None :
        return "<h1>email not exist in </h1>"
    #######

    mesg = Message("New session request from  %s " % (username), sender = 'moustafasamy490@gmail.com', recipients = ['moustafasamy490@gmail.com'])
    mesg.body = message 
    mail.send(mesg)




    message = request.form['order']
    msg = Message("New session request from  %s " % (username), sender = 'moustafasamy490@gmail.com', recipients = [email])
    msg.body = message 
    mail.send(msg)
    return "We Receved your message please tell the seller to contact me"

@app.route('/sell' )
def GT_SELL_PAG():
    if not( check_if_active()):
        return "<h1>YOUR account is not acive</h1>"
    else:
        return render_template('sell.html')




@app.route('/sell' , methods=['POST'])
def POST_SELL_PAG():
    if not( check_if_active()):
        return "<h1>YOUR account is not acive</h1>"
    else:
        username = session['username']
    #####
        email = request.form['e_seller']

        query = Castomers.getByEmail(email)
        if query == None :
            return "<h1>email not exist in </h1>"
    #######    
        message = request.form['order']
        msg = Message("New session request from  %s " % (username), sender = 'moustafasamy490@gmail.com', recipients = [email])

#####mail me #############

        mesg = Message("New session request from  %s " % (username), sender = 'moustafasamy490@gmail.com', recipients = ['moustafasamy490@gmail.com'])
        mesg.body = message 
        mail.send(mesg)


        msg.body = message 
        mail.send(msg)
        return "We Receved your message please tell the seller to contact me"


##### admin panal from here #########
@app.route('/admin/dashboard/usersinfo')
def admin_users_info():
    if "admin" in session:
        users = Castomers.query.all()

        return render_template('users_info.html' , users = users)
    else:
        return redirect ("/login_admin")

@app.route("/admin/account/ac/<id>/edit" , methods=['GET'])
def get_active_page(id):
    if "admin" in session:
        isactivated = Castomers.get(id).isactivated
        return render_template('active_acc.html' , isactivated = isactivated  , id = id)
    else:
        return redirect('/login_admin')



@app.route('/admin/account/ac/<id>/edit', methods=['POST'])
def update_activation(id):
    if "admin" in session:
        isactivated = request.form.get('isactivated')
        Castomers.update_active_value(id, isactivated)
        return redirect('/admin/dashboard/usersinfo' )
    else:
        # user is not logged in --> redirect to login page
        return redirect('/login_admin')










@app.route('/login_admin')
def login_admin():
    return render_template('login-admin.html')


@app.route('/login_admin' , methods=['POST'])
def login_admin_post():
    username = request.form.get('username')
    password = request.form.get('password')

    query = Admin.getByUsername(username)
    if query == None :
        return "<h1>wrong username</h1>"
    if query.password != password:
        # @TODO return a proper failure message
        return "<h1>wrong password</h1>"

    # save session
    print("LOGIN success")
    session.permanent = True
    session['admin'] = username
    session['admin'] = True
    
    return redirect('/admin')






if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')

