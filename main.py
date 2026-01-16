from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from pyexpat.errors import messages
from sqlalchemy.orm import DeclarativeBase, relationship
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from unicodedata import category
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import os
from datetime import datetime



class Base(DeclarativeBase):
    pass


login_manager = LoginManager()
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)
login_manager.init_app(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    products = relationship("Products", back_populates="author")
    cart = relationship('Cart', back_populates='user')
    whatsapp_no = db.Column(db.String(15))
    account_no = db.Column(db.String(25))


class Products(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(20), nullable=False)
    no_in_stock = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = relationship("User", back_populates="products")
    cart = relationship('Cart',back_populates='products')
    reviews = db.Column(db.String(200))
    rating = db.Column(db.String(50))
    img_url = db.Column(db.String(300),nullable=False)

class Cart(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = relationship('User',back_populates='cart')
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'))
    products = relationship('Products', back_populates='cart')


with app.app_context():
    db.create_all()

@app.context_processor
def inject_now():
    return {'now':datetime.now()}

@app.context_processor
def get_cart_no():
    if current_user.is_authenticated:
        return {'cart_no':len(current_user.cart)}
    return {'cart_no': 0}

def get_discounted_price(discount:int,price:str) -> str:
    raw_price = float(price.replace('$',''))
    discounted_price = ((100 - discount)/100) * raw_price
    return f"${discounted_price:.2f}"

@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
    if user:
        return user
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    all_products = Products.query.all()
    return render_template("products.html",products=all_products,get_discounted_price=get_discounted_price)


@app.route("/product/<int:product_id>", methods=['POST','GET'])
def product(product_id):
    specific_product = Products.query.where(Products.id == product_id).scalar()
    return render_template("product.html",specific_product=specific_product)


@app.route("/login", methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if request.method == "POST":
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash("Login successful", category="Success")
                return redirect(url_for('home'))
            flash("Invalid Password. Please input the correct password")
            return redirect(url_for('login'))
        flash("Invalid Email. Please this email is not registered. Input a registered email.")
        return redirect(url_for('login'))
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    email = request.form.get("email")
    name = request.form.get("name")
    print(messages)
    password = request.form.get("password")
    if request.method == "POST":
        hashed_password = bcrypt.generate_password_hash(password=password, rounds=16)
        already_a_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if already_a_user:
            flash("This user is already registered, please try loging in")
            return redirect(url_for('login'))
        else:
            with app.app_context():
                new_user = User(name=name, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            return redirect(url_for('home'))
    return render_template('signup.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/merchant-signup', methods=['POST','GET'])
def merchant_signup():
    whatsapp_no = request.form.get('whatsapp_no')
    account_no = request.form.get('account_no')
    if request.method == 'POST':
        with app.app_context():
            current_user.whatsapp_no = whatsapp_no
            current_user.account_no = account_no
            db.session.commit()
        return redirect(url_for('add_products'))
    return render_template('merchant-signup.html')


@app.route('/add-products', methods=['POST', 'GET'])
def add_products():
    product_name = request.form.get('product_name')
    product_category = request.form.get("category")
    price = request.form.get("price")
    discount = request.form.get('discount')
    description = request.form.get('description')
    amount_in_stock = request.form.get('instock')
    img_url = request.form.get('img_url')
    if current_user.whatsapp_no is None:
        return redirect(url_for('merchant_signup'))
    if request.method == 'POST':
        with app.app_context():
            new_product = Products(
                name=product_name,
                price=price,
                category=product_category,
                description=description,
                discount=discount,
                no_in_stock=amount_in_stock,
                img_url=img_url,
                author=current_user,
            )
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('products'))
    return render_template("add-products.html")

@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete(id):
    delete_product = Products.query.where(Products.id == id).scalar()
    db.session.delete(delete_product)
    db.session.commit()
    return redirect(url_for('products'))
@app.route("/cart")
@login_required
def cart():
    return render_template("cart.html")

@app.route('/add_to_cart/<int:id>',methods=['POST','GET'])
def add_to_cart(id):
    product_added = Products.query.where(Products.id == id).scalar()
    product_to_add = Cart(products=product_added,user=current_user)
    db.session.add(product_to_add)
    db.session.commit()
    return redirect(url_for('cart'))
@app.route('/edit-product/<int:product_id>', methods=['POST','GET'])
def edit(product_id):
    edit_product = Products.query.where(Products.id == product_id).scalar()
    product_name = request.form.get('product_name')
    product_category = request.form.get("category")
    price = request.form.get("price")
    discount = request.form.get('discount')
    description = request.form.get('description')
    amount_in_stock = request.form.get('instock')
    img_url = request.form.get('img_url')
    if current_user.whatsapp_no is None:
        return redirect(url_for('merchant_signup'))
    if request.method == 'POST':
        with app.app_context():
            edited_product = Products.query.where(Products.id == product_id).scalar()
            edited_product.name = product_name
            edited_product.category =product_category
            edited_product.price = price
            edited_product.discount = discount
            edited_product.description = description
            edited_product.no_in_stock = amount_in_stock
            edited_product.img_url = img_url
            db.session.commit()
        return redirect(url_for('products'))
    return render_template('edit-product.html',edit_product=edit_product)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
