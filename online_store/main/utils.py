"""Import os, secrets, PIL, and online_store."""
import os
import secrets
from PIL import Image
from online_store import create_app


def save_image(form_image, folder, size):
    """Save image to profile_images."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(
        app.root_path, f"static/{folder}", image_filename
    )
    output_size = (size, size)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_filename
