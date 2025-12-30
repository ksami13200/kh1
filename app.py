# testing the app 
from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from database import get_db_connection, init_db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB (in a real production app, use migration tools)
# For this purpose, we'll just checks/runs schema execution on startup if needed
# But usually best to run manually. We will provide a CLI command.

@app.cli.command('init-db')
def init_db_command():
    init_db()
    print('Initialized the database.')

@app.route('/')
def home():
    conn = get_db_connection()
    testimonials = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM testimonials ORDER BY id DESC LIMIT 3")
        testimonials = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('home.html', testimonials=testimonials)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/shop')
def shop():
    conn = get_db_connection()
    products = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('shop.html', products=products)

@app.route('/blog')
def blog():
    conn = get_db_connection()
    posts = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blog_posts ORDER BY date_posted DESC")
        posts = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('blog.html', posts=posts)

@app.route('/contact', methods=('GET', 'POST'))
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)',
                           (name, email, message))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Database connection failed.', 'danger')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
