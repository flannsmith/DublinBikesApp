from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from application import views