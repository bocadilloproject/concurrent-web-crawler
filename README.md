# Raspador

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

For convenience, the `site/` directory provides a set of HTML pages you can serve with Python in order to run a local website for testing purposes. The following command serves them on `http://localhost:5001`:

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
{
    "key": 1,
    "url": "http://localhost:5001",
    "state": "scheduled",
    "results": null
}
```

The response will be returned immediately and the scraping will occur *asynchronously*.

The server will answer with a *job key* or ID as above, which can be used to retrieve results by calling `/scrapers/{key}/results`:

For example, let's call `http://localhost:8000/scrapers/1/results`.

- Example response while the scraper is running (status: 202):

```json
{
    "key": 1,
    "url": "http://localhost:5001",
    "state": "in_progress",
    "results": null
}
```

- Example response when the scraper has successfully finished (status: 200):

```json
{
    "key": 1,
    "url": "http://localhost:5001",
    "state": "success",
    "results": {
        "title": "Hello, world!",
        "description": "This fake website rocks.",
        "status": 200
    }
}
```

- Example response if scraping has failed (status: 200):

```json
{
    "key": 1,
    "url": "http://localhost:5001",
    "state": "failed",
    "results": {
        "error": "Cannot connect to host localhost:5001 ssl:None [No route to host]"
    }
}
```

[Pipenv]: https://pipenv.readthedocs.io
