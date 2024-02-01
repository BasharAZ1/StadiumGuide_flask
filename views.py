from flask import render_template, request, redirect,flash,session,url_for
from models import Stadium,User,Review
from werkzeug.security import check_password_hash
from extensions import db
from sqlalchemy.exc import IntegrityError
def homepage(is_logged_in=False,is_admin=False):
    stadiums = Stadium.query.all()
    username = session.get('username', 'Guest')
    is_logged_in=session.get('is_logged_in', False)
    return render_template("homepage.html", stadiums=stadiums,username=username,is_logged_in=is_logged_in,is_admin=is_admin)

def add_stadium():
    if request.method=="GET":
     return render_template("add_stadium.html")
    elif request.method == "POST":
        stadium_name = request.form.get("stadiumName")
        location = request.form.get("location")
        description = request.form.get("description")
        capacity = request.form.get("capacity")
        owner=request.form.get("owner")
        yearBuilt=request.form.get("yearBuilt")
        fieldSize=request.form.get("fieldSize")
        stadiumImage=request.form.get("stadiumImage")
        s=Stadium(stadium_name=stadium_name,location=location,description=description,capacity=capacity,owner=owner,yearBuilt=yearBuilt,fieldSize=fieldSize,stadiumImage=stadiumImage)
        db.session.add(s)
        db.session.commit()
        return redirect("/")
        
def stadium_detail(id):
    stadium = Stadium.query.get_or_404(id)
    username = session.get('username', 'Guest')
    is_logged_in=session.get('is_logged_in', False)
    reviews = stadium.reviews 
    return render_template('stadium_detail.html', stadium=stadium,username=username,is_logged_in=is_logged_in,reviews=reviews)   


def signup():
    return render_template('signup.html')





def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    
    
    
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!")
            return render_template('signup.html', username=username, email=email)

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('homepage'))  # Redirect to homepage or appropriate route
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
            return homepage(is_admin=user.is_admin)
        else:
            flash('Invalid username or password')
            return render_template('signin.html',username=username)
            
    return render_template('signin.html')
    


def logout():
    session.pop('username', None)
    session['is_logged_in'] = False
    
    return redirect(url_for('homepage', is_logged_in=False))


def add_review():
    username = request.form['username']
    print(username)
    stadium_id = request.form['stadium_id']
    rating = request.form['rating']
    comment = request.form['comment']
    if  not username:
        user_id=0
    else:
        user = User.query.filter_by(username=username).first()
        user_id = user.id


    new_review = Review(
        stadium_id=stadium_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )

    db.session.add(new_review)
    try:
        db.session.commit()
        flash('Review added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding review: ' + str(e), 'error')
    return redirect(url_for('stadium_detail',id=stadium_id))



    