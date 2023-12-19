
from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

disciplines = [
    {"id": 1, "name": "Mathematics", "credits": 3, "level": "Intermediate"},
    {"id": 2, "name": "Computer Science", "credits": 4, "level": "Advanced"},
    {"id": 3, "name": "History", "credits": 3, "level": "Beginner"}
]

discipline_parser = reqparse.RequestParser()
discipline_parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
discipline_parser.add_argument('credits', type=int, required=True, help='Credits cannot be blank')
discipline_parser.add_argument('level', type=str, required=True, help='Level cannot be blank')


class DisciplineResource(Resource):
    def get(self, discipline_id):
        discipline = next((item for item in disciplines if item["id"] == discipline_id), None)
        if discipline:
            return discipline
        else:
            return {"message": "Discipline not found"}, 404

    def put(self, discipline_id):
        args = discipline_parser.parse_args()
        discipline = next((item for item in disciplines if item["id"] == discipline_id), None)
        if discipline:
            discipline.update(args)
            return discipline
        else:
            return {"message": "Discipline not found"}, 404

    def delete(self, discipline_id):
        global disciplines
        disciplines = [item for item in disciplines if item["id"] != discipline_id]
        return {"message": "Discipline deleted"}

class DisciplineListResource(Resource):
    def get(self):
        return disciplines

    def post(self):
        args = discipline_parser.parse_args()
        new_discipline = {
            "id": len(disciplines) + 1,
            "name": args["name"],
            "credits": args["credits"],
            "level": args["level"]
        }
        disciplines.append(new_discipline)
        return new_discipline, 201

api.add_resource(DisciplineListResource, '/disciplines')
api.add_resource(DisciplineResource, '/disciplines/<int:discipline_id>')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
