import config
from datetime import datetime
from internal import constants
from service.notion import notion_service
from internal.types import Project
from internal.utils import add_new_multi_select_value
from monkeypatch import notion_patch

# methods
def insert_project(project: Project):    
    notion_patch.monkey_patch()
    existing_project = notion_service.get_projects().get(project.name)
    project_collection = notion_service.get_project_block().collection

    project_row = None
    if existing_project is None:
        project_row = project_collection.add_row()
    else:
        project_row = notion_service.get_projects().get(project.name)
    
    print("Inserting new project: {}".format(project.name))
    project_row.nama = project.name
    project_row.timeline = notion_service.create_date(start=project.start_date, end=project.end_date)

    for val in project.get_workers_collection():
        add_new_multi_select_value(project_collection, "Pekerja", val)

    project_row.pekerja = project.get_workers_collection()
    project_row.deliverables = project.get_deliverables_collection()
    project_row.status = project.status

    return project.name

def get_projects():
    project_map = notion_service.get_projects()
    projects = []
    for project in project_map:
        row = project_map[project]
        projects.append(Project.build_from_collection(row).to_json())
    return projects

def get_project_by_id(title):
    project = notion_service.get_project_by_title(title)
    return Project.build_from_collection(project).to_json()

