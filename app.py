import config
from rq import Retry

from datetime import datetime

from flask import Flask, request
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from service.notion import notion_service
from internal import fiano
from internal.types import ProjectWorker, ProjectDeliverable
from schema import ProjectJsonSchema
from service.worker import worker_queue

app = Flask(__name__)


@app.route('/project', methods=['POST'])
def insert_project():
    try:
        validate(instance=request.json, schema=ProjectJsonSchema)
        data = request.json.get('project')
        
        # Get project name
        project_name = data.get('nama')

        # Get workers
        pekerja_names = data.get('pekerja')
        workers = [ProjectWorker(name) for name in pekerja_names]

        # Get project deliverables
        deliverables_data = data.get('deliverables')
        deliverables = []
        for deliverable in deliverables_data:
            section = deliverable.get('section')
            item = deliverable.get('item')
            subitem = deliverable.get('subitem')
            price = deliverable.get('price')
            quantity = deliverable.get('quantity')
            info = deliverable.get('info')
            unit = deliverable.get('unit')
            
            new_deliverable = ProjectDeliverable(project_name, section, item, subitem, info, quantity, price, unit)
            deliverables.append(new_deliverable)
        
        start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%dT%H:%M:%S.%fZ")

        # enqueue object
        project = fiano.Project(project_name, deliverables=deliverables, workers=workers, start_date=start_date, end_date=end_date)
        job = worker_queue.enqueue(fiano.insert_project, project, retry=Retry(3))

        return "Success enqueuing job for project {} ".format(project_name)

    except ValidationError as e:
        print(e)
        return e.message, 400

@app.route('/projects')
def get_projects():
    return fiano.get_projects()

if __name__ == '__main__':
    app.run()

