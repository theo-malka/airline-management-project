from flask import render_template
from app import app

@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title = 'Airline Management - Homepage')