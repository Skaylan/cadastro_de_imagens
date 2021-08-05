from app import app
from flask import render_template, url_for, request, session, redirect, flash
import os
from dotenv import load_dotenv
from app.models.conn import db
from werkzeug.security import generate_password_hash, check_password_hash


app.secret_key = os.getenv('SECRET_KEY')
load_dotenv()


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
        cursor = db.cursor(prepared=True)
        cursor.execute("SELECT username, password FROM usuarios WHERE username = '"+ username +"'")
        get_pw = cursor.fetchall()
        for row in get_pw:
            stored_username = row[0].decode()
            stored_password = row[1].decode()

        checked_pass = check_password_hash(stored_password, password)
        print(checked_pass)

        if stored_username == username and checked_pass == True:
            session['user'] = username
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
        if password != re_password:
            flash('Senhas não coincidem!')
        else:
            try:
                cursor = db.cursor(prepared=True)
                cursor.execute(f"INSERT INTO usuarios(nome, username, email, password, created_at) VALUES(?,?,?,?,now())", (nome, username, email, hashed_password))
                db.commit()
            except Exception as erro:
                print(erro)
                flash('Houve um erro')
            else:
                flash('Registrado com sucesso!')
    return render_template('register.html')


@app.route('/user')
def user():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))