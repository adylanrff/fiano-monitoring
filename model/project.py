from peewee import CharField, IntegerField, ForeignKeyField
from model import BaseModel

class Project(BaseModel):
    project_name = CharField()
    project_status = CharField()
    timeline_start_date = IntegerField()
    timeline_end_date = IntegerField()
    actual_start_date = IntegerField()
    actual_end_date = IntegerField()
    created_at = IntegerField()
    updated_at = IntegerField()

    class Meta:
        table_name = 'project_tab'

class ProjectDeliverable(BaseModel):
    project_id = ForeignKeyField(Project)
    section = CharField()
    item = CharField()
    subitem = CharField()
    deliverable_status = CharField()
    price = IntegerField()
    quantity = IntegerField()
    unit = IntegerField()
    created_at = IntegerField()
    updated_at = IntegerField()

    class Meta:
        table_name = 'project_deliverable_tab'

class Worker(BaseModel):
    worker_name = CharField()
    worker_type = CharField()
    created_at = IntegerField()
    updated_at = IntegerField()
    salary = IntegerField()
    created_at = IntegerField()
    updated_at = IntegerField()

    class Meta:
        table_name = 'worker_tab'

class ProjectDeliverableWorker(BaseModel):
    worker = ForeignKeyField(Worker)
    project_deliverable = ForeignKeyField(ProjectDeliverable)
    created_at = IntegerField()
    updated_at = IntegerField()

    class Meta: 
        table_name = 'project_deliverable_worker_tab'
    
class ProjectDeliverableSchedule(BaseModel):
    project_deliverable = ForeignKeyField(ProjectDeliverable)
    schedule_type = CharField()
    start_time = IntegerField()
    end_time = IntegerField()
    created_at = IntegerField()
    updated_at = IntegerField()

    class Meta: 
        table_name = 'project_deliverable_schedule_tab'
        indexes = (
            (('project_deliverable', 'schedule_type'), True),
        )
