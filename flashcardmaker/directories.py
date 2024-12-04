import os
import secrets
from flashcardmaker import app
from PIL import Image
from flask_login import current_user

class UserDir:
    def __init__(self):
        self.user_path = os.path.join(app.root_path, 'static/users', current_user.username)

    def create_directory(self, directory):
        dir_path = os.path.join(self.user_path, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def remove_directory(self, directory):
        dir_path = os.path.join(self.user_path, directory)
        if os.path.exists(dir_path):
            if len(os.listdir(dir_path)) == 0:
                os.rmdir(dir_path)
            else:
                raise Exception("Directory must be empty")
            
    def add_flashcard(self, directory, picture, name):
        _, f_ext = os.path.splitext(picture.filename)
        filename = name + f_ext
        flashcard_path = os.path.join(self.user_path, directory, filename)
        picture.save(flashcard_path)

        return filename

    def remove_flashcard(self, directory, name):
        flashcard_path = os.path.join(self.user_path, directory, name)
        os.remove(flashcard_path)

    def save_account_picture(self, picture):
        image_path = os.path.join(app.root_path, 'static/profile_picture')
        old_picture = current_user.image_file
        if old_picture != "default.jpg":
            old_picture_path = os.path.join(image_path, old_picture)
            os.remove(old_picture_path)

        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(picture.filename)
        picture_fn = random_hex + f_ext
        
        new_picture_path = os.path.join(image_path, picture_fn)
        output_size = (125, 125)
        i = Image.open(picture)
        i.thumbnail(output_size)
        i.save(new_picture_path)

        return picture_fn