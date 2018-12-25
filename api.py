import bocadillo

from jobs import Jobs

api = bocadillo.API()
jobs = Jobs()


@api.route("/crawls", methods=["post"])
async def create_crawl(req, res):
    json = await req.json()
    url = json["url"]
    job_id = jobs.create(url)

    @res.background
    async def crawl_it():
        await jobs.run(job_id)

    res.media = {"job_id": job_id}
    res.status_code = 202


@api.route("/crawls/{job_id:d}")
async def get_crawl(req, res, job_id: int):
    results = jobs.results_of(job_id)
    res.media = {"results": results, "job_id": job_id}
    res.status_code = 200 if results is not None else 202


if __name__ == '__main__':
    api.run()
