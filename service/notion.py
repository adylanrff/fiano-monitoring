import config
from typing import Optional
from notion.client import NotionClient
from notion.collection import NotionDate


class NotionService:
    def __init__(self, token):
        self.token: str = token
        self.client: NotionClient = NotionClient(token_v2=token)

    def get_block(self, url):
        return self.client.get_block(url)

    def create_date(self, start, end):
        return NotionDate(start=start, end=end)

    def get_worker_block(self):
        return self.client.get_block(config.NOTION_WORKER_PAGE_URL)

    def get_project_block(self):
        return self.client.get_block(config.NOTION_PROJECT_PAGE_URL)

    def get_deliverables_block(self):
        return self.client.get_block(config.NOTION_DELIVERABLES_PAGE_URL)

    def get_projects(self):
        project_collection = self.get_project_block().collection
        project_map = {}
        for row in project_collection.get_rows():
            project_map[row.nama] = row
        return project_map

    def get_workers(self):
        worker_block = self.get_worker_block()
        worker_collection = worker_block.collection
        worker_map = {}
        for row in worker_collection.get_rows():
            worker_map[row.nama] = row

        return worker_map

    def get_deliverables_by_project(self, projectId):
        project_cv = self.client.get_collection_view(
            config.NOTION_DELIVERABLES_PAGE_URL)

        filter_params = {
            "filters": [{
                "filter": {
                    "value": {
                        "type": "exact",
                        "value": projectId
                    },
                    "operator": "relation_contains"
                },
                "property": "project"
            }],
            "operator": "and"
        }

        result = project_cv.build_query(filter=filter_params).execute()
        deliverables_map = {}
        for row in result: 
            deliverables_map[row.uuid] = row
        
        print(deliverables_map)
        return deliverables_map


notion_service: NotionService = NotionService(config.NOTION_TOKEN_V2)
