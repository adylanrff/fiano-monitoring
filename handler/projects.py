import config
from rq import Retry

from datetime import datetime

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from service.notion import notion_service
from internal import fiano
from internal import types
from schema import ProjectJsonSchema
from service.worker import worker_queue
from internal import repository

def add_project_handler(request):
    try:
        validate(instance=request.json, schema=ProjectJsonSchema)
        data = request.json.get('project')

        # Get project name
        project_name = data.get('nama')
        # Get workers
        pekerja_names = data.get('pekerja')
        workers_obj = [types.ProjectWorker(name) for name in pekerja_names]
        # get dates
        start_date = datetime.strptime(
            data.get('start_date'), "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(
            data.get('end_date'), "%Y-%m-%dT%H:%M:%S.%fZ")

        # Get project deliverables
        deliverables_data = data.get('deliverables')
        deliverables = []
        deliverables_data_to_insert = []
        for deliverable in deliverables_data:
            section = deliverable.get('section')
            item = deliverable.get('item')
            subitem = deliverable.get('subitem')
            price = deliverable.get('price')
            quantity = deliverable.get('quantity')
            info = deliverable.get('info')
            unit = deliverable.get('unit')
            workers = deliverable.get('workers', [])
            schedules = deliverable.get('schedules', [])

            new_deliverable = types.ProjectDeliverable(
                project_name, section, item, subitem, info, quantity, price, unit, workers, schedules)
            deliverables.append(new_deliverable)

        # enqueue object
        project = fiano.Project(project_name, deliverables=deliverables,
                                workers=workers_obj, start_date=start_date, end_date=end_date)

        job = worker_queue.enqueue(
            fiano.insert_project, project, retry=Retry(3))
        
        db_job = worker_queue.enqueue(
            repository.insert_to_db, project, deliverables, workers)

        return "Success enqueuing job for project {} ".format(project_name)

    except ValidationError as e:
        print(e)
        return e.message, 400
