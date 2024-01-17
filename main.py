from flask import Blueprint, redirect, url_for, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user, current_user
from Db import db
from Db.models import users, reservation, seans
from datetime import datetime

site = Blueprint('site', __name__)


@site.route('/')
def main():
    return redirect('/login')


@site.route('/register', methods=["GET", "POST"])
def register():

    errors=[]
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    if request.method == 'GET':
        return render_template('register.html', errors=errors)
    
    username_form = request.form.get('username')
    password_form = request.form.get('password')

    if not (username_form or password_form):
        errors.append('Пожалуйста, заполните все поля')
        return render_template('register.html', errors=errors)
    
    if len(password_form) < 5:
        errors.append('Пароль должен быть не менее 5 символов')
        return render_template('register.html', errors=errors)
    
    for i in password_form:
        if i in alphabet:
            errors.append('Пароль не должен содержать русские символы')
            return render_template('register.html', errors=errors)


    isUserExist = users.query.filter_by(login=username_form).first()

    if isUserExist is not None:
        errors.append('Пользователь с данным именем уже существует')
        return render_template('register.html', errors=errors)
    

    
    hashedPswd = generate_password_hash(password_form, method='pbkdf2')
    newUser = users(login=username_form, password=hashedPswd)

    db.session.add(newUser)
    db.session.commit()

    return redirect('/login')

@site.route('/login', methods=["GET", "POST"])
def login():
    errors=[]

    if request.method == "GET":
        return render_template("login.html", errors=errors)
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    if not (username_form or password_form):
        errors.append('Пожалуйста, заполните все поля')
        return render_template('login.html', errors=errors)

    my_user = users.query.filter_by(login=username_form).first()

    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect('/seanses')
        else:
            errors.append('Неправильный пароль')
            return render_template('login.html', errors=errors)
    if my_user is None:
        errors.append('Пользователь не найден')
        return render_template('login.html', errors=errors)
    return render_template("login.html") 


@site.route('/seanses/add', methods=["GET", "POST"])
def add_seanses():
    if current_user.get_id():
        if int(current_user.get_id()) == 10:
            errors = []

            if request.method == 'GET':
                return render_template('add_seanses.html')
            

            title = request.form.get('title')
            film_time = request.form.get('film_time')
            film_date = request.form.get('film_date')


            if not (title or film_time or film_date):
                errors.append('Пожалуйста, заполните все поля')
                return render_template('add_seanses.html', errors=errors) 
            
            newFilm = seans(title=title, time = film_time, data= film_date)

            db.session.add(newFilm)
            db.session.commit()
            return render_template('seanses.html')
        else:
            return redirect("/login")
    return redirect('/login')




@site.route('/seanses', methods=["GET", "POST"])
def show_seanses():
    if current_user.get_id():
        my_seanses = seans.query.order_by(seans.data).all()
        current_date = datetime.now().date()
        print(current_date)
        return render_template('seanses.html', lists=my_seanses, current_date = current_date)
    return redirect('/login')


@site.route('/seanses/<int:seans_id>', methods=["GET", "POST"])
def seeSeans(seans_id):
    if current_user.get_id():
        errors = []
        current_date = datetime.now().date()
        seats = [1,2,3,4,5,6,7,8,9,10,
                11,12,13,14,15,16,17,18,19,20,
                21,22,23,24,25,26,27,28,29,30]
        chosen_seats = []
        seats_red = []
        my_seans = seans.query.filter_by(id=seans_id).first()
        reserv = reservation.query.filter_by(seans=seans_id).all()
        for res in reserv:
            chosen_seats.append(res.seat)
        for i in seats:
            if i not in chosen_seats:
                seats_red.append(i)
        if request.method == 'GET':
            return render_template('seansN.html', my_seans = my_seans, seats_red = seats_red, errors=errors,current_date=current_date)
        selected_seats = request.form.getlist('selected_seats')
        if len(selected_seats) > 5:
            errors.append('Вы не можете выбрать более 5 мест')
            return render_template ('seansN.html', my_seans = my_seans, seats_red = seats_red, errors = errors,current_date=current_date)
        for s in selected_seats:
            new_reservation = reservation(seans=seans_id, user = int(current_user.get_id()), seat = s)
            db.session.add(new_reservation)
        db.session.commit()
        return redirect('/seanses')
    return redirect('/login')

@site.route('/profile', methods=["GET"])
def profile():
    if current_user.get_id():
        return render_template('profile.html')
    return redirect('/login')

    
@site.route('/profile_logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect('/')


@site.route('/profile_delete', methods=['GET','POST'])
@login_required
def deletes():
    id_m = int(current_user.get_id())
    dels = users.query.filter_by(id = id_m).first()
    db.session.delete(dels)
    db.session.commit()
    return redirect ('/login')


@site.route('/change_reserv', methods=['GET','POST'])
def change_reserv():
    if current_user.get_id():
        if int(current_user.get_id()) == 10:
            reserv = reservation.query.all()
            if request.method == 'GET':
                return render_template ('change_reserv.html', reserv=reserv)
            selected_reserv = request.form.getlist('selected_res')
            print(selected_reserv)
            for i in selected_reserv:
                del_res = reservation.query.filter_by(id=i).first()
                db.session.delete(del_res)
            db.session.commit()
            return redirect('/seanses')
        return redirect('/login')
    return redirect('/login')


@site.route('/change_seans', methods=['GET','POST'])
def change_seans():
    if current_user.get_id():
        if int(current_user.get_id()) == 10:
            sns = seans.query.all()
            if request.method == 'GET':
                return render_template ('change_seans.html', sns=sns)
            selected_sns = request.form.getlist('selected_sns')
            for i in selected_sns:
                del_sns = seans.query.filter_by(id=i).first()
                db.session.delete(del_sns)
            db.session.commit()
            return redirect('/seanses')
        return redirect('/login')
    return redirect('/login')