from flask import render_template, redirect, flash, url_for, request
from flashcardmaker import app, bcrypt, db, mail
from flashcardmaker.forms import (RegistrationForm, LoginForm, UpdateAccountForm, AddDirectoryForm, 
                                  AddFlashcardForm, RequestResetForm, ResetPasswordForm)
from flashcardmaker.models import User, Directory, Flashcard
from flask_login import login_user, logout_user, current_user, login_required
from flashcardmaker import storage_manager
from flashcardmaker.vision import VisionAI
from flask_mail import Message
import os, json


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/demo")
def demo():
    json_path = os.path.join(app.root_path, 'static', 'utils', 'demo_boxes.json')

    with open(json_path, "r") as file:
        bounding_boxes = json.load(file)

    return render_template("demo.html", bounding_boxes=bounding_boxes, title='Demo')

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

    profile_picture = storage_manager.get_account_picture_url(current_user.image_filename)

    return render_template('account.html', title='Account', image_file=profile_picture, form=form)

@app.route("/directories", methods=["GET", "POST"])
@login_required
def directories():
    form = AddDirectoryForm()
    directories = current_user.directories
    if form.validate_on_submit():
        directory = Directory(name=form.name.data, user_id=current_user.id)
        storage_manager.create_directory(directory.name)
        db.session.add(directory)
        db.session.commit()
        return redirect(url_for('directories'))
    return render_template('directories.html', title='My Flashcards',
                           form=form, directories=directories)

@app.route("/directories/<string:directory_slug>/delete", methods=["GET", "POST"])
def directory_delete(directory_slug):
    directory = Directory.query.filter_by(slug=directory_slug).first_or_404()
    try:
        storage_manager.remove_directory(directory.name)
        db.session.delete(directory)
        db.session.commit()
    except:
        flash(f'Directory is not empty!', 'danger')

    return redirect(url_for('directories'))

@app.route("/directories/<string:directory_slug>", methods=["GET", "POST"])
def flashcards(directory_slug):
    directory = Directory.query.filter_by(slug=directory_slug).first_or_404()
    form = AddFlashcardForm(directory.id)

    if form.validate_on_submit():
        append_flashcard(directory, form)

    update_signed_urls(directory)

    return render_template('flashcards.html', directory=directory, form=form, current_flashcard=None, title=directory.name)

@app.route("/directories/<string:directory_slug>/<string:flashcard_filename>", methods=["GET", "POST"])
def single_flashcard(directory_slug, flashcard_filename):
    directory = Directory.query.filter_by(slug=directory_slug).first_or_404()
    form = AddFlashcardForm(directory.id)

    if form.validate_on_submit():
        append_flashcard(directory, form)

    update_signed_urls(directory)
    flashcard = Flashcard.query.filter_by(image_file=flashcard_filename).first_or_404()

    return render_template('flashcards.html', directory=directory, form=form, current_flashcard=flashcard, title=flashcard.title)

def append_flashcard(directory, form):
    image = form.picture.data
    filename = storage_manager.add_flashcard(directory.name, image)
    image.seek(0)
    vision = VisionAI(image.read())
    print(vision.grouped_boxes)
    flashcard = Flashcard(title=form.title.data, image_file=filename, boxes_cords=vision.grouped_boxes, directory_id=directory.id)
    db.session.add(flashcard)
    db.session.commit()

def update_signed_urls(directory):
    for flashcard in directory.flashcards:
        url = storage_manager.get_flashcard_url(directory.name, flashcard.image_file)
        flashcard.temp_signed_url = url

@app.route("/directories/<string:directory_slug>/<string:flashcard_filename>/delete", methods=["GET", "POST"])
def flashcard_delete(directory_slug, flashcard_filename):
    directory = Directory.query.filter_by(slug=directory_slug).first_or_404()
    flashcard = Flashcard.query.filter_by(image_file=flashcard_filename).first_or_404()
    storage_manager.remove_flashcard(directory.name, flashcard_filename)
    db.session.delete(flashcard)
    db.session.commit()

    return redirect(url_for('flashcards', directory_slug=directory_slug))

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