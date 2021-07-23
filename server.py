import os
from flask import Flask, flash, redirect, request, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User

app = Flask(__name__)
database_url = os.getenv('DATABASE_URL', 'postgresql:///test-users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

@app.route('/')
def hello():
    """Homepage"""
    return render_template('index.html')


@app.route("/scim/v2/Users", methods=['GET'])
def users_get():
    """Get Users"""    
    query = User.query
    request_filter = request.args.get('filter')
    match = None
    if request_filter:
        match = re.match('(\w+) eq "([^"]*)"', request_filter)
    if match:
        (search_key_name, search_value) = match.groups()
        search_key = getattr(Users, search_key_name)
        query = query.filter(search_key == search_value)
    count = int(request.args.get('count', 100))
    start_index = int(request.args.get('startIndex', 1))
    if start_index < 1:
        start_index = 1
    start_index -= 1
    query = query.offset(start_index).limit(count)
    total_results = query.count()
    found = query.all()
    response = ListResponse(found,
                      start_index=start_index,
                      count=count,
                      total_results=total_results)
    return flask.jsonify(response.to_scim_resource())

if __name__ == "__main__":
    app.run(debug=True)