import os
import io
import secrets
from flashcardmaker import app
from PIL import Image
from flask_login import current_user
from utils import bucket_manager, encryptor

class UserDir:
    PROFILE_PICTURES_FOLDER = "profile-pictures"

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
        current_picture = current_user.image_filename
        if current_picture != "default.jpg":
            bucket_manager.remove_from_s3(self.PROFILE_PICTURES_FOLDER, current_picture)

        image, image_name = self.prepare_profile_picture(picture)
        bucket_manager.upload_to_s3(image, self.PROFILE_PICTURES_FOLDER, image_name)

        return image_name

    def prepare_profile_picture(self, picture):
        """Resizes picture to 125x125 and encrypts filename"""
        _, f_ext = os.path.splitext(picture.filename)
        image_format = f_ext[1:].upper()
        picture_fn = encryptor.generate_uuid_filename(extension=f_ext)
        
        output_size = (125, 125)
        i = Image.open(picture)
        i.thumbnail(output_size)

        if image_format == "JPG":
            image_format = "JPEG"

        image_buffer = io.BytesIO()
        i.save(image_buffer, format=image_format)
        image_buffer.seek(0)

        return image_buffer, picture_fn

    def get_account_picture(self, filename):
        return bucket_manager.get_presigned_url(self.PROFILE_PICTURES_FOLDER, filename)