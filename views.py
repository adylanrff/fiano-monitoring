from app_init import app
from flask import request
from handler import projects as project_handler

@app.route('/project', methods=['POST'])
def insert_project():
    return project_handler.add_project_handler(request)

@app.route('/projects')
def get_projects():
    return {
        "data": fiano.get_projects()
    }
