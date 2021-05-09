import sys
import configparser
from pprint import pprint
from datetime import datetime, date
import notion
from notion.client import NotionClient
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

try:
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    client = NotionClient(token_v2=config.get("Notion", "token"))
    
except Exception as e:
    print("Exception: " + str(e))
    sys.exit(1)

app = Flask(__name__)
api = Api(app)

class Project(Resource):
    def get(self):
        projectCollection = client.get_collection_view("https://www.notion.so/yukina/75df30bb16fa4bbe8545101278f82019?v=09307c14fd8a4c59b2b6c0c1dee48d62")
        projectList = []
        
        for row in projectCollection.collection.get_rows():
            project = {"title": row.title, "uuid": row.id, "tags": row.Tags, "type": row.Type}
            projectList.append(project)
        
        return projectList

class Thing(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('title')
            parser.add_argument('status')
            parser.add_argument('tags', action='append')
            parser.add_argument('projectTags')
            parser.add_argument('event', type=bool)
            parser.add_argument('deadLineStartDate')
            parser.add_argument('deadLineStartTime')
            parser.add_argument('deadLineEndDate')
            parser.add_argument('deadLineEndTime')
            parser.add_argument('deadLineTimeEnable', type=bool)
            parser.add_argument('project')
            parser.add_argument('note')
            parser.add_argument('code')

            args = parser.parse_args()

            print(args)

            thingCollection = client.get_collection_view("https://www.notion.so/yukina/cacf4f64685d45e6bfb4b95a9f61c882?v=762ef6bedd8845e7850fe6c762bea7dc")
            thing = thingCollection.collection.add_row()
            thing.title = args['title']
            thing.Status = args['status']
            thing.Tags = args['tags']
            thing.ProjectTags = args['projectTags']
            thing.isEvent = args['event']
            thing.Project = args['project']
            thing.Note = args['note']
            thing.Code = args['code']

            if(args['deadLineStartDate'] is not None):
                if(args['deadLineTimeEnable'] is True):
                    start = datetime.strptime(args['deadLineStartDate'] + " " + args['deadLineStartTime'], '%Y/%m/%d %H:%M')
                    if(args['deadLineEndDate'] is not None):
                        end = datetime.strptime(args['deadLineEndDate'] + " " + args['deadLineEndTime'], '%Y/%m/%d %H:%M')
                        thing.DeadLine = notion.collection.NotionDate(start, end=end)
                    else:
                        thing.DeadLine = notion.collection.NotionDate(start)
                if(args['deadLineTimeEnable'] is False or None):
                    start = datetime.strptime(args['deadLineStartDate'], '%Y/%m/%d').date()
                    if(args['deadLineEndDate'] is not None):
                        end = datetime.strptime(args['deadLineEndDate'], '%Y/%m/%d').date()
                        thing.DeadLine = notion.collection.NotionDate(start, end=end)
                    else:
                        thing.DeadLine = notion.collection.NotionDate(start)
                
            return "ok", 201
        except Exception as e:
            print(e)
            return str(e), 500


class Event(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('title')
            parser.add_argument('type')
            parser.add_argument('tags', action='append')
            parser.add_argument('project')

            args = parser.parse_args()
            
            print(args)

            eventCollection = client.get_collection_view("https://www.notion.so/yukina/48c699eca4b5442da622d06638d0ecba?v=828762e97cdc4db2876f44a3fcd6abe4")
            event = eventCollection.collection.add_row()
            event.title = args['title']
            event.Type = args['type']
            event.Tags = args['tags']
            event.Project = args['project']
            
            return "ok", 201
        except Exception as e:
            print(e)
            return str(e), 500

api.add_resource(Project, '/project')
api.add_resource(Thing, '/thing')
api.add_resource(Event, '/event')

if __name__ == '__main__':
    app.run(host=dcdos-notion-api, debug=False)
