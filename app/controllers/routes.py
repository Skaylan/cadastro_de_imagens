from app import app
from flask import render_template, url_for, request, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.tables import db, Usuario, Images
from sqlalchemy.exc import IntegrityError
import os
from app.controllers.config import *
import uuid


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/explorer', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        return redirect(url_for('user'))

    images = Images.query.order_by(Images.posted_at.desc()).all()    
    return render_template('index.html', images=images)


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
            flash('Usuario não existe!', 'erro')
        else:
            checked_pass = check_password_hash(user_infos.password, password)
            if checked_pass == False:
                flash('Senha Incorreta!', 'erro')
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
            flash('Senhas não coincidem!', 'erro')
        else:
            try:
                usuario = Usuario(nome, username, email, hashed_password)
                db.session.add(usuario)
                db.session.commit()
                flash('Registrado com sucesso!', 'success')
            except IntegrityError as erro:
                db.session.rollback()
                string_error = str(erro.__cause__)
                if 'email' in string_error:
                    flash('Email já registrado!', 'erro')
                elif 'username' in string_error:
                    flash('Username já registrado!', 'erro')

    return render_template('register.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user' not in session:
        return redirect(url_for('login'))
    id = session['id']
    images = Images.query.order_by(Images.posted_at.desc()).all()
    im = [i for i in images if i.owner_id == id]
    return render_template('user.html', images=im)



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
            image.save(os.path.join(app.config['IMAGE_UPLOAD_PATH'], image.filename))

            image = Images(image.filename, session['id'], session['user'])
            db.session.add(image)
            db.session.commit()
            flash('Imagem Salva com sucesso!', 'success')
        return redirect(url_for('user'))


@app.route('/delete_image', methods=['GET', 'POST'])
def delete_image():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        image_id = request.form['image']
        delete = Images.query.filter_by(id=image_id).first()
        img_name = delete.file_name
        os.remove(os.path.join(app.config['IMAGE_UPLOAD_PATH'], img_name))
        db.session.delete(delete)
        db.session.commit()
    
    return redirect(url_for('user'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    id = session['id']
    infos = Usuario.query.filter_by(id=id).first()

    return render_template('profile.html', infos=infos)


@app.route('/edit_infos', methods=['GET', 'POST'])
def edit_infos():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        id = session['id']
        infos = Usuario.query.filter_by(id=id).first()

        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_password = request.form['newpassword']
        
        new_hashed_pass = generate_password_hash(new_password)
        checked_pass = check_password_hash(infos.password, password)
        if checked_pass == False:
            flash('Senha Incorreta!', 'erro')
        elif checked_pass == True:
            try:
                infos.name = name
                infos.email = email
                infos.username = username
                infos.password = new_hashed_pass
                db.session.commit()
            except  Exception as error:
                print(error.__cause__)
            
            else:
                flash('Dados atualizados com sucesso!', 'success')

        return redirect(url_for('profile'))


@app.route('/delete_account')
def delete_account():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('delete-account.html')


@app.route('/explore')
def explore():
    if 'user' not in session:
        return redirect(url_for('login'))

    id = session['id']
    images = Images.query.order_by(Images.posted_at.desc()).all()

    return render_template('explore.html', images=images)



@app.route('/delete_account_route', methods=['POST'])
def delete_account_route():
    if 'user' not in session:
        return redirect(url_for('login'))

    id = session['id']
    if request.method == 'POST':
        user = Usuario.query.filter_by(id=id).first()
        images = Images.query.filter_by(owner_id=id).all()
        password = request.form['password']
        user_password = user.password
        checked_password = check_password_hash(user_password, password)
        if checked_password == True:
            
            for image in images:
                img_name = image.file_name
                os.remove(os.path.join(app.config['IMAGES_UPLOADS'], img_name))
                db.session.delete(image)
                db.session.commit()

            session.pop('user', None)
            db.session.delete(user)
            db.session.commit()

            return redirect(url_for('index'))

        else:
            flash('Senha Incorreta!', 'erro')

            return redirect(url_for('delete_account'))