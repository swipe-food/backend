from datetime import datetime
from typing import Callable, List

from apscheduler.schedulers.blocking import BlockingScheduler


class BlockingSchedulerAdapter:
    """Adapter for the BlockingScheduler from the apscheduler library.

    This scheduler blocks the current process and should be used when
    it is the only thing running in the process.
    """

    def __init__(self):
        self._scheduler = BlockingScheduler()

    def start(self):
        self._scheduler.start()

    def add_daily_jobs(self, jobs: List[Callable]):
        for index, job in enumerate(jobs):
            self._scheduler.add_job(job, 'cron', hour=index % 24, start_date=datetime.now())
