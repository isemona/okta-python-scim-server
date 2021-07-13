"""Models and database functions for Python Scim Server."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions


class User(db.Model):
    """User in Python Scim server."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    active = db.Column(db.String(64), default=False)
    userName = db.Column(db.String(255), unique=True, nullable=False, index=True)
    familyName = db.Column(db.String(255))
    middleName = db.Column(db.String(255))
    givenName = db.Column(db.String(255))
    email = db.Column(db.String(255))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<" \
            f"User id={self.id} active = {self.active} userName = {self.userName} familyName = {self.familyName} middleName = {self.middleName} givenName = {self.givenName} email = {self.email}>"


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pythonscimserver'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.
    from server import app
    connect_to_db(app)

    # you specified db.create_all() here to create the database no need to type this command on the terminal
    db.create_all()

    print("Connected to DB.")