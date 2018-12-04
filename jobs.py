from typing import NamedTuple, Optional, List


class Result(NamedTuple):
    url: str
    title: Optional[str]
    description: Optional[str]


class Job(NamedTuple):
    id: int
    url: str
    status: str
    results: List[Result]


class Jobs:
    _last_id = 0

    def __init__(self):
        self._jobs = {}

    def get(self, job_id: int) -> Optional[Job]:
        return self._jobs.get(job_id)

    def create(self, url: str) -> Job:
        self._last_id = job_id = self._last_id + 1
        job = Job(id=job_id, url=url, status='pending', results=[])
        self._jobs[job_id] = job
        return job
