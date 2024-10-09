#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):

    def get(self):
        return {'message': 'Welcome to the Newsletter RESTFul API'}


class NewsLetters(Resource):

    def get(self):
        newsletter_dict_list = [
            newsletter.to_dict() for newsletter in Newsletter.query.all()
        ]
        return newsletter_dict_list

    def post(self):
        new_newsletter = Newsletter(title=request.form.get('title'),
                                    body=request.form.get('body'))

        db.session.add(new_newsletter)
        db.session.commit()

        new_newsletter_dict = new_newsletter.to_dict()
        return new_newsletter_dict


class NewsletterById(Resource):

    def get(self, id):
        newsletter_dict = Newsletter.query.get(id).to_dict()
        return newsletter_dict


api.add_resource(Home, '/')
api.add_resource(NewsLetters, '/newsletters')
api.add_resource(NewsletterById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
