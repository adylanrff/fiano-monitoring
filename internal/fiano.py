import config
from datetime import datetime
from internal import constants
from service.notion import notion_service
from internal.types import Project
from internal.utils import add_new_multi_select_value


# methods
def insert_project(project: Project):    
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

    return project.name

def get_projects():
    workers = notion_service.get_workers()
    block = notion_service.get_block(config.NOTION_ROOT_PAGE_URL)
    
    projects_db_block = None
    pekerja_db_block = None
    deliverables_db_block = None
    
    for block in block.children:
        
        if hasattr(block, "title"):
            if block.title == constants.PEKERJA_PAGE_TITLE:
                pekerja_db_block = block
            elif block.title == constants.TASKS_PAGE_TITLE:
                deliverables_db_block = block
            elif block.title == constants.PROJECT_PAGE_TITLE:
                projects_db_block = block
        
    return projects_db_block.title
