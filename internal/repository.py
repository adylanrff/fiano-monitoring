from model.project import Project
from model.project import ProjectDeliverable
from model.project import ProjectDeliverableSchedule
from model.project import ProjectDeliverableWorker
from model.project import Worker
from datetime import datetime
from app_init import db


def insert_to_db(project, deliverables, workers):
    new_project, project_created = Project.get_or_create(
        project_name=project.name,
        defaults={'project_status': project.status,
                  'timeline_start_date': project.start_date,
                  'timeline_end_date': project.end_date,
                  'created_at':  datetime.now(),
                  'updated_at': datetime.now()
                  }
    )

    deliverables_data_to_insert = [
        ProjectDeliverable(
            project_id=new_project.id,
            section=deliverable.section,
            item=deliverable.item,
            subitem=deliverable.subitem,
            info=deliverable.info,
            quantity=deliverable.quantity,
            price=deliverable.price,
            unit=deliverable.unit) for deliverable in deliverables]

    worker_db_data = []
    for w in workers:
        worker, worker_created = Worker.get_or_create(
            worker_name=w.name,
            defaults={
                'worker_type': "HARIAN",
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        )
        if worker_created:
            worker.save()
        worker_db_data.append(worker)

    if project_created:
        new_project.save()
        with db.database.atomic():
            ProjectDeliverable.bulk_create(
                deliverables_data_to_insert)
