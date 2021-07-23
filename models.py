"""Models and database functions for Python Scim Seresponseer."""
# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class ListResponse():
    def __init__(self, list, start_index=1, count=None, total_results=0):
        self.list = list
        self.start_index = start_index
        self.count = count
        self.total_results = total_results

    def to_scim_resource(self):
        response = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": self.total_results,
            "startIndex": self.start_index,
            "Resources": []
        }
        resources = []
        for item in self.list:
            resources.append(item.to_scim_resource())
        if self.count:
            response['itemsPerPage'] = self.count
        response['Resources'] = resources
        return response

class User(db.Model):
    """User in Python Scim seresponseer."""

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
    
    def __init__(self, resource):
        self.update(resource)


    def to_scim_resource(self):
        response = {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": self.id,
            "userName": self.userName,
            "name": {
                "familyName": self.familyName,
                "givenName": self.givenName,
                "middleName": self.middleName,
            },
            "active": self.active,
            "meta": {
                "resourceType": "User",
                "location": url_for('user_get',
                                    user_id=self.id,
                                    _external=True),
            }
        }
        return response


    def scim_error(message, status_code=500):
        response = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "detail": message,
            "status": str(status_code)
        }
        return flask.jsonify(response), status_code


    # def send_to_browser(obj):
    #     socketio.emit('user',
    #                 {'data': obj},
    #                 broadcast=True,
    #                 namespace='/test')


    # def render_json(obj):
    #     response = obj.to_scim_resource()
    #     send_to_browser(response)
    #     return flask.jsonify(response)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<" \
            f"User id={self.id} active = {self.active} userName = {self.userName} familyName = {self.familyName} middleName = {self.middleName} givenName = {self.givenName} email = {self.email}>"


#####################################################################
# Helper functions

# def connect_to_db(app):
#     """Connect the database to our Flask app."""

#     # Configure to use our PostgreSQL database
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pythonscimserver'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.app = app
#     db.init_app(app)


# if __name__ == "__main__":
#     # As a convenience, if we run this module interactively, it will
#     # leave you in a state of being able to work with the database
#     # directly.
#     from server import app
#     connect_to_db(app)

#     # you specified db.create_all() here to create the database no need to type this command on the terminal
#     db.create_all()

#     print("Connected to DB.")