from flask import render_template, request, redirect,flash,session,url_for
from models import Stadium,User,Review
from werkzeug.security import check_password_hash
from models import db
from sqlalchemy.exc import IntegrityError


def homepage(is_logged_in=False,is_admin=False):
    stadiums = Stadium.query.all()
    username = session.get('username', 'Guest')
    is_logged_in=session.get('is_logged_in', False)
    user = User.query.filter_by(username=username).first()
    return render_template("homepage.html", stadiums=stadiums,username=username,is_logged_in=is_logged_in,is_admin=user.is_admin)

def add_stadium(id=None):
    if request.method=="GET":
     return render_template("add_stadium.html",stadium_data={})
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
    stadium=Stadium.query.filter_by(id=stadium_id).first()
    if stadium.rating:
     new_total_reviews = len(stadium.reviews)
     stadium.rating = round(float(((stadium.rating * (len(stadium.reviews)-1)) + float(rating)) / new_total_reviews), 2)
     stadium.stars_number=int(stadium.rating)
    else:
     stadium.rating = round(float(rating), 2)
     stadium.stars_number=int(rating)
        
    try:
        db.session.commit()
        flash('Review added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding review: ' + str(e), 'error')
    return redirect(url_for('stadium_detail',id=stadium_id))



def delete_stadium(id):
    stadium = Stadium.query.get_or_404(id)
    db.session.delete(stadium)
    db.session.commit()
    return redirect(url_for('homepage'))
    


def edit_stadium(id):
    print(id)
    stadium = Stadium.query.get_or_404(id)
    if request.method == 'POST':
        stadium.stadium_name = request.form['stadiumName']
        print(stadium.stadium_name)
        stadium.location = request.form['location']
        stadium.description = request.form['description']
        stadium.capacity = request.form.get('capacity', type=int)
        stadium.owner = request.form['owner']
        stadium.yearBuilt = request.form.get('yearBuilt', type=int)
        stadium.fieldSize = request.form['fieldSize']
        stadium.stadiumImage = request.form['stadiumImage']
        db.session.commit()
        return redirect(url_for('homepage'))  # 
    return render_template("add_stadium.html", stadium_data=stadium)