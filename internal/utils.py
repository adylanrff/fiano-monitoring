import config
from uuid import uuid1
from service.notion import notion_service
from random import choice
from threading import Thread

def add_new_multi_select_value(collection, prop, value):
    colors = [
        "default",
        "gray",
        "brown",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple",
        "pink",
        "red",
    ]
    
    color = choice(colors)

    collection_schema = collection.get("schema")
    prop_schema = next(
        (v for k, v in collection_schema.items() if v["name"] == prop), None
    )

    if not prop_schema:
        print(
            f'"{prop}" property does not exist on the collection!'
        )
        return 

    if prop_schema["type"] != "multi_select":
        print(f'"{prop}" is not a multi select property!')
        return 
    
    dupe = next(
        (o for o in prop_schema["options"] if o["value"] == value), None
    )
    if dupe:
        print(f'"{value}" already exists in the schema!')
        return

    prop_schema["options"].append(
        {"id": str(uuid1()), "value": value, "color": color}
    )
    collection.set("schema", collection_schema)


class ProjectCreationWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            deliverable, deliverables, deliverables_collection, project_id, deliverables_blocks = self.queue.get()
            try:
                while True:
                    try:
                        new_deliverable_block = deliverable.get_or_create_collection_from_project(deliverables, deliverables_collection, project_id)
                        deliverables_blocks.append(new_deliverable_block)
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        break
            finally:
                self.queue.task_done()

class ProjectDeliverableReaderWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            all_deliverables, deliverable = self.queue.get()
            try:
                while True:
                    try:
                        from internal.types import ProjectDeliverable
                        new_deliverable = ProjectDeliverable.build_from_collection(deliverable).__dict__
                        all_deliverables.append(new_deliverable)
                    except:
                        continue
                    else:
                        break
            finally:
                self.queue.task_done()
