from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'hush_hush'

allusers = []


class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.firstname = None
        self.lastname = None
        self.email = None

    def __init__(self, username, password, firstname, lastname, email):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Password"})

    firstname = StringField(validators=[
        InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "First Name"})

    lastname = StringField(validators=[
        InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Last Name"})

    email = StringField(validators=[
        InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Email"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        for i in range(len(allusers)):
            if username == allusers[i].username:
                return False
        return True


class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for i in range(len(allusers)):
            if form.username.data == allusers[i].username:
                return render_template('dashboard.html', res=allusers[i])
        return render_template('createfirst.html')
    return render_template('login.html', form=form)


@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    for i in range(len(allusers)):
        if username == allusers[i].username:
            return render_template('dashboard.html', res=allusers[i])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if not form.validate_username(form.username.data):
        return render_template('badusername.html')
    if form.validate_on_submit() and form.validate_username(form.username.data):
        new_user = User(username=form.username.data, password=form.password.data,
                        firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
        allusers.append(new_user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
