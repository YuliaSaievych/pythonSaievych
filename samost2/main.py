# main.py

from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import secrets
from flask import render_template

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

# Replace the secret key with a strong, random secret in a production environment
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)

# Sample user data (for demonstration purposes, replace this with your user authentication logic)
users = {
    'john_doe': {'password': 'secret', 'roles': ['admin']},
    'jane_doe': {'password': 'secret', 'roles': ['user']}
}

disciplines = [
    {"id": 1, "name": "Mathematics", "credits": 3, "level": "Intermediate"},
    {"id": 2, "name": "Computer Science", "credits": 4, "level": "Advanced"},
    {"id": 3, "name": "History", "credits": 3, "level": "Beginner"}
]

discipline_parser = reqparse.RequestParser()
discipline_parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
discipline_parser.add_argument('credits', type=int, required=True, help='Credits cannot be blank')
discipline_parser.add_argument('level', type=str, required=True, help='Level cannot be blank')

# Route for generating a JWT token (login)
@app.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
    parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
    args = parser.parse_args()

    username = args['username']
    password = args['password']

    if username in users and users[username]['password'] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

class SecureDisciplineResource(Resource):
    @jwt_required()
    def put(self, discipline_id):
        current_user = get_jwt_identity()
        if 'admin' in users[current_user]['roles']:
            args = discipline_parser.parse_args()
            discipline = next((item for item in disciplines if item["id"] == discipline_id), None)
            if discipline:
                discipline.update(args)
                return discipline
            else:
                return {"message": "Discipline not found"}, 404
        else:
            return {"message": "Unauthorized to update discipline"}, 403

    @jwt_required()
    def delete(self, discipline_id):
        current_user = get_jwt_identity()
        if 'admin' in users.get(current_user, {}).get('roles', []):
            discipline = next((item for item in disciplines if item["id"] == discipline_id), None)
            if discipline:
                disciplines.remove(discipline)
                return {"message": "Discipline deleted"}
            else:
                return {"message": "Discipline not found"}, 404
        else:
            return {"message": "Unauthorized to delete discipline"}, 403

class DisciplineResource(Resource):
    def get(self, discipline_id):
        discipline = next((item for item in disciplines if item["id"] == discipline_id), None)
        if discipline:
            return discipline
        else:
            return {"message": "Discipline not found"}, 404

class DisciplineListResource(Resource):
    def get(self):
        return [{"id": discipline["id"], "name": discipline["name"], "credits": discipline["credits"], "level": discipline["level"]} for discipline in disciplines]

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if 'admin' in users.get(current_user, {}).get('roles', []):
            args = discipline_parser.parse_args()
            new_discipline = {
                "id": len(disciplines) + 1,
                "name": args['name'],
                "credits": args['credits'],
                "level": args['level']
            }
            disciplines.append(new_discipline)
            return {"id": new_discipline["id"], "name": new_discipline["name"], "credits": new_discipline["credits"], "level": new_discipline["level"]}, 201
        else:
            return {"message": "Unauthorized to create discipline"}, 403

api.add_resource(DisciplineListResource, '/disciplines')
api.add_resource(DisciplineResource, '/disciplines/<int:discipline_id>')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
