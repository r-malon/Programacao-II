from flask import Flask, request, render_template, redirect
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
user_list = []

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html', user_list=user_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = None
	if request.method == 'GET':
		name = request.args.get('name')
		password = request.args.get('password')
		for user in user_list:
			if user.check_psw(password) and user.name == name:
				msg = "Logged in"
			else:
				msg = "Error!"
	return render_template('login.html', msg=msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	msg = None
	if request.method == 'GET':
		name = request.args.get('name')
		password = request.args.get('password')
		if user_exists(name):
			msg = "User already exists!"
		else:
			user_list.append(User(name, password))
			msg = "Sucess!"
	return render_template('signup.html', msg=msg)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		pass

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)