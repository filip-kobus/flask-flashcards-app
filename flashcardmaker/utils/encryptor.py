import uuid

def generate_uuid_filename(extension=".jpg"):
    """Generate a unique filename using UUID4 with an optional file extension."""
    unique_id = str(uuid.uuid4())
    return unique_id + extension

if __name__ == "__main__":
    print(generate_uuid_filename(".png"))
