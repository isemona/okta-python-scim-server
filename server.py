import os
from re import U
from flask import Flask, flash, redirect, request, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
#from models import User

app = Flask(__name__)
database_url = os.getenv('DATABASE_URL', 'postgresql:///test-users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

@app.route('/')
def hello():
    """Homepage"""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)