from Flask import Flask, Response
from flask.ext.login import LoginManager, UserMixin, login_required

login_manager = LoginManager()
login_manager.init_app(app)

# Mock db
users = {'foo@bar.tld': {'pw': 'secret'}}

class User(flask_login.UserMixin):
	pass

@app.route("/login/")
def login():
  return render_template("login.html",**app.config)

###

@login_manager.user_loader
def user_loader(email):
	if email not in users:
		return

	user = User()
	user.id = email
	return user

@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None

@login_manager.request_loader
def request_loader(request):
	email = request.form.get('email')
	if email not in users:
		return

	user = User()
	user.id = email

	# DO NOT store passwords in plain text and 
	# compare password hashes using constant-time comparison!
	user.is_authenticated = request.form['pw'] == users[email]['pw']

	return user

@app.route('/login', methods=['GET', 'POST'])
def login():
	# Here we use a class of some kind to represent and validate our
    # client-side form data. 
    form = LoginForm()
    if form.validate_on_submit():
    	# Login and validate the user.
    	# user should be an instance of the 'User' class.
    	login_user(user)

    	flask.flash('Logged in successfully.')

    	next = flask.request.args.get('next')
    	# next_is_valid should check to see if the
    	# user has valid permission to access the 'next' url
    	if not next_is_valid(next):
    		return flask.abort(400)

    	return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''
    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
    	user = User()
    	user.id = email
    	flask_login.login_user(user)
    	return flask.redirect(flask.url_for('protected'))

   return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
	return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
	flask_login.logout_user()
	return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
	return 'Unauthorized'