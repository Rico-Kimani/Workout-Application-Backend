from app import app
from models import db

with app.app_context():
    print("Seeding database...")