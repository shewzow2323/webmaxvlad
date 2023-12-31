from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, make_response, redirect, session

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/indexxx.html')

courses = [
    {"name": "c++", "videos": 3, "price":3000},
    {"name": "basic", "videos": 30, "price":0},
    {"name": "c#", "videos": 8} #если цена не указана то курс бесплатный
]

@lab8.route('/lab8/api/courses/', methods=['get'])
def get_courses():
    return courses

@lab8.route('/lab8/api/courses/<int:course_num>', methods=['get'])
def get_course(course_num):
    return courses[course_num]

@lab8.route('/lab8/api/courses/<int:course_num>', methods=['delete'])
def del_course(course_num):
    del courses [course_num]
    return '', 204




