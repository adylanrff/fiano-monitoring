import hashlib
from datetime import datetime
from queue import Queue
from typing import Literal
from service.notion import notion_service
from internal.utils import ProjectCreationWorker

# Types
class ProjectDeliverable:
    STATUS = [
        "Persiapan",
        "Sipil",
        "Produksi",
        ""
    ]
    def __init__(self, project: str, section: str, item:str, subitem:str, info:str, quantity:int, price:int):
        name = '-'.join([project, section, item, subitem])
        self.uuid = project + "-" + str(hashlib.sha256(name.encode('utf-8')).hexdigest())[:5]
        self.section = section
        self.item = item
        self.subitem = subitem
        self.info = info
        self.quantity = quantity
        self.price = price
        self.total_price = self.quantity * self.price
        self.status = "Persiapan"
        self.deliverables_map = {}

    @classmethod
    def build_from_json(cls, data):
        pass
    
    def get_or_create_collection_from_project(self, deliverables, deliverables_collection, projectId):
        deliverables_collection = notion_service.get_deliverables_block().collection
        deliverable = deliverables.get(self.uuid)
        print(deliverable)
        
        if deliverable is None:
            deliverable_row = deliverables_collection.add_row()
            deliverable_row.uuid = self.uuid
            deliverable_row.section = self.section
            deliverable_row.item = self.item
            deliverable_row.subitem = self.subitem
            deliverable_row.info = self.info
            deliverable_row.jumlah = self.quantity
            deliverable_row.harga = self.price
            deliverable_row.status = self.status
            deliverable = deliverable_row

        return deliverable

class ProjectWorker:
    def __init__(self, name: str, type:Literal["HARIAN", "BORONGAN"] = "HARIAN"):
        self.name = name
        self.type = type

    @classmethod
    def get_or_create_worker_collection(cls, name):
        workers_map = notion_service.get_workers()
        worker_collection = notion_service.get_worker_block().collection
        
        worker = workers_map.get(name)
        if worker is None:
            new_worker = cls(name)
            worker_row = worker_collection.add_row()
            worker_row.nama = new_worker.name
            worker_row.tipe = new_worker.type
            worker = worker_row
        
        return worker
    
    @classmethod
    def build_from_json(cls, data):
        pass



class Project:
    def __init__(
        self, 
        name: str, 
        deliverables: list[ProjectDeliverable]=[], 
        workers: list[ProjectWorker]=[], 
        start_date:datetime=datetime.now(), 
        end_date:datetime=datetime.now()):
        
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.deliverables = deliverables
        self.workers = workers
    
    def get_workers_collection(self):
        worker_names = []
        for worker in self.workers:
            cur_worker = ProjectWorker.get_or_create_worker_collection(worker.name)
            worker_names.append(cur_worker.nama)

        return worker_names


    def get_deliverables_collection(self):
        current_project = notion_service.get_projects().get(self.name)
        deliverables = notion_service.get_deliverables_by_project(current_project.id)
        deliverables_collection = notion_service.get_deliverables_block().collection

        deliverables_blocks = []

        queue = Queue()

        for x in range(8):
            worker = ProjectCreationWorker(queue)
            worker.daemon = True
            worker.start()

        for deliverable in self.deliverables: 
            queue.put((deliverable, deliverables, deliverables_collection, current_project.id, deliverables_blocks))
        
        queue.join()
        return deliverables_blocks

    @classmethod
    def build_from_json(cls, data):
        pass
