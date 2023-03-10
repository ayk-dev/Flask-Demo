from decouple import config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class TodoModel(db.Model):
    __tablename__ = "todos"
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    creator_pk = db.Column(db.Integer, db.ForeignKey('creators.pk'))
    creator = db.relationship('CreatorModel')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CreatorModel(db.Model):
    __tablename__ = "creators"
    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    todos = db.relationship("TodoModel", backref="todo", lazy='dynamic')


class TodoResource(Resource):
    def post(self):
        data = request.get_json()
        new_todo = TodoModel(**data)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo.as_dict()


# with app.app_context():
#     db.create_all()

api.add_resource(TodoResource, "/todos/")


if __name__ == '__main__':
    app.run()
