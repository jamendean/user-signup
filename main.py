from flask import Flask, request, redirect, render_template
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    username = request.args.get('username')
    email = request.args.get('email')
    error1 = request.args.get('error1')
    error2 = request.args.get('error2')
    error3 = request.args.get('error3')
    error4 = request.args.get('error4')
    return render_template('user-signup.html', username=username, email=email, error1=error1,
        error2=error2, error3=error3, error4=error4)

def invalid_string_length(string):
    return (len(string) < 3 or len(string) > 20)


@app.route("/user-signup", methods=["POST"])
def validate():
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    email = request.form['email']
    error_msg = ''
    if not username:
        error_msg += "error1=Username is required.&"
    elif re.search('\s', username):
        error_msg += "error1=Username must not contain space characters.&"
        username = re.sub('\s', '', username)
    elif invalid_string_length(username):
        error_msg += "error1=Username must be between 3 and 20 characters.&"
    if not password1:
        error_msg += "error2=Password is required.&"
    elif re.search('\s', password1):
        error_msg += "error2=Password must not contain space characters.&"
    elif invalid_string_length(password1):
        error_msg += "error2=Password must be between 3 and 20 characters.&"
    elif not password2:
        error_msg += "error3=Verify password is required.&"
    elif re.search('\s', password2):
        error_msg += "error3=Verify password must not contain space characters.&"
    elif invalid_string_length(password2):
        error_msg += "error3=Verify password must be between 3 and 20 characters.&"
    elif password1 != password2:
        error_msg += "error3=Verify password does not match.&"
    if email:
        if len(email.split('@')) != 2:
            error_msg += "error4=Email must contain one @ symbol.&"
        elif len(email.split('.')) != 2:
            error_msg += "error4=Email must contain one period.&"
        elif re.search('\s', email):
            error_msg += "error4=Email must not contain space characters.&"
        elif invalid_string_length(email):
            error_msg += "error4=Email must be between 3 and 20 characters.&"
            
    if not (error_msg):
        return render_template('welcome.html', username = username)
    else:
        return redirect('/?' + error_msg + 'username=' + username + '&email=' + email)

app.run()