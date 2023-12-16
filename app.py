from flask import Flask, Blueprint, render_template, request, make_response
from db import db
from flask_sqlalchemy import SQLAlchemy
from db.models import users
from flask_login import LoginManager


from flask import Flask
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5





app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.secret_key = "123"

app.secret_key = '123'
user_db = "postgres"
host_ip = "localhost"
host_port = "5432"
database_name = "knowledge_base_for_vlad"
password = "123"
 
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')
    




