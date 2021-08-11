from app import app
from flask import render_template, url_for, request, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.conn import db, Usuario, Images
from sqlalchemy.exc import IntegrityError
import os
from app.controllers import config
import uuid




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
        username = username.lower()
        user_infos = Usuario.query.filter_by(username=username).first()
        if user_infos == None:
            flash('Usuario não existe')
        
        else:
            checked_pass = check_password_hash(user_infos.password, password)
            if checked_pass == False:
                flash('Senha Incorreta!')

            elif user_infos.username == username and checked_pass == True:
                    session['id'] = user_infos.id
                    session['user'] = user_infos.username
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


@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user' not in session:
        return redirect(url_for('login'))
    id = session['id']
    images = Images.query.filter_by(owner_id=id).all()
    return render_template('user.html', images=images)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            file_extension = image.filename
            file_extension = file_extension.split('.'[0])
            image.filename = uuid.uuid4().hex
            image.filename = image.filename + '.' + file_extension[1]
            image.save(os.path.join(app.config['IMAGES_UPLOADS'], image.filename))

            image = Images(image.filename, session['id'])
            db.session.add(image)
            db.session.commit()
            flash('Imagem Salva com sucesso!')
        return redirect(url_for('user'))

@app.route('/delete_image', methods=['GET', 'POST'])
def delete_image():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':

        image_id = request.form['image']
        delete = Images.query.filter_by(id=image_id).first()
        img_name = delete.file_name
        os.remove(os.path.join(app.config['IMAGES_UPLOADS'], img_name))
        db.session.delete(delete)
        db.session.commit()
    
    return redirect(url_for('user'))

    