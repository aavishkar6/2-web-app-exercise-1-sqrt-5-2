from flask import Flask, render_template, request, redirect, url_for, make_response
from utils import (
    register_user,
    login_user,
    show_listings,
    requires_login,
    add_listing,
    edit_profile,
    update_user_data,
    change_password,
    get_user_preferences,
    redirect_if_logged_in
)
from db import get_current_user_data
from defaults import TEMPLATES_DIR, STATIC_DIR, LOGIN_COOKIE_NAME

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)


@app.route('/')
def home():
    return render_template('index.html', user=get_current_user_data())


@app.route('/register', methods=['GET', 'POST'])
@redirect_if_logged_in
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    elif request.method == 'POST':
        try:
            register_user(request.form)
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('auth/register.html', error=e)


@app.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        try:
            user_id, setup_complete = login_user(request.form)
            redirect_page = 'home' if setup_complete else 'profile'
            response = make_response(redirect(url_for(redirect_page)))
            response.set_cookie(LOGIN_COOKIE_NAME, str(user_id))
            return response
        except Exception as e:
            return render_template('auth/login.html', error=e)


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.delete_cookie(LOGIN_COOKIE_NAME)
    return response


@app.route('/listings', methods=['GET', 'POST'])
@requires_login
def listings():
    if request.method == 'GET':
        return render_template('listings.html', listings_array=show_listings({}))
    elif request.method == 'POST':
        add_listing(request.form)
        return redirect(url_for('listings'))


@app.route('/additems', methods=['GET'])
@requires_login
def additems():
    return render_template('additems.html')


@app.route('/profile', methods=['GET', 'POST'])
@requires_login
def profile():
    if request.method == 'GET':
        return render_template('profile.html', user=get_current_user_data(), tags=get_user_preferences())
    elif request.method == 'POST':
        if request.form.get('update_user_data'):
            return edit_profile(request.form, update_user_data)
        elif request.form.get('change_password'):
            return edit_profile(request.form, change_password)
