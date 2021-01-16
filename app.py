from flask import Flask, url_for, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
from forms import FileComplaintForm, AdminForm
from config import Config
from flask_bcrypt import Bcrypt
from datetime import datetime
import random
from final import Processing_Test

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

class Complaints(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	area = db.Column(db.String(80), nullable=False)
	street = db.Column(db.Integer, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=False)
	email = db.Column(db.String(120), nullable=False)
	label = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(50), nullable=True)
    
	def __repr__(self):
		return f"Complaints('{self.area}','{self.date_posted}')"

class Admin(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"Admin('{self.email}', '{self.password}')"


@login_manager.user_loader
def load_user(email):
	return Admin.query.all()[0]



@app.route('/')
@app.route('/home')
def home():
	label = request.args.get("label",'', type = str)
	area = request.args.get("area",'', type = str)
	if label == "" and area == "":
		com = Complaints.query.order_by(Complaints.date_posted.desc()).all()
	elif area == "":
		com = Complaints.query.order_by(Complaints.date_posted.desc()).filter_by(label=label).all()
	else:
		com = Complaints.query.order_by(Complaints.date_posted.desc()).filter_by(area=area).all()
	return render_template('index.html', title='Home', com=com)

@app.route('/status/<string:id>/<string:stype>')
def status(id, stype):
	com = Complaints.query.filter_by(id=id).first()
	com.status = stype
	db.session.commit()
	return redirect(url_for('home'))
@app.route('/report', methods=['GET', 'POST'])
def report():
	reportForm = FileComplaintForm()
	if reportForm.submit.data==True:
		pred = Processing_Test(reportForm.description.data)
		com = Complaints(area=reportForm.area.data, street=reportForm.street.data, title=reportForm.title.data, description=reportForm.description.data, email=reportForm.email.data, label=pred)
		db.session.add(com)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('report.html', title='Report', reportForm=reportForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
	adminForm = AdminForm()
	if adminForm.login.data==True:
		admin = Admin.query.filter_by(email=adminForm.email.data).first()
		if admin and bcrypt.check_password_hash(admin.password, adminForm.password.data):
			login_user(admin)
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', adminForm=adminForm)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(port=5000)