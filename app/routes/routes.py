from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db

main_bp = Blueprint('main', __name__)

products = [{"id": i, "name": f"Product {i+1}", "price": (i + 1) * 10} for i in range(20)]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please log in.', 'warning')
            return redirect(url_for('main.login'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('main.products_page'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

@main_bp.route('/products')
def products_page():
    if 'user' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('main.login'))

    return render_template('products.html', products=products)

@main_bp.route('/cart', methods=['POST'])
def cart():
    if 'user' not in session:
        flash('Please log in to access the cart.', 'warning')
        return redirect(url_for('main.login'))

    item_id = int(request.form['item_id'])
    flash(f'Product {item_id + 1} added to the cart.', 'success')
    return redirect(url_for('main.products_page'))

@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
