import bocadillo
from bocadillo.exceptions import HTTPError

from jobs import Jobs

api = bocadillo.API()

jobs = Jobs()


@api.route('/jobs/{pk:d}')
class JobDetail:

    async def get(self, req, res, pk: int):
        job = jobs.get(pk)
        if job is None:
            raise HTTPError(404)
        res.media = job._asdict()


@api.route('/jobs')
class JobList:

    async def post(self, req, res):
        payload = await req.json()
        if 'url' not in payload:
            raise HTTPError(400)
        job = jobs.create(payload['url'])
        res.status_code = 201
        res.media = job._asdict()


if __name__ == '__main__':
    api.run()
