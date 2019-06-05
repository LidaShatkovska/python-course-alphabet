from flask import Flask, render_template, abort, url_for
from werkzeug.utils import redirect
from fruits.routes import fruits
from vegetables.routes import vegetables

app = Flask(__name__)
app.register_blueprint(fruits)
app.register_blueprint(vegetables)


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/redirect_page')
def redirect_page():
    return render_template('redirect_page.html')


@app.route('/error_401')
def error_page():
    return render_template('error_401.html')


@app.route('/redirect')
def index():
    return redirect(url_for('redirect_page'))


@app.route('/login')
def login():
    abort(401)


@app.errorhandler(401)
def error_401_handler(error):
    return render_template("error_401.html", error=error)
