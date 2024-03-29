
from flask import render_template, request, redirect,flash,session,url_for
from models import User
from werkzeug.security import check_password_hash
from models import db
from sqlalchemy.exc import IntegrityError

def signup():
    return render_template('signup.html')





def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
def is_password_legal(password):
    if len(password) < 8:
        return False
    special_characters = "!@#&%()"
    if not any(char in special_characters for char in password):
        return False

    return True 
    
    
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!")
            return render_template('signup.html', username=username, email=email)
        if not is_password_legal(password):
            flash("Password must be at least 8 characters long and include at least one of the following special characters: !@#&%")
            return render_template('signup.html', username=username, email=email)

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('homepage'))  
        except IntegrityError:
            db.session.rollback()
            flash('This username or email is already taken. Please choose a different one.')
            return render_template('signup.html', username=username, email=email)

    return render_template('signup.html')
    
    

def signin_page():
    return render_template("signin.html")
    
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['is_logged_in'] = True
            return redirect(url_for('homepage',is_admin=user.is_admin))
        
        else:
            flash('Invalid username or password')
            return render_template('signin.html',username=username)
            
    return render_template('signin.html')
    


def logout():
    session.pop('username', None)
    session['is_logged_in'] = False
    
    return redirect(url_for('homepage', is_logged_in=False))

