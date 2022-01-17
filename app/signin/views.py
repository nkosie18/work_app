from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_user, logout_user, login_manager, login_required
from werkzeug.urls import url_parse
from app.signin.models import User
from app.signin.forms import LoginForm, RegistrationForm
from app import db
import datetime

login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')
logout_bp = Blueprint('logout', __name__, template_folder='templates', static_folder='static')
register_bp = Blueprint('register', __name__, template_folder='templates', static_folder='static')



@login_bp.route('/login', methods=['GET', 'POST' ])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login.login'))

        elif user.status != 'Active':
            flash('This user account has been suspended. \n Please contact the Administrator to activate the account.')
            return redirect(url_for('login.login'))

        login_user(user, remember = form.remember_me.data)
        session.permanent = True
        next_page = url_for('home')
        if not next_page or url_parse(next_page).netloc !='':
            net_page = url_for('home')
        return redirect(url_for('home'))
    date1 = datetime.datetime.now().date().strftime("%d %B %Y")
    today = datetime.datetime.now().strftime("%A")
    if today == "Monday":
        roster1 = ['Daily Morning Checks All Linacs','Daily Planning checks','Vmat Plan checks', 'SASQART (Linac 1)']
    elif today == "Tuesday":
        roster1 = ['Daily Morning Checks All Linacs','Daily Planning checks','Brachytherapy checks', 'Pass Brachytherapy Docs']
    elif today == "Wednesday":
        roster1 = ['Daily Morning Checks All Linacs','Daily Planning checks','Vmat Plan checks on Linac 2', 'SASQART (Linac 2)']
    elif today == "Thursday":
        roster1 = ['Daily Morning Checks All Linacs','Daily Planning checks','Brachytherapy checks', 'Pass Brachytherapy Documents']
    elif today == "Friday":
        roster1 = ['Daily Morning Checks All Linacs','Daily Planning checks','Brachytherapy checks', 'Pass Brachytherapy Documents', ' SASQART (Linac  3)']
    else:
        roster1= ['It is the weekend. There is nothing to show today.', ' Enjoy your weekend, we will see you on Monday!']    
    return render_template ('signin/login.html', form=form, date1=date1, today = today, roster1 = roster1)

@logout_bp.route('/logout_user')
def logout():
    logout_user()
    return redirect(url_for('login.login'))
@register_bp.route('/register_user', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.is_authenticated:
        if current_user.role == 'Admin':
            form = RegistrationForm()

            if form.validate_on_submit():
                str_password = form.password.data
                min_length = len(str_password)
                if min_length < 8 or str.islower(str_password) or str.isupper(str_password) or str.isdigit(str_password) or str.isalpha(str_password):
                    flash('Your password need to be at least 8 cherectors long and have a combination of upper, lower case charactors and numbers')
                    return redirect(url_for('register.register'))

                new_user = User(username=form.username.data, role = form.role.data, status = 'Active')
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()

                flash('New user has been added successfully! ')
                return redirect(url_for('confirm.confirm'))

            return render_template('register_newUser.html', form = form) 

        else:
            return render_template('errors/unauthorized.html')

    else:
        return render_template('errors/unauthorized.html')

