import os

class Config:
    SECRET_KEY = 'just-for-development-alone'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'json'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # (max-limit of 16 MB)