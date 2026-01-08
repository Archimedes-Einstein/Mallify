from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
import os

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:astroworld%4019@localhost/data"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    products = relationship("Products",back_populates="author")

class Products(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(20), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = relationship("User",back_populates="products")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/products")
def products():
    return render_template("products.html")
@app.route("/product")
def product():
    return render_template("product.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/signup")
def signup():
    return render_template('signup.html')
@app.route("/cart")
def cart():
    return render_template("cart.html")
if __name__ == "__main__" :
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)