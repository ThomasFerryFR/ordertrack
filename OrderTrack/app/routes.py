from app import app, db
from flask import render_template, flash, redirect, request, url_for
from app import Scraper
from app.forms import OrderForm, LoginForm, RegistrationForm, DeleteButton
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Tracker, Order
from werkzeug.urls import url_parse

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	print(current_user)
	tracker = current_user.tracker[0]

	form = OrderForm()
	form.carrier.choices = [('Maersk Line','Maersk Line')]
	orders_db = tracker.orders.all()
	orders = []

	for order in orders_db:
		delete = DeleteButton()
		delete.order_id.data = order.id
		orders.append([order,delete])
    
	if form.validate_on_submit():
		tracker.create_order(form.orderName.data, form.po.data, form.container.data, form.carrier.data, form.dueDate.data)
		return redirect(url_for('index'))

	for order in orders:
		a = request.form
		b = dict(a)

		
		print(b)
		if "submit" in b and "order_id" in b:
			print(order[0].id)
			print(b["order_id"])
			if order[1].is_submitted() and b["submit"]==['Delete Order']:
				qry = Order.query.get(int(b["order_id"][0]))
				db.session.delete(qry)
				db.session.commit()
				
				orders_db = tracker.orders.all()
				orders = []

				for order in orders_db:
					delete = DeleteButton()
					delete.order_id.data = order.id
					orders.append([order,delete])

		return render_template('index.html', title='Hello World', orders=orders, form=form)

	return render_template('index.html', title='Hello World', orders=orders, form=form) 

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        if user.tracker is None:
        	user.set_tracker()

        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
   
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)