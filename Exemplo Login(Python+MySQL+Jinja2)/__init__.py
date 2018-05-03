from flask import Flask
import flask.views
import hashlib
from database import *
import functools

app = Flask(__name__)
app.secret_key = "psi"

admins = ["cmsilva", "dcabaceira"]

def login_required_admin(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if ('username' in flask.session) and (flask.session['username'] in admins):
            return method(*args, **kwargs)
        else:
            flask.flash(
                "A login is required to see the page or you don't have permissions to enter", 'error')
            return flask.redirect(flask.url_for('index'))
    return wrapper

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        if 'create' in flask.request.form:
            return flask.redirect(flask.url_for('register'))
        require = ['username', 'passwd']
        for r in require:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required".format(r), 'error')
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        passwhard = hashlib.sha3_224(passwd.encode("utf-8")).hexdigest()
        listN = getDetails()[2]
        if username in listN and getPassword(username) == passwhard:
            flask.session['username'] = username
            flask.session['admins'] = admins
            if username in admins:
                flask.session['role'] = "Administrator"
            else:
                flask.session['role'] = 'Registered'
        else:
            flask.flash("Username doesn't exist or incorrect password", 'error')
        return flask.redirect(flask.url_for('index'))

class Error404(flask.views.MethodView):
    def get(self):
        return flask.render_template('404.html'), 404

class Register(flask.views.MethodView):
    @login_required_admin
    def get(self):
        return flask.render_template("register.html")

    @login_required_admin
    def post(self):
        require = ['username', 'passwd', 'passwd2']
        for r in require:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required".format(r), 'error')
                return flask.redirect(flask.url_for('register'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        passwd2 = flask.request.form['passwd2']

        if len(username) == 0:
            flask.flash("Error: Username is required", 'error')
            return flask.redirect(flask.url_for('register'))
        if username in getDetails()[2]:
            flask.flash("Error: This username already exist!", 'error')
            return flask.redirect(flask.url_for('register'))
        if " " in passwd:
            flask.flash("Error: Passwords must not have white spaces!", 'error')
            return flask.redirect(flask.url_for('register'))
        if (":" or "/" or "\\" or "|" or "%" or "\'") in passwd:
            flask.flash("Error: Passwords must not contain \':\', \'/\', \'\\', \'|\', \'%\'!", 'error')
            return flask.redirect(flask.url_for('register'))
        if passwd != passwd2:
            flask.flash("Error: Passwords must be the same!", 'error')
            return flask.redirect(flask.url_for('register'))
        if len(passwd) < 8:
            flask.flash("Error: Password must be at least 8 characters", 'error')
            return flask.redirect(flask.url_for('register'))
        passwhard = hashlib.sha3_224(passwd.encode("utf-8")).hexdigest()
        insertDetails(username, passwhard)
        return flask.redirect(flask.url_for('index'))

app.add_url_rule('/', view_func=Main.as_view('index'), methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=Register.as_view('register'), methods=['GET', 'POST'])
app.add_url_rule('/404/', view_func=Error404.as_view('404'), methods=['GET'])

@app.errorhandler(404)
def page_not_found(e):
    return flask.redirect(flask.url_for('404'))

app.debug = True

app.run(port=80)
