from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import webbrowser
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'kajd8449'  # Session secret key

valid_username = "user"
valid_password = "password"

# Pytop for OTP
def generate_otp():
    totp = pyotp.TOTP('base32secret3232')  # BASE32 encryption 
    otp = totp.now()  
    return otp

# Fake info creater
def generate_fake_data():
    credit_card = f"{random.randint(1000000000000000, 9999999999999999)}"
    credit_card_password = f"{random.randint(1000, 9999)}"
    id_number = f"{random.randint(10000000000, 99999999999)}"
    birth_year = random.randint(1989, 2000)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)  
    birth_date = f"{birth_day:02d}-{birth_month:02d}-{birth_year}"

    fake_data = {
        "credit_card": credit_card,
        "credit_card_password": credit_card_password,
        "id_number": id_number,
        "birth_date": birth_date,
    }
    return fake_data


@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login'))  # Directs to login page


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Checking credentials
        if username == valid_username and password == valid_password:
            # OTP creation
            otp = generate_otp()
            session['otp'] = otp  
            session['username'] = username  
            print(f"Generated OTP: {otp}")  
            return redirect(url_for('otp'))  
        else:
            return render_template('login.html', error="Invalid credentials, please try again.")
    
    return render_template('login.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if 'username' not in session:
        # Direct to login if username is not in session
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp = request.form['otp']
        
        # OTP check
        if otp == session.get('otp'):  
            return redirect(url_for('dashboard'))  # Direct to dashboard
        else:
            return render_template('otp.html', error="Invalid OTP, please try again.")
    
    return render_template('otp.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():

    if 'username' not in session:
        return redirect(url_for('login'))

    fake_data = generate_fake_data()
    return render_template('dashboard.html', fake_data=fake_data)

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')  
    app.run(debug=True, use_reloader=False)
