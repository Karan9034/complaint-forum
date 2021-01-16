from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email

class FileComplaintForm(FlaskForm):
	area = SelectField('Area', validators=[DataRequired()], choices=[('Whitehall','Whitehall'), ('Trafalgar Square','Trafalgar Square'), ('Bloomsbury', 'Bloomsbury'), ('Chelsea', 'Chelsea'), ('Kensington', 'Kensington')])
	street = SelectField('Street No.', validators=[DataRequired()], choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])
	title = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()], render_kw={"rows":"4"})
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Post Your Report')

class AdminForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	login = SubmitField('Login')