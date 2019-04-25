from flask import Flask, request, render_template, redirect, session
from hashlib import sha256

class User:
	def __init__(self, name, password):
		self.name = name
		self.password = sha256(password.encode()).hexdigest()
	def check_psw(self, password):
		return self.password == sha256(password.encode()).hexdigest()

def user_exists(name):
	for user in user_list:
		if name == user.name:
			return True
	return False

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'hey_baby'
user_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html', user_list=user_list)

@app.route('/login', methods=['POST'])
def login():
	msg = None
	name = request.form['name']
	password = request.form['password']
	for user in user_list:
		if user.check_psw(password) and user.name == name:
			msg = "Logged in"
		else:
			msg = "Error!"
	return render_template('login.html', msg=msg)

@app.route('/form_login')
def form_login():
	return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
	msg = None
	session['name'] = request.form['name']
	session['password'] = request.form['password']
	if user_exists(session['name']):
		msg = "User already exists!"
	else:
		user_list.append(User(session['name'], session['password']))
		msg = "Sucess!"
	return render_template('signup.html', msg=msg)

@app.route('/form_signup', methods=['GET'])
def form_signup():
	return render_template('signup.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)