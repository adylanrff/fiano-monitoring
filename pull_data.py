import logging
from internal import fiano
from model import project as project_model
logging.basicConfig(filename='data.log', encoding='utf-8', level=logging.INFO)

if __name__ == "__main__":
    logging.info("Pulling data")
    projects = fiano.get_projects()
    for project in projects:
        project = project_model.Project.get(project_name=project.nama)
        print(project)
        print(project.get('deliverables'))
    
