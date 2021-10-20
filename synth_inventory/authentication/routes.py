from flask import Blueprint, render_template, request
from synth_inventory.forms import UserLoginForm
from synth_inventory.models import User, db
auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        data = User(email, password)
        db.session.add(data)
        db.session.commit()
    return render_template('signup.html', form = form)


@auth.route('/signin')
def signin():
    return render_template('signin.html')
