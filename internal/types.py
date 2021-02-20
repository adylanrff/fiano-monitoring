import hashlib
import json
from datetime import datetime
from queue import Queue
from typing import Literal, List
from service.notion import notion_service
from internal.utils import ProjectCreationWorker, ProjectDeliverableReaderWorker
from internal.utils import add_new_multi_select_value

# Types


class ProjectDeliverable:
    def __init__(self, project: str, section: str, item: str, subitem: str, info: str, quantity: int, price: int, unit: str, workers: List[str], schedules: List[object]):
        name = '-'.join([project, section, item, subitem])
        self.uuid = project + "-" + \
            str(hashlib.sha256(name.encode('utf-8')).hexdigest())[:5]
        self.section = section
        self.item = item
        self.subitem = subitem
        self.info = info
        self.quantity = quantity
        self.price = price
        self.total_price = self.quantity * self.price
        self.status = "Gambar Kerja"
        self.unit = unit
        self.workers = workers
        self.schedules = schedules

    @classmethod
    def build_from_json(cls, data):
        pass

    @classmethod
    def build_from_collection(cls, row):
        uuid = row.uuid
        project = row.project[0].title
        section = row.section
        item = row.item
        subitem = row.subitem
        info = row.info
        quantity = row.jumlah
        price = row.harga
        status = row.status
        unit = row.unit

        deliverable = cls(project, section, item, subitem,
                          info, quantity, price, unit)
        deliverable.uuid = uuid
        deliverable.status = status
        return deliverable

    def get_or_create_collection_from_project(self, deliverables, deliverables_collection, projectId):
        deliverables_collection = notion_service.get_deliverables_block().collection
        deliverable = deliverables.get(self.uuid)

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
            deliverable_row.unit = self.unit

            pekerja = []
            for worker_name in self.workers:
                add_new_multi_select_value(
                    deliverables_collection, "Pekerja", worker_name)
                worker = ProjectWorker.get_or_create_worker_collection(
                    worker_name)
                pekerja.append(worker_name)
            deliverable_row.pekerja = pekerja

            for schedule in self.schedules:
                sd = schedule.get('start_date')
                ed = schedule.get('end_date')
                start_date = datetime.strptime(schedule.get('start_date'), "%Y-%m-%dT%H:%M:%S.%fZ") if sd is not None else None
                end_date = datetime.strptime(schedule.get('end_date'), "%Y-%m-%dT%H:%M:%S.%fZ") if ed is not None else None

                date = notion_service.create_date(
                    start=start_date, end=end_date)
                schedule_type = schedule.get('schedule_type', '').lower()
                if schedule_type == 'gambar kerja':
                    deliverable_row.jadwal_gambar_kerja = date
                elif schedule_type == 'belanja':
                    deliverable_row.jadwal_belanja = date
                elif schedule_type == 'sipil':
                    deliverable_row.jadwal_sipil = date
                elif schedule_type == 'produksi':
                    deliverable_row.jadwal_sipil = date
                elif schedule_type == 'delivery':
                    deliverable_row.jadwal_delivery = date
                elif schedule_type == 'setting':
                    deliverable_row.jadwal_setting = date
                elif schedule_type == 'finishing':
                    deliverable_row.jadwal_finishing = date

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
        deliverables: List[ProjectDeliverable]=[], 
        workers: List[ProjectWorker]=[], 
        start_date:datetime=datetime.now(), 
        end_date:datetime=datetime.now(),
        project_status:str="RAB",
        progress=0,
        ):
        
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.deliverables = deliverables
        self.workers = workers
        self.status = project_status
        self.progress = progress
    
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

    def to_json(self):
        return self.__dict__

    @classmethod
    def build_from_json(cls, data):
        pass

    @classmethod 
    def build_from_collection(cls, row):
        name=row.nama
        # generate deliverables
        collection_deliverables = row.deliverables
        deliverables = []

        queue = Queue()
        for x in range(8):
            worker = ProjectDeliverableReaderWorker(queue)
            worker.daemon = True
            worker.start()

        for deliverable in collection_deliverables:
             queue.put((deliverables, deliverable))

        queue.join()

        workers = row.pekerja
        start_date = row.timeline.start
        end_date = row.timeline.end
        project_status = row.status
        
        return cls(name, deliverables, workers, start_date, end_date, project_status)
