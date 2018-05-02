from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.Scraper import order as scraped_order

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tracker = db.relationship('Tracker', backref='owner', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash, password)

	def set_tracker(self):
		tracker = Tracker(user_id=self.id)
		db.session.add(tracker)
		db.session.commit()

class Tracker(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	orders = db.relationship('Order', backref='displayer', lazy='dynamic')

	def create_order(self, name, po, cont, carrier, dueDate):
		status = scraped_order(name,po,cont,carrier,dueDate)
		status.extract_status()
		etaDate = status.etaDate
		order = Order(tracker_id=self.id, name=name, po=po, cont=cont,carrier=carrier,dueDate=dueDate,etaDate=etaDate)
		db.session.add(order)
		db.session.commit()

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id'))
	name = db.Column(db.String(128))
	po = db.Column(db.String(128))
	cont = db.Column(db.String(128))
	carrier = db.Column(db.String(128))
	dueDate = db.Column(db.String(128))
	etaDate = db.Column(db.String(128))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))