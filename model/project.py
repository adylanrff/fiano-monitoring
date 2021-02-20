from app import db
from peewee import Model
from flask_peewee.db import Database
from peewee import CharField, IntegerField, ForeignKeyField, DateTimeField

class BaseModel(Model):
    class Meta:
        database = db.database


class Project(BaseModel):
    project_name = CharField()
    project_status = CharField()
    timeline_start_date = DateTimeField()
    timeline_end_date = DateTimeField()
    actual_start_date = DateTimeField()
    actual_end_date = DateTimeField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

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
    unit = CharField()
    info = CharField()
    created_at = IntegerField()
    updated_at = IntegerField()

    class Meta:
        table_name = 'project_deliverable_tab'


class Worker(BaseModel):
    worker_name = CharField()
    worker_type = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    salary = IntegerField()

    class Meta:
        table_name = 'worker_tab'


class ProjectDeliverableWorker(BaseModel):
    worker = ForeignKeyField(Worker)
    project_deliverable_id = ForeignKeyField(ProjectDeliverable)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'project_deliverable_worker_tab'


class ProjectDeliverableSchedule(BaseModel):
    project_deliverable_id = ForeignKeyField(ProjectDeliverable)
    schedule_type = CharField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'project_deliverable_schedule_tab'
        indexes = (
            (('project_deliverable', 'schedule_type'), True),
        )
