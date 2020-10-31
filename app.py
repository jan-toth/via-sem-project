from flask import Flask
from flask_restplus import Api, Resource
import json

# TODO actual database
with open('db.json') as fr:
    db = json.loads(fr.read())


flask_app = Flask(__name__)
app = Api(app=flask_app, version="0.1", title="Kam pudem?", 
description="""Semestral project for 'Internet Applications Development' course at the Czech Technical University in Prague.""" )



# TODO change ... do not send this everytime => session
# TODO passwords should be hashed (possibly salted)
session_parser = app.parser()
session_parser.add_argument('username', type=str, location='headers')
session_parser.add_argument('password', type=str, location='headers')

ns = app.namespace("kam-pudem", description='Organize a poll to decide on a venue where you shall meet with your friends.')

def get_user(username):
    for user in db['users']:
        if user['username'] == username:
                return user    
    return None

@ns.route("/")
class Root(Resource):
    
    @app.doc(
        responses={200: 'OK', 400: "Username unknown", 403: "Incorect password"}, 
        parser=session_parser,
        description="Get list of all active polls connected with the user."
    )
    def get(self):
        args = session_parser.parse_args()
        user = get_user(args['username'])

        if user:
            if args['password'] == user['password']:
                return [poll for poll in db['events'] if poll['host'] == user['id'] or user['id'] in poll['guests']]
            else:
                ns.abort(403, status="Incorrect password", statusCode="403")
        else:
            ns.abort(400, status="Unknown username", statusCode="400")
            

"""Run Flask app"""
if __name__ == "__main__":
    flask_app.run(debug=True)
