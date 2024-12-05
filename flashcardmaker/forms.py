from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flashcardmaker.models import User, Directory, Flashcard
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose another one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Account with this email already exists.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])

    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if(username.data != current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose another one.')
        
    def validate_email(self, email):
        if(email.data != current_user.email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Account with this email already exists.')
            
class AddDirectoryForm(FlaskForm):
    name = StringField('New Folder Name',
                            validators=[Length(min=2, max=30)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        directory = Directory.query.filter_by(name=name.data, user_id=current_user.id).first()
        if directory:
            raise ValidationError('Folder with this name already exists.')
        

class AddFlashcardForm(FlaskForm):
    def __init__(self, directory_id):
        super().__init__()
        self._directory_id = directory_id

    title = StringField('Flashcard title',
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    picture = FileField('Upload image',
                        validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    
    submit = SubmitField('Add')

    def validate_title(self, title):
        flashcard = Flashcard.query.filter_by(directory_id=self._directory_id, title=title.data).first()
        if flashcard:
            raise ValidationError('Flashcard with this name already exists.')
        

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')