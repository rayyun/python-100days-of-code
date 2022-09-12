# Day96-Professional Portfolio Project 16 : Online Shop

from bs4 import BeautifulSoup
import bs4
import requests
import csv
import cssutils
import tinycss
from tinycss.css21 import CSS21Parser
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.orm import relationship
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from forms import RegisterForm, LoginForm, AddressForm
from flask_gravatar import Gravatar
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import random
from datetime import date
import upload_items
from werkzeug.security import generate_password_hash, check_password_hash


import json
import os
import stripe



BASE_URL = "https://www.leonandgeorge.com"

stripe.api_key = os.environ.get('STRIPE_API_KEY')

app = Flask(__name__)
Bootstrap(app)

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plantshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
db = SQLAlchemy(app)


# For login
login_manager = LoginManager()
login_manager.init_app(app)


##CONFIGURE TABLES
# Product TABLE Configuration
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    short_detail = db.Column(db.Text, nullable=False)
    long_detail = db.Column(db.Text, nullable=False)
    img_sm_url = db.Column(db.String(500), nullable=False)
    img_md_url = db.Column(db.String(500), nullable=False)
    img_lg_url = db.Column(db.String(500), nullable=False)
    org_item_url = db.Column(db.String(250), nullable=False)
    shop = db.Column(db.String(1), nullable=False)
    createdAt = db.Column(db.String(50), nullable=False)
    updatedAt = db.Column(db.String(50), nullable=False)
    publishedAt = db.Column(db.String(50))

    cart_item = relationship("CartItem", back_populates="product")


# User TABLE Configuration
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.String(1), nullable=False)
    vendor = db.Column(db.String(1), nullable=False)
    registeredAt = db.Column(db.String(50), nullable=False)
    lastLogin = db.Column(db.String(50), nullable=False)

    cart = relationship("Cart", back_populates="cart_user")
    address = relationship("UserAddress", back_populates="user")


# User-Address TABLE Configuration
class UserAddress(UserMixin, db.Model):
    __tablename__ = "user_address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    street_1 = db.Column(db.String(50), nullable=False)
    street_2 = db.Column(db.String(50))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    user = relationship("User", back_populates="address")


# Cart TABLE Configuration
class Cart(UserMixin, db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.String(50), nullable=False)
    updatedAt = db.Column(db.String(50), nullable=False)

    cart_user = relationship("User", back_populates="cart")
    cart_item = relationship("CartItem", back_populates="cart")


# CartItem TABLE Configuration
class CartItem(UserMixin, db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    product_id =  db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), nullable=False)
    createdAt = db.Column(db.String(50), nullable=False)
    updatedAt = db.Column(db.String(50), nullable=False)

    product = relationship("Product", back_populates="cart_item")
    cart = relationship("Cart", back_populates="cart_item")


# Order TABLE Configuration
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)

    #Create Foreign Key, "user.id" the users refers to the tablename of User.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(db.String(10), nullable=False)
    sub_total = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    shipping = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    billing_address_id = db.Column(db.Integer, db.ForeignKey("user_address.id"))
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("user_address.id"))


# OrderItems TABLE Configuration
class OrderItem(db.Model):
    __tablename__ = "order_item"
    id = db.Column(db.Integer, primary_key=True)

    #Create Foreign Key, "users.id" the users refers to the tablename of User.
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.String(50), nullable=False)
    updatedAt = db.Column(db.String(50), nullable=False)


db.create_all()



# #######################################
# #### Just execute once at first
# #### bulk uploap product items
# #######################################
#
# upload_items.bulk_upload(db, Product)


def get_today():
    return date.today().strftime("%m-%d-%Y %H:%M:%S")


@app.route("/")
def home():
    # items = db.session.query(Product).all()
    items = db.session.query(Product).filter_by(shop="T").all()

    return render_template("index.html", all_items=items)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        # if email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))

        # password incorrect
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))

        else:
            login_user(user)
            return redirect(url_for("home"))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/sign-up/<string:user_type>', methods=["GET", "POST"])
def register(user_type):
    form = RegisterForm()
    admin, vendor = 'F', 'F'

    if user_type == 'admin':
        admin = 'T'
    elif user_type == 'vendor':
        vendor = 'T'

    if form.validate_on_submit():

        # print(form.email.data)
        # print(form.password.data)
        # print(form.first_name.data)
        # print(form.last_name.data)

        # If user's email already exists
        if User.query.filter_by(email=form.email.data).first():
            # Send flash message
            flash("You've already signed up with that email. Log in instead!")

            return redirect(url_for("login"))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        # today_date = get_today()

        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            admin=admin,
            vendor=vendor,
            registeredAt=get_today(),
            lastLogin=get_today()
         )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route("/item-detail/<int:item_id>")
def item_detail(item_id):
    # item = db.session.query(Product).get(item_id)
    item = Product.query.get(item_id)

    return render_template("item_detail2.html", item=item)


@app.route("/show-cart", methods=["GET", "POST"])
def show_cart():
    # today_date = get_today()

    if not current_user or not current_user.is_authenticated:
        flash("You need to login or register!")
        return redirect(url_for("login"))

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart_id = cart.id
        # print(cart.id)
        # print(cart.user_id)

    else:
        cart_id = None

    if request.method == "POST":
        data = request.form

        if data['action'] == 'add':

            if not cart:
                new_cart = Cart(
                    user_id=current_user.id,
                    type='active',
                    status='active',
                    createdAt=get_today(),
                    updatedAt=get_today()
                )

                db.session.add(new_cart)
                db.session.commit()

                cart = Cart.query.filter_by(user_id=current_user.id).first()
                cart_id = cart.id

            else:
                # cart_id = cart.id
                cart.updatedAt = get_today()
                db.session.commit()

            cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=data['product_id']).first()

            if not cart_item:
                new_cart_item = CartItem(
                    cart_id=cart.id,
                    product_id=int(data["product_id"]),
                    quantity=int(data["quantity"]),
                    status=data["status"],
                    createdAt=get_today(),
                    updatedAt=get_today()
                )

                db.session.add(new_cart_item)
                db.session.commit()
            else:
                # cart_item.price = float(data["price"])
                # cart_item.discount = float(data["discount"])
                cart_item.quantity += int(data["quantity"])
                cart_item.status = data["status"]
                cart_item.updatedAt = get_today()

                db.session.commit()

        else:
            switch_status = ('saved', 'active')

            if data['action'] == 'delete':
                print('Delete - ', data['delete_id'])
                item_to_delete = CartItem.query.get(data['delete_id'])
                db.session.delete(item_to_delete)

            elif data['action'] in switch_status:
                print(f"{data['action']} - {data['update_id']}")
                item_to_switch_status = CartItem.query.get(data['update_id'])
                item_to_switch_status.quantity = 1
                item_to_switch_status.status = data['action']
                item_to_switch_status.updateAt = get_today()

            elif data['action'] == 'update':
                print(f"Update quantity to {data['quantity']} - {data['update_id']}")
                item_to_update = CartItem.query.get(data['update_id'])
                item_to_update.quantity = int(data['quantity'])
                item_to_update.updateAt = get_today()

            cart = Cart.query.filter_by(id=data['cart_id']).first()
            cart.updateAt = get_today()

            db.session.commit()




        return redirect(url_for("show_cart"))

    # print("cart_id - ", cart_id)


    # cart_list = db.session.query(CartItem, Product).join(Product).filter(CartItem.cart_id == cart.id).filter(CartItem.status == 'active').filter(CartItem.product_id == Product.id).all()
    # saved_list = db.session.query(CartItem, Product).join(Product).filter(CartItem.cart_id == cart.id).filter(CartItem.status == 'saved').filter(CartItem.product_id == Product.id).all()


    ##### join query
    # cart_list = db.session.query(CartItem, Product).filter(CartItem.cart_id == cart.id).filter(CartItem.status == 'active').filter(CartItem.product_id == Product.id).all()
    # saved_list = db.session.query(CartItem, Product).filter(CartItem.cart_id == cart.id).filter(CartItem.status == 'saved').filter(CartItem.product_id == Product.id).all()


    cart_list = CartItem.query.filter_by(cart_id=cart_id, status='active').order_by(desc(CartItem.id)).all()
    saved_list = CartItem.query.filter_by(cart_id=cart_id, status='saved').order_by(desc(CartItem.id)).all()



    # print(cart_list)

    return render_template("cart.html", cart_list=cart_list, saved_list=saved_list)


@app.route("/order", methods=["GET", "POST"])
def order_items():
    if not current_user or not current_user.is_authenticated:
        flash("You need to login or register!")
        return redirect(url_for("login"))

    form = AddressForm()

    # cart = Cart.query.filter_by(user_id=current_user.id).first()


    cart_id = request.args['cart_id']
    # print(cart_id)

    cart_list = CartItem.query.filter_by(cart_id=cart_id, status='active').order_by(desc(CartItem.id)).all()

    # return render_template("order.html", cart_list=cart_list)
    return render_template("checkout.html", form=form, cart_list=cart_list, current_user=current_user)




#     data = request.form
    #     print(current_user.id)
    #     print(data["product_id"])
    #     print(data["price"])
    #     print(data["discount"])
    #     print(data["quantity"])
    #
    # return render_template("cart.html")


# @app.route("/show-cart/<int:cart_id>", methods=["GET", "POST"])
# def show_cart(cart_id):
#     return render_template("cart.html", cart_id=cart_id)



def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/checkout')
def checkout():
    # data = request.
    # intent = #
    # return render_template("checkout-org.html" , client_secret=intent.client_secret)
    return render_template("checkout.html")


@app.route('/success')
def transaction_success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)