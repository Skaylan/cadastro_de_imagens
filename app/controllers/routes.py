from colorama.ansi import Back
from app import app
from flask import render_template, url_for, request, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from app.models.conn import db
from app.controllers.funcs import check_username, check_password


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

        try:
            cursor = db.cursor(prepared=True)
            cursor.execute("SELECT id, username, password FROM usuarios WHERE username = '"+ username +"'")
            user_infos = cursor.fetchall()
            print(user_infos)

            if len(user_infos) == 0:
                flash('Nome de usuario não existe')

            else:

                for row in user_infos:
                    stored_id = row[0]
                    stored_username = row[1].decode()
                    stored_password = row[2].decode()

                checked_pass = check_password_hash(stored_password, password)

                if stored_username == username and checked_pass == True:
                    session['user'] = stored_username
                    session['id'] = stored_id
                    return redirect(url_for('user'))

                elif check_username(username, stored_username) == False:
                    flash('Nome de usuario incorreto!')
                    
                elif check_password(password, stored_password) == False:
                    flash('Senha incorreta!')

        except Exception as erro:
            print(erro.__cause__)

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
    id = session['id']
    return render_template('user.html', id=id)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))