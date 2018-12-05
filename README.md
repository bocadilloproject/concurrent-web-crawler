# Tarantula

A concurrent web crawling service built with [Bocadillo], as featured in the Bocadillo docs.

[Bocadillo]: https://github.com/bocadilloproject/bocadillo

## Install

Using [Pipenv]:

```bash
pipenv install
```

## Quick start

Start the mock website (which we're going to crawl):

```bash
pipenv run python server.py 5001
```

Start the API server:

```bash
pipenv run python api.py
```

Crawl it:

```bash
curl http://localhost:8000/server/5001
```

[Pipenv]: https://pipenv.readthedocs.io
