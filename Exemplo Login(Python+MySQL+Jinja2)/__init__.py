from flask import Flask
import flask.views
import hashlib
from database import *

app = Flask(__name__)
app.secret_key = "psi"

admins = ["cmsilva", "dcabaceira"]

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
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

app.add_url_rule('/', view_func=Main.as_view('index'), methods=['GET', 'POST'])
app.add_url_rule('/404/', view_func=Error404.as_view('404'), methods=['GET'])

@app.errorhandler(404)
def page_not_found(e):
    return flask.redirect(flask.url_for('404'))

app.debug = True

app.run(port=80)
