from flask import Flask, render_template, g, request, redirect, flash, session, url_for
import sqlite3
import os
app = Flask(__name__)

DATABASE = 'time.db'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home(): #using sessions to store the username, to call back and see if it works
    if 'username' in session: 
        results = f'Logged in as {session["username"]}'
        log = ('enter the medium')
        return render_template("home.html", result=results, log=log)
    return render_template("basic.html")


#this is the upload page you can think of it
@app.route('/account') 
def account():
    if 'username' in session:
        results = f'Logged in as {session["username"]}'
        return render_template("account.html", result=results)
    flash ("an error occured. please retry or log out and log in again")
    return render_template("basic.html")


#this is a layout for the inside of the website. after the login page as those use diffrent styles and layouts
@app.route('/trueHome')
def truehome():
    return render_template("trueHome.html")

#login page
@app.route('/login') 
def login():
    return render_template("login.html")

#register  q
@app.route('/register', methods=["GET","Post"])
def register_function():
    if request.method == "POST":
        cursor = get_db().cursor()
        user_ID = request.form.get("username")
        Email = request.form.get("Email")
        password = request.form.get("password")

        sql = ("INSERT INTO Account(user_ID,mail,password) VALUES (?,?,?)")
        print (user_ID + " user")
        print (Email + " mail") 
        print (password + " pass")
        try:
            cursor.execute(sql,(user_ID,Email,password))
            get_db().commit()
            flash ("User registered, please log in")
            return redirect ("/login")
            
        except:
            flash ("failed to register, username already exists")
        return redirect ("/register")

    return render_template("register.html")



@app.route('/fail')
def fail():
    return render_template("fail.html")




@app.route('/out')
def out():
    if 'username' in session:
        cursor = get_db().cursor()
       #querey of data to import/send to the box thing
        sql = ("SELECT * FROM Image ORDER BY Image_ID DESC") 
        
        cursor.execute(sql)
        
        results = cursor.fetchall() 
        print (results)
        return render_template("out.html", results=results)
    else:
        results = ("Not logged in")

        print ("failed, not logged in")
        return render_template("fail.html", results=results)
    



@app.route('/find', methods=["GET","Post"])  
def login_function():
    if request.method == "POST":
       
        cursor = get_db().cursor()
        user_ID = request.form.get("username")
        password = request.form.get("password")
        find_user = ("SELECT * FROM Account WHERE (user_ID,password) = (?,?)")
        cursor.execute(find_user,(user_ID, password))
        results = cursor.fetchall()       
         
        if len(results) > 0:
             #he have a user in the database with the right password
            session['username'] = request.form['username']
            global user
            user = (results[0][0])
            return redirect ("/out")
        
        else:
            flash ("error, check spelling and caps")
            return redirect ("/login")
            





@app.route('/upload',methods=["GET","Post"])
def upload():
    request.files['file'].save(f'static/uploads/{request.files["file"].filename}')
    if request.method == "POST":
        try:
            
            cursor = get_db().cursor()
            filename = request.files["file"]
            print(filename.filename)    
            User_ID = session["username"]
            print (User_ID)
            sql = ("INSERT INTO Image(filename, User_ID) VALUES (?,?)")
            cursor.execute(sql,(filename.filename,User_ID))
            get_db().commit()
            results = cursor.fetchall() 
            return redirect("/out")
        except:
            flash ("something went wrong. try again with a diffrent image format, png is preferable")
            return render_template("fail.html", results=results)
        return redirect("/out")






@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


