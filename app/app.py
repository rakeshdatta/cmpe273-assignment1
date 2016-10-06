from flask import Flask
from flask import request
from model import db
from model import User
from model import CreateDB
from flask import jsonify
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
import json

# initate flask app
app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello World! Docker-Compose for Flask & Mysql\n'

#################################################################
@app.route('/v1/expenses', methods=['POST'])
def create():
	makeDB()
        body = request.data
        parsedbody = json.loads(body)

        expense = User( parsedbody['name'],
                    	parsedbody['email'],
                    	parsedbody['category'],
                    	parsedbody['description'],
                    	parsedbody['link'],
                    	parsedbody['estimated_costs'],
                    	parsedbody['submit_date'],
			"pending",
			"09-30-2016")


        db.session.add(expense)
        db.session.commit()

        return    jsonify({'id':expense.id,
                           'name':expense.username,
                           'email': expense.email,
                           'category': expense.category,
                           'description':expense.description,
                           'link':expense.link,
                           'estimated_costs':expense.estimated_costs,
                           'submit_date':expense.submit_date,
                           'status':expense.status,
                           'decision_date':expense.decision_date}),201


@app.route('/v1/expenses/<eid>', methods=['GET','DELETE','PUT'])
def rest(eid):
	makeDB()
	if request.method == 'GET':
		expense = User.query.filter_by(id=eid).first_or_404()
		return    jsonify({'id':expense.id, 
				   'name':expense.username,
				   'email': expense.email, 
				   'category': expense.category,
				   'description':expense.description,
				   'link':expense.link,
				   'estimated_costs':expense.estimated_costs,
				   'submit_date':expense.submit_date,
				   'status':expense.status,
				   'decision_date':expense.decision_date}),200

	if request.method == 'PUT':
		body = request.data
		parsedbody = json.loads(body)
 
	       	rec = User.query.get(eid)

                for key in parsedbody:
                	if key == 'name':
				rec.username = parsedbody['name']		
                	if key == 'email':
				rec.email = parsedbody['email']		
                	if key == 'category':
				rec.category = parsedbody['category']		
                	if key == 'description':
				rec.description = parsedbody['description']		
                	if key == 'link':
				rec.link = parsedbody['link']		
                	if key == 'estimated_costs':
				rec.estimated_costs = parsedbody['estimated_costs']		
                	if key == 'submit_date':
				rec.submit_date = parsedbody['submit_date']		
                	if key == 'status':
				rec.status = parsedbody['status']		
                	if key == 'decision_date':
				rec.decision_date = parsedbody['decision_date']		
		
                return " ",202


	if request.method == 'DELETE':
	        rec = User.query.get(eid)

		db.session.delete(rec)
		db.session.commit()
		return eid,204

##########################################################

def makeDB():
	HOSTNAME = 'mysqlserver'
	DATABASE = 'newtest'
	PASSWORD = 'p@ssw0rd123'
	USER = 'root'

	database = CreateDB(hostname = HOSTNAME)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
	db.create_all()
	db.session.commit()


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)

