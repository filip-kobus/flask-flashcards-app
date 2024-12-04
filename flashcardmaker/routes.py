from flask import render_template, redirect, flash, url_for, request
from flashcardmaker import app, bcrypt, db
from flashcardmaker.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddDirectoryForm, AddFlashcardForm
from flashcardmaker.models import User, Directory, Flashcard
from flask_login import login_user, logout_user, current_user, login_required
from flashcardmaker.directories import UserDir
from flashcardmaker.vision import VisionAi
import os


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form) 

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Wrong password or email!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            user_dir = UserDir()
            new_picture = user_dir.save_account_picture(form.picture.data)
            current_user.image_file = new_picture
        db.session.commit()
        flash(f'Account updated!', 'success')
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_picture/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/directories", methods=["GET", "POST"])
@login_required
def directories():
    image_file = url_for('static', filename='folder_icon.png')
    form = AddDirectoryForm()
    directories = current_user.directories
    if form.validate_on_submit():
        directory = Directory(name=form.name.data, user_id=current_user.id)
        user_dir = UserDir()
        user_dir.create_directory(directory.name)
        db.session.add(directory)
        db.session.commit()
        return redirect(url_for('directories'))
    return render_template('directories.html', title='My Flashcards',
                           form=form, image_file=image_file, directories=directories)

@app.route("/directories/<int:directory_id>/delete", methods=["GET", "POST"])
def directory_delete(directory_id):
    user_dir = UserDir()
    directory = Directory.query.get_or_404(directory_id)
    try:
        user_dir.remove_directory(directory.name)
        db.session.delete(directory)
        db.session.commit()
    except:
        flash(f'Directory is not empty!', 'danger')

    return redirect(url_for('directories'))

@app.route("/directories/<int:directory_id>", methods=["GET", "POST"])
def directory(directory_id):
    form = AddFlashcardForm()
    form.set_directory_id(directory_id)
    directory = Directory.query.get_or_404(directory_id)
    directory_path = "users/" + current_user.username + "/" + directory.name + "/"
    if form.validate_on_submit():
        user_dir = UserDir()
        vision = 
        filename = user_dir.add_flashcard(directory.name, form.picture.data, form.title.data)
        flashcard = Flashcard(title=form.title.data, image_file=filename, boxes_cords={}, directory_id=directory_id)
        db.session.add(flashcard)
        db.session.commit()
    return render_template('directory.html', title=directory.name, flashcards=directory.flashcards, form=form, directory_path=directory_path, current_flashcard=None)

@app.route("/directories/<int:directory_id>/<int:flashcard_id>", methods=["GET", "POST"])
def flashcard(directory_id, flashcard_id):
    form = AddFlashcardForm()
    form.set_directory_id(directory_id)
    directory = Directory.query.get_or_404(directory_id)
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    directory_path = "users/" + current_user.username + "/" + directory.name + "/"
    if form.validate_on_submit():
        user_dir = UserDir()
        filename = user_dir.add_flashcard(directory.name, form.picture.data, form.title.data)
        flashcard = Flashcard(title=form.title.data, image_file=filename, boxes_cords={}, directory_id=directory_id)
        db.session.add(flashcard)
        db.session.commit()
    return render_template('directory.html', title=directory.name, flashcards=directory.flashcards, form=form, directory_path=directory_path,  current_flashcard=flashcard)

@app.route("/directories/<int:directory_id>/<int:flashcard_id>/delete", methods=["GET", "POST"])
def flashcard_delete(directory_id, flashcard_id):
    user_dir = UserDir()
    directory = Directory.query.get_or_404(directory_id)
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    user_dir.remove_flashcard(directory.name, flashcard.image_file)
    db.session.delete(flashcard)
    db.session.commit()

    return redirect(url_for('directory', directory_id=directory_id))