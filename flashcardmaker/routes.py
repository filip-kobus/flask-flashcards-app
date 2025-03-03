from flask import render_template, redirect, flash, url_for, request
from flashcardmaker import app, bcrypt, db, mail
from flashcardmaker.forms import (RegistrationForm, LoginForm, UpdateAccountForm, AddDirectoryForm, 
                                  AddFlashcardForm, RequestResetForm, ResetPasswordForm)
from flashcardmaker.models import User, Directory, Flashcard
from flask_login import login_user, logout_user, current_user, login_required
from flashcardmaker import storage_manager
from flashcardmaker.vision import VisionAI
from flask_mail import Message
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
            new_picture = storage_manager.save_account_picture(form.picture.data)
            current_user.image_filename = new_picture
        db.session.commit()
        flash(f'Account updated!', 'success')
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = storage_manager.get_account_picture_url(current_user.image_filename)
    print(image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/directories", methods=["GET", "POST"])
@login_required
def directories():
    image_file = url_for('static', filename='folder_icon.png')
    form = AddDirectoryForm()
    directories = current_user.directories
    if form.validate_on_submit():
        directory = Directory(name=form.name.data, user_id=current_user.id)
        storage_manager.create_directory(directory.name)
        db.session.add(directory)
        db.session.commit()
        return redirect(url_for('directories'))
    return render_template('directories.html', title='My Flashcards',
                           form=form, image_file=image_file, directories=directories)

@app.route("/directories/<int:directory_id>/delete", methods=["GET", "POST"])
def directory_delete(directory_id):
    directory = Directory.query.get_or_404(directory_id)
    try:
        storage_manager.remove_directory(directory.name)
        db.session.delete(directory)
        db.session.commit()
    except:
        flash(f'Directory is not empty!', 'danger')

    return redirect(url_for('directories'))

@app.route("/directories/<int:directory_id>", methods=["GET", "POST"])
def directory(directory_id):
    form = AddFlashcardForm(directory_id)
    directory = Directory.query.get_or_404(directory_id)
    if form.validate_on_submit():
        filename = storage_manager.add_flashcard(directory.name, form.picture.data)
        form.picture.data.seek(0)
        vision = VisionAI(form.picture.data.read())
        flashcard = Flashcard(title=form.title.data, image_file=filename, boxes_cords=vision.grouped_boxes, directory_id=directory_id)
        db.session.add(flashcard)
        db.session.commit()

    flashcards_with_urls = get_url_for_flashcards_gallery(directory)
    return render_template('directory.html', title=directory.name, flashcards=flashcards_with_urls, form=form, current_flashcard=None)

def get_url_for_flashcards_gallery(directory):
    flashcards_with_urls = []
    for flashcard in directory.flashcards:
        url = storage_manager.get_flashcard_url(directory.name, flashcard.image_file)
        flashcards_with_urls.append({
            "id": flashcard.id,
            "title": flashcard.title,
            "signed_image_url": url,
            "image_file": flashcard.image_file,
            "boxes_cords": flashcard.boxes_cords,
            "directory_id": flashcard.directory_id
        })
    
    return flashcards_with_urls

def get_url_for_main_flashcard(directory, flashcard):
    url = storage_manager.get_flashcard_url(directory.name, flashcard.image_file)
    flashcard_with_url = {
            "id": flashcard.id,
            "title": flashcard.title,
            "signed_image_url": url,
            "image_file": flashcard.image_file,
            "boxes_cords": flashcard.boxes_cords,
            "directory_id": flashcard.directory_id
        }
    
    return flashcard_with_url

@app.route("/directories/<int:directory_id>/<int:flashcard_id>", methods=["GET", "POST"])
def flashcard(directory_id, flashcard_id):
    form = AddFlashcardForm(directory_id)
    directory = Directory.query.get_or_404(directory_id)
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    flashcards_with_urls = get_url_for_flashcards_gallery(directory)

    if form.validate_on_submit():
        filename = storage_manager.add_flashcard(directory.name, form.picture.data)
        form.picture.data.seek(0)
        vision = VisionAI(form.picture.data.read())
        flashcard = Flashcard(title=form.title.data, image_file=filename, boxes_cords=vision.grouped_boxes, directory_id=directory_id)
        db.session.add(flashcard)
        db.session.commit()
    flashcard_with_url = get_url_for_main_flashcard(directory, flashcard)

    return render_template('directory.html', title=directory.name, flashcards=flashcards_with_urls, form=form, current_flashcard=flashcard_with_url)

@app.route("/directories/<int:directory_id>/<int:flashcard_id>/delete", methods=["GET", "POST"])
def flashcard_delete(directory_id, flashcard_id):
    directory = Directory.query.get_or_404(directory_id)
    flashcard = Flashcard.query.get_or_404(flashcard_id)
    storage_manager.remove_flashcard(directory.name, flashcard.image_file)
    db.session.delete(flashcard)
    db.session.commit()

    return redirect(url_for('directory', directory_id=directory_id))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='filipkr204@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('If account with this email exists, email was sent', 'success')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user.password = hashed_password
        db.session.add(user)
        db.session.commit()
        flash(f'Password succesfuly changed', 'success')
        return redirect(url_for('home'))

    return render_template('reset_token.html', title='Reset Password', form=form)