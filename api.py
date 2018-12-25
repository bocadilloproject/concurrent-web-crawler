from itertools import count
from typing import Dict

import bocadillo
from bocadillo.exceptions import HTTPError

from jobs import Job

api = bocadillo.API()


@api.error_handler(HTTPError)
def to_json(req, res, exc: HTTPError):
    res.status_code = exc.status_code
    res.media = {"error": str(exc), "state": exc.status_code}


# In-memory store of jobs
jobs: Dict[int, Job] = {}

# Iterator for auto-incremented job keys.
keys = count(start=1)


@api.route("/scrapers", methods=["post"])
async def create_scraper(req, res):
    json = await req.json()
    url = json["url"]
    job = Job(key=next(keys), url=url)
    jobs[job.key] = job

    @res.background
    async def scrape():
        await job.run()

    res.media = job.to_json()
    res.status_code = 202


@api.route("/scrapers/{key:d}/results")
async def get_scraper_results(req, res, key: int):
    job = jobs.get(key)
    if job is None:
        raise HTTPError(404)
    res.media = job.to_json()
    res.status_code = 200 if job.finished is not None else 202


if __name__ == '__main__':
    api.run()
