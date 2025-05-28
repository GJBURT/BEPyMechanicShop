from dotenv import load_dotenv

# Load .env
load_dotenv()

from app import create_app
from app.models import db
import os
from app.config import config_by_name
from flask.cli import with_appcontext
import secrets

# print(secrets.token_hex(16))  # Print a random secret key for debugging

# Print to debug the loading of the .env variables
print(f"DB_USER: {os.getenv('DB_USER')}, DB_PASSWORD: {os.getenv('DB_PASSWORD')}")

# Determine config name
config_name = os.getenv('FLASK_ENV', 'development')
# config_class = config_by_name.get(config_name)

print(f'Using configuration: {config_name}')
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")

app = create_app(config_name)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()   