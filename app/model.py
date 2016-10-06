from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand



# Database Configurations
app = Flask(__name__)
DATABASE = 'newtest'
PASSWORD = 'p@ssw0rd123'
USER = 'root'
HOSTNAME = 'mysqlserver'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)

# Database migration command line
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):

	# Data Model User Table
	id		= db.Column(db.Integer, primary_key=True)
	username 	= db.Column(db.String(100), unique=False)
	email		= db.Column(db.String(120), unique=False)
	category 	= db.Column(db.String(120), unique=False)
	description 	= db.Column(db.String(120), unique=False)
	link 		= db.Column(db.String(120), unique=False)
	estimated_costs = db.Column(db.String(120), unique=False)
	submit_date 	= db.Column(db.String(120), unique=False)
	status 		= db.Column(db.String(120), unique=False)
	decision_date 	= db.Column(db.String(120), unique=False)

	def __init__(self, username, email, category, description, link, estimated_costs, submit_date, status, decision_date):
		self.username  = username
		self.email = email
		self.category = category
		self.description = description
		self.link = link
		self.estimated_costs = estimated_costs
		self.submit_date = submit_date
		self.status= status
		self.decision_date = decision_date

	def __repr__(self):
		return '<User %r>' % self.username

class CreateDB():
	def __init__(self, hostname=None):
		if hostname != None:	
			HOSTNAME = hostname
		import sqlalchemy
		engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
		engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db


if __name__ == '__main__':
	manager.run()

