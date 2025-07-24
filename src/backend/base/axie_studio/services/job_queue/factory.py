from axie_studio.services.base import Service
from axie_studio.services.factory import ServiceFactory
from axie_studio.services.job_queue.service import JobQueueService


class JobQueueServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(JobQueueService)

    def create(self) -> Service:
        return JobQueueService()
