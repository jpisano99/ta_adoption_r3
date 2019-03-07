from my_app import app
from my_app.settings import app_cfg
from flask import render_template

from my_app.process_bookings import process_bookings
from my_app.build_dashboard import build_dashboard


@app.route('/')
def index():
    print('index')
    # return 'Hello Jimmy!'
    return render_template('index.html')


@app.route('/process_bookings_click')
def process_bookings_click():
    print('here i am')
    print(app_cfg['HOME'])
    process_bookings()
    return render_template('index.html')


@app.route('/build_dashboard_click')
def build_dashboard_click():
    print('here i am')
    print(app_cfg['HOME'])
    build_dashboard()
    return render_template('index.html')


@app.route('/test')
def test():
    print('hello')
    return 'index.html'
