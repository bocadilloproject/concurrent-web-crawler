# Tarantula

A concurrent web scraping service built with [Bocadillo] which allows clients to fetch metadata about websites.

[Bocadillo]: https://github.com/bocadilloproject/bocadillo

## Install

Using [Pipenv]:

```bash
pipenv install
```

## Usage

First, start the API server:

```bash
pipenv run python api.py
```

To prevent fetching external websites, you can run the following command to serve the HTML documents inside `site/` on `http://localhost:5001`:

```bash
python -m http.server 5001 -b localhost -d site
```

Create a scraper for one of the pages, e.g. `index.html`:

```bash
curl http://localhost:8000/scrapers \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"url": "http://localhost:5001"}'
```

Example response:

```json
{"job_id": 1}
```

The response will be returned immediately and the scraping will occur *asynchronously*.

The server will answer with a *job ID* (as above) which we can use to retrieve results by calling `/scrapers/{job_id}/results`:

For example, let's call `http://localhost:8000/scrapers/1/results`:

- Example response while the scraper is running:

```json
{
  "results": null,
  "job_id": 1
}
```

- Example response when the scraper has finished:

```json
{
  "results": {
    "title": null,
    "description": null,
    "status": 200
  },
  "job_id": 1
}
```


[Pipenv]: https://pipenv.readthedocs.io
