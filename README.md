# Raspador

A concurrent web scraping service built with [Bocadillo] which allows clients to fetch metadata about websites.

## Rationale

Raspador demonstrates how to build:

1. A asynchronous web server exposing RESTful API endpoints.
2. A concurrent and non-blocking web service without resorting to a message queue or a broker.

To achieve (2), Raspador makes use of [background tasks][background task] to run I/O-intensive jobs in the background.

This principle can be easily adapted to other I/O-bound operations such as sending email (e.g. with [aiosmtpd]) or logging messages to an external service (e.g. with [aiologstash]).

## Concept

Raspador uses a simple, in-memory *scraper job* system. Jobs run *asynchronously* (i.e. in the background) while clients can use the server's REST API to create jobs and inspect their results.

In practice, a scraper job only consists in fetching a single URL. It is delayed by 5 seconds in order to simulate longer I/O-bound processing.

Jobs are stored in-memory, but it is very possible to extend Raspador to store them in a database instead. An asynchronous database client such as [asyncpg] would then be of great help.

## Install

Using [Pipenv]:

```bash
pipenv install
```

## Usage

### Running the app

First, start the API server:

```bash
pipenv run python api.py
```

For convenience, the `site/` directory provides a set of HTML pages you can serve with Python in order to run a local website for testing purposes. The following command serves them on `http://localhost:5001`:

```bash
python -m http.server 5001 -b localhost -d site
```

### Creating a scraper job

To create a scraper for one of the pages, e.g. `index.html`, make a call to the `POST /scrapers` endpoint:

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

The response will be returned immediately. This is because the scraping occurs *asynchronously* after the response has been sent. This is implemented with a [background task].

### Retrieving scraping results

When creating a scraper job, the server will return a *job key* (a unique identifier), which can be used to retrieve results by making a call to the GET `/scrapers/{key}/results` endpoint.

Below are example responses for a call to `/scrapers/1/results` (assuming the scraper job we're interested in has a key `1`).

- While the scraper is running (status: 202):

```json
{
    "key": 1,
    "url": "http://localhost:5001",
    "state": "in_progress",
    "results": null
}
```

- When the scraper has successfully finished (status: 200):

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

- If scraping has failed (status: 200):

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

[Bocadillo]: https://bocadilloproject.github.io
[Pipenv]: https://pipenv.readthedocs.io
[aiosmtpd]: https://github.com/aio-libs/aiosmtpd
[aiologstash]: https://github.com/aio-libs/aiologstash
[asyncpg]: https://github.com/MagicStack/asyncpg
[background task]: https://bocadilloproject.github.io/topics/features/background-tasks.html
