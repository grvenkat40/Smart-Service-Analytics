from flask import Flask, render_template, redirect, flash, url_for, session, request
import sqlite3

app=Flask(__name__)
app.secret_key = 'aS3cr3t!Key#789@dev'  # Good enough for local testing

import sqlite3

def init_db():
    conn = sqlite3.connect("database\Database.db")
    cursor = conn.cursor()
    
    # Create user table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_name TEXT NOT NULL,
            Mail TEXT NOT NULL,
            Password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
init_db()

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        with sqlite3.connect(r'database/Database.db') as conn:
            cursor = conn.cursor()
            get_query='SELECT * FROM user where Mail=? and Password=?'
            value=(email,password)
            cursor.execute(get_query,value)
            user_there = cursor.fetchone()

            if user_there:
                session['username'] = username
                flash('Login Success ✅')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalied details, Please register ❌👇')
                return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            with sqlite3.connect('database/Database.db') as conn:
                cursor = conn.cursor()
                insert_query='INSERT INTO user(User_name,Mail,Password) VALUES (?,?,?)'
                cursor.execute(insert_query,(username,email,password))
                conn.commit()
                flash(f'{username} Registerd success 🤝')
                return redirect(url_for('login'))
        except Exception as e:
            flash(f'{e} 👾')
        finally:
            cursor.close()
    return render_template('register.html')


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html',username=session['username'])
    else:
        flash('Please login first ⏰')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.❗')
    return redirect(url_for('login'))

if __name__ =='__main__':
    app.run(debug=True)