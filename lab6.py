from flask import Blueprint, render_template, request, redirect, session
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user

lab6 = Blueprint('lab6', __name__)

@lab6.route('/lab6/check')
def main():
    my_users = users.query.all()
    print(my_users)
    return "result in console!"

@lab6.route('/lab6/checkarticles')
def checkarticles():
    my_articles = articles.query.all()
    print(my_articles)
    return "result in console!"

@lab6.route('/lab6/register', methods=["GET", "POST"])
def register():
    errors = []
    if request.method == "GET":
        return render_template("auth_note.html")
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    inUserExist = users.query.filter_by(username=username_form).first()

    if inUserExist is not None:
        errors.append('Пользователь с таким именем уже существует') 
        return render_template('auth_note.html', errors=errors) 
    
    if not username_form:
        errors.append('Пожалуйста, заполните все поля')
        print(errors)
        return render_template('auth_note.html', errors=errors)
    
    if len(password_form) < 5:
        errors.append('Длина пароля должна быть больше 5 символов')
        print(errors)
        return render_template('auth_note.html', errors=errors)
    
    hashedPswd = generate_password_hash(password_form, method='pbkdf2')
    new_User = users(username=username_form, password=hashedPswd)

    db.session.add(new_User)
    db.session.commit()

    return render_template('login_note.html')

@lab6.route('/lab6/login', methods=["GET", "POST"])
def login():
    errors = []
    if request.method == "GET":
        return render_template('login_note.html')
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    if not username_form or not password_form:
        errors.append('Пожалуйста, заполните все поля')
        print(errors)
        return render_template('login_note.html', errors=errors)

    my_user = users.query.filter_by(username=username_form).first()

    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect('/lab6/articles')
        else:
            errors.append('Введен неправильный пароль') 
            return render_template('login_note.html', errors=errors) 
    else:
        errors.append('Пользователя не существует') 
        return render_template('login_note.html', errors=errors) 

@lab6.route('/lab6/articles') 
@login_required 
def articles_list(): 
    my_articles = articles.query.filter((articles.is_public == True) | (articles.user_id == current_user.id)).all() 
    return render_template('list_note.html', articles=my_articles, username=current_user.username) 

@lab6.route('/lab6/articles/<int:article_id>')
@login_required
def articless(article_id):
    my_article = articles.query.get(article_id)
    if not my_article.is_public and my_article.user_id != current_user.id:
        return redirect('/lab6/head')
    return render_template('view_note.html', articles=my_article) 

@lab6.route('/lab6/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab6/head')

@lab6.route('/lab6/create_note', methods=["GET", "POST"]) 
@login_required 
def create(): 
    errors = [] 
    if request.method == 'GET': 
        return render_template('create_note.html', errors=errors) 
 
    if request.method == "POST": 
        text_article = request.form.get("text_article") 
        title = request.form.get("title_article") 
        is_public = request.form.get("is_public")
        if not text_article or not title: 
            errors.append("Заполните все поля") 
            return render_template('create_note.html', errors=errors) 
 
        new_article = articles(title=title, article_text=text_article, user_id=current_user.id, is_public=is_public) # добавляем новое поле для публичности статьи
        db.session.add(new_article) 
        db.session.commit() 
 
        return redirect(f"/lab6/articles/new_article.id") 
 
    return redirect("/lab6/login_note")

@lab6.route('/lab6/head')
def head():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = 'Anonim'
    return render_template('lab6.html', username=username)

