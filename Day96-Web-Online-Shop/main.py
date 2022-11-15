# Day96-Professional Portfolio Project 16 : Online Shop

# from bs4 import BeautifulSoup
# import bs4
import requests
# import csv
# import cssutils
# import tinycss
# from tinycss.css21 import CSS21Parser
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
from datetime import date, datetime
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
    order_item = relationship("OrderItem", back_populates="product")


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
    status = db.Column(db.String(20), nullable=False)
    sub_total = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    shipping = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    billing_address_id = db.Column(db.Integer, db.ForeignKey("user_address.id"))
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("user_address.id"))
    payment_desc = db.Column(db.String(36))
    createdAt = db.Column(db.String(50), nullable=False)
    updatedAt = db.Column(db.String(50), nullable=False)


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

    product = relationship("Product", back_populates="order_item")


db.create_all()



# #######################################
# #### Just execute once at first
# #### bulk uploap product items
# #######################################
#
# upload_items.bulk_upload(db, Product)


def get_today():
    print(datetime.today().strftime("%m-%d-%Y %H:%M:%S"))
    return datetime.today().strftime("%m-%d-%Y %H:%M:%S")


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

    return render_template("item_detail.html", item=item)


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


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not current_user or not current_user.is_authenticated:
        flash("You need to login or register!")
        return redirect(url_for("login"))

    if 's_status' in request.args and request.args['s_status'] == 'confirmed':
        shipping_address = [request.args['s_address']]
        s_status = request.args['s_status']
    else:
        # shipping_address = billing_address = UserAddress.query.filter_by(user_id=current_user.id).order_by(desc(UserAddress.id)).all()
        shipping_address =  UserAddress.query.filter_by(user_id=current_user.id).order_by(desc(UserAddress.id)).all()


    if 'b_status' in request.args and request.args['b_status'] == 'confirmed':
        billing_address = [request.args['b_address']]
        b_status = request.args['b_status']
    else:
        # shipping_address = billing_address = UserAddress.query.filter_by(user_id=current_user.id).order_by(desc(UserAddress.id)).all()
        billing_address = UserAddress.query.filter_by(user_id=current_user.id).order_by(desc(UserAddress.id)).all()

        if not billing_address:
            billing_address = ""


        s_status = ''
    # billing_address = UserAddress.query.filter_by(user_id=current_user.id).order_by(desc(UserAddress.id)).all()

    # if 'b_status' in request.args and request.args['b_status'] == 'confirmed':
    #     billing_address = [request.args['b_address']]
    #     b_status = request.args['b_status']

    print("shipping_address : ", shipping_address)

    cart = Cart.query.filter_by(user_id=current_user.id).first()

    shipping_form = AddressForm()

    # if request.method == 'GET' and shipping_address:
    if request.method == 'GET':
    # print(type(cart.cart_user.first_name), cart.cart_user.last_name)
        shipping_form.name.default = f'{cart.cart_user.first_name} {cart.cart_user.last_name}'
        shipping_form.action.default = "confirm_shipping_address"
        shipping_form.s_status.default = "confirmed"
        shipping_form.process()

    # shipping_form.name.default = f'{cart.cart_user.first_name} {cart.cart_user.last_name}'
    # shipping_form.process()

    billing_form = AddressForm()

    # if billing_address:
    if request.method == 'GET':
    # print(cart.cart_user.first_name, cart.cart_user.last_name)
        billing_form.name.default = f'{cart.cart_user.first_name} {cart.cart_user.last_name}'
        billing_form.action.default = "confirm_billing_address"
        billing_form.s_status.default = "confirmed"
        billing_form.b_status.default = "confirmed"
        billing_form.process()

    # s_status, b_status = '', ''
    # s_status =




    cart_id = request.args['cart_id'] if 'cart_id' in request.args else request.form['cart_id']
    s_status = request.args['s_status'] if 's_status' in request.args else ''
    b_status = request.args['b_status'] if 'b_status' in request.args else ''
    print(cart_id)

    cart_list = CartItem.query.filter_by(cart_id=cart_id, status='active').order_by(desc(CartItem.id)).all()

    # cart_list_dict = []
    #
    # for clist in cart_list:
    #     cart_item_dict = {
    #         "id": clist.id,
    #         "cart_id": clist.cart_id,
    #         "product_id": clist.product_id,
    #         "quantity": clist.quantity,
    #         "price": clist.product.price,
    #         "discount": clist.product.discount,
    #     }
    #
    #     cart_list_dict.append(cart_item_dict)
    #
    # print(type(cart_list_dict), cart_list_dict)
    # cart_list_json = json.dumps(cart_list_dict)
    #
    # print(type(cart_list_json), cart_list_json)

    cart_list_dict = []
    cart_list_json = ''

    if shipping_form.validate_on_submit():
        print("shipping_form.submit")
        new_address = UserAddress(
            user_id=current_user.id,
            type="shipping",
            name=shipping_form.name.data,
            street_1=shipping_form.street_1.data,
            street_2=shipping_form.street_2.data,
            city=shipping_form.city.data,
            state=shipping_form.state.data,
            zip_code=shipping_form.zip_code.data,
            phone=shipping_form.phone.data
        )

        db.session.add(new_address)
        db.session.flush()
        shipping_address = new_address
        db.session.commit()

        print(shipping_address)

        return redirect(url_for("checkout", cart_id=cart_id, s_status='confirmed', s_address=shipping_address))

    elif request.method == "POST":
        print("post")
        # if request.form['action'] == "confirm-shipping-address":

        data = request.form
        if data['action'] == "confirm-shipping-address":
            shipping_address = UserAddress.query.filter_by(user_id=current_user.id, id=data['ship_address_id']).all()
            print('elif - ', shipping_address)
            print(cart_list)
            # print(len(shipping_address))
            cart_id = data['cart_id']
            s_status = data['s_status']

            # return redirect(url_for("checkout", cart_id=data['cart_id'], s_address=shipping_address, s_form=shipping_form, b_form=billing_form, cart_list=cart_list, current_user=current_user))
            # return render_template("checkout.html", cart_id=data['cart_id'], s_address=shipping_address s_form=shipping_form, b_form=billing_form, cart_list=cart_list, current_user=current_user, s_status='confirmed')

        elif data['action'] == "confirm-billing-address":
            shipping_address = UserAddress.query.filter_by(user_id=current_user.id, id=data['ship_address_id']).all()
            billing_address = UserAddress.query.filter_by(user_id=current_user.id, id=data['bill_address_id']).all()

            cart_id = data['cart_id']

            s_status = data['s_status']
            b_status = data['b_status']


            for clist in cart_list:
                cart_item_dict = {
                    "id": clist.id,
                    "cart_id": clist.cart_id,
                    "user_id": current_user.id,
                    "product_id": clist.product_id,
                    "quantity": clist.quantity,
                    "price": clist.product.price,
                    "discount": clist.product.discount,
                    "ship_address_id": int(data['ship_address_id']),
                    "bill_address_id" : int(data['bill_address_id'])
                }

                cart_list_dict.append(cart_item_dict)

            print(type(cart_list_dict), cart_list_dict)
            cart_list_json = json.dumps(cart_list_dict)

            print(type(cart_list_json), cart_list_json)

            # order_subtotal = 0
            # order_discount = 0
            # order_tax = 0
            # order_shipping = 0
            #
            # for item in cart_list_dict:
            #     order_subtotal += item['price'] * item['quantity']
            #     order_discount += item['discount'] * item['quantity']
            #
            # order_total = order_subtotal - order_discount + (order_subtotal - order_discount) * order_tax + order_shipping
            #
            #
            #
            # # insert order / order_item table
            # new_order = Order(
            #     user_id=current_user.id,
            #     status='NC',
            #     sub_total=order_subtotal,
            #     discount=order_discount,
            #     tax=order_tax,
            #     shipping=order_shipping,
            #     total=order_total,
            #     billing_address_id=int(data['bill_address_id']),
            #     shipping_address_id=int(data['ship_address_id'])
            # )
            #
            # db.session.add(new_order)
            # db.session.flush()
            # order_id = new_order.id
            # print(order_id)
            #
            # db.session.commit()
            #


            # return render_template("checkout.html", cart_id=data['cart_id'], s_address=shipping_address, b_address=billing_address, bs_form=shipping_form, b_form=billing_form, cart_list=cart_list, current_user=current_user, s_status='confirmed', b_status='confirmed')

    # return render_template("order.html", cart_list=cart_list)
    return render_template("checkout.html", cart_id=cart_id, s_address=shipping_address, b_address=billing_address, s_form=shipping_form, b_form=billing_form, cart_list=cart_list, cart_list_json=cart_list_json, current_user=current_user, s_status=s_status, b_status=b_status)




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

    print('here -----', items)
    total = 0

    print(type(items))
    print(type(json.loads(items)))

    for item in json.loads(items):
        print('before - total', total)
        print('item.quantity', item['quantity'])
        print('item.price', item['price'])
        print('item.discount', item['discount'])
        total += item['quantity'] * (item['price'] - item['discount'])
        print('after - total', total)

    print(round(total*100))

    return round(total*100)



# def calculate_order_amount(items):
#     # Replace this constant with a calculation of the order's amount
#     # Calculate the order total on the server to prevent
#     # people from directly manipulating the amount on the client
#
#     print('here -----', items)
#     total = 0
#
#     print(type(items))
#     print(type(json.loads(items)))
#
#     for item in json.loads(items):
#         print('before - total', total)
#         print('item.quantity', item['quantity'])
#         print('item.price', item['price'])
#         print('item.discount', item['discount'])
#         total += item['quantity'] * (item['price'] - item['discount'])
#         print('after - total', total)
#
#     print(round(total*100))
#
#     return round(total*100)



def insert_order(items):
    print('---- insert order ---')
    print(items)
    print(type(items))

    order_subtotal = 0
    order_discount = 0
    order_tax = 0
    order_shipping = 0
    user_id, ship_address_id, bill_address_id = 0, 0, 0

    for item in json.loads(items):
        order_subtotal += item['price'] * item['quantity']
        order_discount += item['discount'] * item['quantity']
        user_id = item['user_id']
        ship_address_id = item['ship_address_id']
        bill_address_id = item['bill_address_id']

    order_total = order_subtotal - order_discount + (order_subtotal - order_discount) * order_tax + order_shipping

    # insert order / order_item table
    new_order = Order(
        user_id=user_id,
        status='pending',
        sub_total=order_subtotal,
        discount=order_discount,
        tax=order_tax,
        shipping=order_shipping,
        total=order_total,
        billing_address_id=bill_address_id,
        shipping_address_id=ship_address_id,
        payment_desc='',
        createdAt=get_today(),
        updatedAt=get_today()
    )

    db.session.add(new_order)
    db.session.flush()
    order_id = new_order.id
    print(order_id)
    db.session.commit()


    for item in json.loads(items):
        new_order_item = OrderItem(
            order_id=order_id,
            product_id=item['product_id'],
            price=item['price'],
            discount=item['discount'],
            quantity=item['quantity'],
            createdAt=get_today(),
            updatedAt=get_today()
        )

        db.session.add(new_order_item)
        db.session.commit()






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

        insert_order(data['items'])

        print('create_payment : ', jsonify({'clientSecret': intent['client_secret']}))


        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


# @app.route('/checkout')
# def checkout():
#     # data = request.
#     # intent = #
#     # return render_template("checkout-org.html" , client_secret=intent.client_secret)
#     return render_template("checkout.html")


@app.route('/success')
def transaction_success():
    if not current_user or not current_user.is_authenticated:
        flash("You need to login or register!")
        return redirect(url_for("login"))


    print("----success----")

    print(f"user_id : {current_user.id}")
    # print(f"cart_id : {cart_id}")
    print(request.args.to_dict(flat=False))
    print(type(request.args))

    transaction_result = request.args.to_dict(flat=False)
    print(transaction_result)

    current_order_items = ''

    if transaction_result['redirect_status'][0] == 'succeeded':
        current_order = Order.query.filter_by(user_id=current_user.id, status='pending').order_by(desc(Order.id)).first()

        order_id = current_order.id

        print('order_id : ', type(order_id), order_id)

        # current_order = Order.query.get(order_id)

        current_order.status = 'processing'
        current_order.payment_desc = transaction_result['payment_intent'][0]
        current_order.updatedAt = get_today()
        db.session.commit()

        current_order_items = OrderItem.query.filter_by(order_id=order_id).all()
        cart_id = Cart.query.filter_by(user_id=current_user.id).order_by(desc(Cart.id)).first().id

        for c_order_item in current_order_items:
            delete_cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=c_order_item.product_id, status='active').first()
            db.session.delete(delete_cart_item)
            db.session.commit()


    print('current_order_items: ', current_order_items)

    return render_template("success.html", order=current_order, order_items=current_order_items, result=transaction_result['redirect_status'][0])


@app.route('/order-history')
def order_history():
    if not current_user or not current_user.is_authenticated:
        flash("You need to login or register!")
        return redirect(url_for("login"))

    order_list = []

    all_orders = Order.query.filter_by(user_id=current_user.id, status='processing').order_by(desc(Order.id)).all()

    for order in all_orders:
        order_dict = {}
        print(order.id, type(order.id))
        order_dict['id'] = order.id
        order_dict['order'] = order
        order_dict['order_items'] = []

        print("order_dict['id'] :", type(order_dict['id']))
        all_order_items = OrderItem.query.filter_by(order_id=order.id).order_by(desc(OrderItem.id)).all()

        for order_item in all_order_items:
            print(order_item.product_id)
            order_dict['order_items'].append(order_item)

        order_list.append(order_dict)

    print(order_list)


    return render_template("order_history.html", order_list=order_list)



if __name__ == "__main__":
    app.run(debug=True)
