from flashcardmaker import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id ))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    directories = db.relationship('Directory', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.directories}')"
    

class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', lazy=True)

    def __repr__(self):
        return f"Directory('{self.id}, {self.name}, {self.flashcards}')"


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    image_file = db.Column(db.String(20), nullable=False)
    boxes_cords = db.Column(db.PickleType)
    directory_id = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=False)

    def __repr__(self):
        return f"Flashcards('{self.id},{self.directory_id} , {self.title}')"