from asyncio import sleep

from crawler import crawl


class Jobs:
    def __init__(self):
        self._results = {}
        self._jobs = {}
        self._next_job_id = 0

    def create(self, url: str) -> int:
        job_id = self._next_job_id = self._next_job_id + 1
        self._results[job_id] = None

        async def job():
            await sleep(10)
            return await crawl(url)

        self._jobs[job_id] = job()
        return job_id

    async def run(self, job_id: int):
        job = self._jobs.pop(job_id)
        self._results[job_id] = await job

    def results_of(self, job_id: int):
        return self._results[job_id]
