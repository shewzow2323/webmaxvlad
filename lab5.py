
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask import Blueprint, render_template, request, make_response, redirect, session
# import psycopg2
# lab5 = Blueprint("lab5",__name__)


# def dbConnect():
#     conn = psycopg2.connect(
#         host='127.0.0.1',
#         database='knowledge_base_for_vlad',
#         user='postgres',
#         password='postgres'
#     )
#     return conn

# def dbClose(cursor, connection):
#     cursor.close()
#     connection.close()

# @lab5.route("/lab5")
# def main():
#     visitableuser = 'Anonim'
#     return render_template('lab5.html', username=visitableuser)

# @lab5.route("/lab5/users")
# def users():
#     conn = psycopg2.connect(
#         host="127.0.0.1",
#         database="knowledge_base_for_lolandvi",
#         user="lolandvi_knowledge_base",
#         password="123"
#     )
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM users;")
#     result = cur.fetchall()
#     cur.close()
#     conn.close()
#     return render_template('users.html', result=result)

# @lab5.route("/lab5/auth_note", methods=['GET', 'POST'])
# def auth():
#     errors = []

#     if request.method == 'GET':
#         return render_template('auth_note.html', errors=errors)
    
#     username = request.form.get('username')
#     password = request.form.get('password')

#     if not (username and password):
#         errors.append('Пожалуйста, заполните все поля')
#         print(errors)
#         return render_template('auth_note.html', errors=errors)
    
#     hashpassword = generate_password_hash(password)
#     conn = dbConnect()
#     cur = conn.cursor()
#     cur.execute(f"SELECT username FROM users WHERE username = '{username}';")

#     if cur.fetchone() is not None:
#         errors.append("Пользователь с таким именем уже существует")
#         dbClose(cur, conn)
#         return render_template('auth_note.html', errors=errors)
    
#     cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashpassword}');")
#     conn.commit()
#     dbClose(cur, conn)

#     return redirect("login_note")

# @lab5.route("/lab5/login_note", methods=['GET', 'POST'])
# def login():
#     errors = []

#     if request.method == 'GET':
#         return render_template('login_note.html', errors=errors)
    
#     username = request.form.get('username')
#     password = request.form.get('password')
#     user = username
#     if not (username and password):
#         errors.append('Пожалуйста, заполните все поля')
#         return render_template('login_note.html', errors=errors)
    
#     conn = dbConnect()
#     cur = conn.cursor()
#     cur.execute(f"SELECT username, id FROM users WHERE username = '{username}';")

#     result = cur.fetchone()
#     print(result)
#     if result is None:
#         errors.append("Пользователь с таким именем уже существует")
#         dbClose(cur, conn)
#         return render_template('login_note.html', errors=errors)
    
#     username, userid = result[0], result[1]
#     hashpassword = generate_password_hash(password)
#     if check_password_hash(hashpassword, password):
#         session['username'] = username
#         session['userid'] = userid
#         dbClose(cur, conn)
#         return render_template("lab5.html", username=user)
#     else:
#         errors.append("Неправильный логин или пароль")
#         return redirect("login_note", errors=errors)


# @lab5.route("/lab5/create_note", methods=['GET', 'POST'])
# def create():
#     errors = []

#     userid = session.get("userid")

#     if userid is not None:

#         if request.method == 'GET':
#             return render_template('create_note.html', errors=errors)
        
#         if request.method == "POST":
#             text_article = request.form.get("text_article")
#             title = request.form.get("title_article")
#             print(text_article)
#             if text_article == '':
#                 errors.append("Заполните текст")            
#                 return render_template('create_note.html', errors=errors)
    
#         conn = dbConnect()
#         cur = conn.cursor()
#         cur.execute(f"INSERT INTO articles(user_id, title, article_text) VALUES ('{userid}', '{title}', '{text_article}') RETURNING id")

#         new_article_id = cur.fetchone()[0]
#         conn.commit()

#         dbClose(cur, conn)
#         return redirect(f"/lab5/view_note/{new_article_id}")
#     return redirect("/lab5/login_note")

# @lab5.route("/lab5/view_note/<int:article_id>", methods=['GET', 'POST'])
# def view(article_id):
#     userid = session.get("userid")

#     if userid is not None:
#         conn = dbConnect()
#         cur = conn.cursor()
#         cur.execute("SELECT title, article_text FROM articles WHERE id = %s and user_id = %s", (article_id, userid))
#         articlebody = cur.fetchone()
#         print(articlebody)
#         conn.commit()
#         if articlebody is None:
#             return "Not found!"
#         text = articlebody[1].splitlines()
#         return render_template("view_note.html", article_text=text, article_title=articlebody[0], username=session.get("username"))

# @lab5.route("/lab5/list_note/", methods=['GET', 'POST'])
# def view_list():
#     userid = session.get("userid")
#     username = session.get("username")
#     if userid is not None:
#         conn = dbConnect()
#         cur = conn.cursor()
#         cur.execute(f"SELECT title FROM articles WHERE user_id = {userid}")
#         articlebody = cur.fetchall()
#         print(articlebody)
#         conn.commit()
#         return render_template("list_note.html", articlebody=articlebody, username=username )
    
# @lab5.route("/lab5/logout/")
# def logout():
#     session.clear()
#     return redirect('/lab5/login_note')