from model.project import Project
from model.project import ProjectDeliverable
from model.project import ProjectDeliverableSchedule
from model.project import ProjectDeliverableWorker
from model.project import Worker
from datetime import datetime
from app_init import db

def insert_to_db(project, deliverables, workers):

    with db.database.atomic() as transaction:
        new_project, project_created = Project.get_or_create(
            project_name=project.name,
            defaults={'project_status': project.status,
                    'timeline_start_date': project.start_date,
                    'timeline_end_date': project.end_date,
                    'created_at':  datetime.now(),
                    'updated_at': datetime.now()
                    }
        )

        if project_created:
            new_project.save()

        for deliverable in deliverables:
            db_deliverable = ProjectDeliverable(
                project_id=new_project.id,
                section=deliverable.section,
                item=deliverable.item,
                subitem=deliverable.subitem,
                info=deliverable.info,
                quantity=deliverable.quantity,
                price=deliverable.price,
                unit=deliverable.unit)

            db_deliverable.save()
            workers = deliverable.workers
            schedules = deliverable.schedules
            
            for w in workers:
                worker, worker_created = Worker.get_or_create(
                    worker_name=w,
                    defaults={
                        'worker_type': "HARIAN",
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                )
                if worker_created:
                    worker.save()

                deliverable_worker_created = ProjectDeliverableWorker(
                    project_deliverable_id=db_deliverable.id,
                    worker_id=worker.id,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                deliverable_worker_created.save()

            for s in schedules:
                db_schedule = ProjectDeliverableSchedule(
                    project_deliverable=db_deliverable.id,
                    schedule_type=s.get('schedule_type'),   
                    start_time=s.get('start_time'),   
                    end_time=s.get('end_time'),   
                    created_at=datetime.now(),   
                    updated_at=datetime.now(),   
                )
                db_schedule.save()
