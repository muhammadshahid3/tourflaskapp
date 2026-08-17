import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename


def save_upload(file_storage):
    """Save an uploaded FileStorage to the uploads folder and return the
    relative static path to store on the model, or None if no file given."""
    if not file_storage or not file_storage.filename:
        return None
    filename = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    dest = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
    file_storage.save(dest)
    return f"images/uploads/{unique_name}"
