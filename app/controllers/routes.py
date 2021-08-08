from app import app
from flask import render_template, url_for, request, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from app.models.conn import db, Usuario
from sqlalchemy.exc import IntegrityError


load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        return redirect(url_for('user'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('user'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_infos = Usuario.query.filter_by(username=username).first()
        print(user_infos.username)
        if user_infos == None:
            flash('Usuario não existe')
        
        else:
            checked_pass = check_password_hash(user_infos.password, password)
            if checked_pass == False:
                flash('Senha Incorreta!')

            elif user_infos.username == username and checked_pass == True:
                    session['user'] = user_infos.username
                    session['id'] = user_infos.id
                    session['name'] = user_infos.name
                    return redirect(url_for('user'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('user'))

    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re-password']
        hashed_password = generate_password_hash(password)

        username = username.lower()
        if password != re_password:
            flash('Senhas não coincidem!')
        else:
            try:
                usuario = Usuario(nome, username, email, hashed_password)
                db.session.add(usuario)
                db.session.commit()
                flash('Registrado com sucesso!')
            except IntegrityError as erro:
                db.session.rollback()
                string_error = str(erro.__cause__)
                if 'email' in string_error:
                    flash('Email já registrado!')
                elif 'username' in string_error:
                    flash(('Username já registrado'))

    return render_template('register.html')


@app.route('/user')
def user():
    if 'user' not in session:
        return redirect(url_for('login'))
    id = session['id']
    name = session['name']
    return render_template('user.html', id=id, name=name)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))