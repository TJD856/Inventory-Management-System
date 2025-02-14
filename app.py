import random
import string
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import bcrypt
import subprocess
import threading
import io
import time
from PIL import Image, ImageDraw, ImageFont
from flask import send_file

# Flask Setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Setup
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'lol1'
mysql = MySQL(app)

# GUI Thread Management
gui_threads = {}

def run_gui(script_path):
    """Run a GUI script in a separate thread."""
    subprocess.run(["python", script_path])

def start_gui_thread(name, script_path):
    """Start a GUI thread dynamically if not already running."""
    global gui_threads
    if name not in gui_threads or not gui_threads[name].is_alive():
        print(f"Starting GUI thread for {name}...")  # Add logging here
        gui_threads[name] = threading.Thread(target=run_gui, args=(script_path,), daemon=True)
        gui_threads[name].start()
    else:
        print(f"GUI thread for {name} is already running.")


# CAPTCHA generation and image rendering
def generate_captcha():
    captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return captcha_code

def generate_captcha_image(captcha_code):
    image = Image.new('RGB', (200, 80), color=(255, 255, 255))
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    draw.text((50, 25), captcha_code, font=font, fill=(0, 0, 0))
    
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route('/captcha')
def captcha():
    captcha_code = generate_captcha()
    session['captcha_code'] = captcha_code
    img_io = generate_captcha_image(captcha_code)
    return send_file(img_io, mimetype='image/png')

def get_low_stock_products():
    """Fetch products with stock less than 10."""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, stock FROM products WHERE stock < 10")
    low_stock_items = cursor.fetchall()
    cursor.close()
    return low_stock_items


@app.route('/')
def index():
    if 'username' in session:
        low_stock_items = get_low_stock_products()
        return render_template('index.html', username=session['username'], low_stock_items=low_stock_items)
    flash('Please log in to access the dashboard.', 'info')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        entered_captcha = request.form.get('captcha')

        if entered_captcha != session.get('captcha_code'):
            flash('Invalid CAPTCHA. Please try again.', 'error')
            return redirect(url_for('login'))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            session['username'] = username
            flash('Login successful!', 'success')
            # Start the dashboard GUI (adjust the script name if needed)
            start_gui_thread('dashboard', 'dashboard_gui.py')  # Make sure this script exists and works
            time.sleep(2)  # Wait for 2 seconds to give the thread time to start
            return redirect(url_for('index'))  # Redirect to the dashboard or index page
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists.", 'error')
            return redirect(url_for('signup'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
        mysql.connection.commit()
        cursor.close()

        flash("Sign up successful!", 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/employees')
def employees():
    if 'username' in session:
        start_gui_thread('employees', "employee_gui.py")
        return redirect(url_for('index'))
    flash('Please log in.', 'info')
    return redirect(url_for('login'))

@app.route('/sales')
def sales():
    if 'username' in session:
        start_gui_thread('sales', "sales_gui.py")
        return redirect(url_for('index'))
    flash('Please log in.', 'info')
    return redirect(url_for('login'))

@app.route('/products')
def products():
    if 'username' in session:
        start_gui_thread('products', "product_gui.py")
        low_stock_items = get_low_stock_products()
        return render_template('products.html', low_stock_items=low_stock_items)
    flash('Please log in.', 'info')
    return redirect(url_for('login'))

@app.route('/categories')
def categories():
    if 'username' in session:
        start_gui_thread('categories', "category_gui.py")
        return redirect(url_for('index'))
    flash('Please log in.', 'info')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
