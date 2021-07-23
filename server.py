from flask import Flask, render_template

from models import Users

app = Flask(__name__)


@app.route('/')
def hello():
    """Homepage"""
    return render_template('index.html')


@app.route("/scim/v2/Users", methods=['GET'])
    def users_get():
    """Get users"""
    if request.method == 'GET':
    
    user_data {
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

    return flask.jsonify(user_data)

if __name__ == "__main__":
    app.run(debug=True)