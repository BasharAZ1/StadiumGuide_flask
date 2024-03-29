from flask import Flask
from views import homepage, add_stadium,stadium_detail,add_review,delete_stadium,edit_stadium
from authentication import signup,register,signin_page,login,logout

def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    app.add_url_rule('/signup', 'signup', signup)
    app.add_url_rule('/signin', 'signin_page', signin_page)
    app.add_url_rule('/login', 'login', login,methods=[ "POST"])
    app.add_url_rule('/logout', 'logout', logout,methods=[ "POST","GET"])
    app.add_url_rule('/register', 'register',register,methods=[ "POST"])
    app.add_url_rule('/add_stadium.html', 'add_stadium', add_stadium, methods=["GET", "POST"])
    app.add_url_rule('/stadium/<int:id>', 'stadium_detail', stadium_detail, methods=["GET", "POST"])
    app.add_url_rule('/add_review', 'add_review', add_review, methods=["GET", "POST"])
    app.add_url_rule('/delete_stadium/<int:id>', 'delete_stadium', delete_stadium, methods=["GET"])
    app.add_url_rule('/edit_stadium/<int:id>', 'edit_stadium', edit_stadium, methods=["GET","POST"])
    
