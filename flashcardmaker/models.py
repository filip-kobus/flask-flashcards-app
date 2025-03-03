from flashcardmaker import db, login_manager, app
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from slugify import slugify


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id ))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_filename = db.Column(db.String(50), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    directories = db.relationship('Directory', lazy=True)

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.directories}')"
    

class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', lazy=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.slug = self.generate_unique_slug(name)
        self.user_id = user_id

    def generate_unique_slug(self, name):
        base_slug = slugify(name)
        unique_slug = base_slug
        counter = 1

        while Directory.query.filter_by(slug=unique_slug).first():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1

        return unique_slug

    def __repr__(self):
        return f"Directory('{self.id}, {self.name}, {self.flashcards}')"


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    image_file = db.Column(db.String(50), nullable=False)
    boxes_cords = db.Column(db.PickleType)
    directory_id = db.Column(db.Integer, db.ForeignKey('directory.id'), nullable=False)
    temp_signed_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"Flashcards('{self.id},{self.directory_id} , {self.title}')"