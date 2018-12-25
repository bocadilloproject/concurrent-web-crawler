from asyncio import sleep
from html.parser import HTMLParser
from typing import Tuple

import aiohttp


async def scrape(url: str, wait: int = 5) -> dict:
    await sleep(wait)
    status, text = await fetch(url)
    print({"event": "fetched", "url": url})

    results = parse_results(text)
    results["status"] = status

    return results


async def fetch(url) -> Tuple[int, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            status = response.status
            return status, text


class Parser(HTMLParser):
    _STARTED = object()

    def __init__(self):
        super().__init__()
        self.urls = []
        self.title = None
        self.description = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1" and self.title is None:
            self.title = self._STARTED
        elif tag == "meta" and self.description is None:
            if attrs.get("name") == "description":
                self.description = attrs.get("content")

    def handle_data(self, data: str):
        self._set_if_started("title", data)

    def _set_if_started(self, attr: str, data):
        if getattr(self, attr) == self._STARTED:
            setattr(self, attr, data)

    @property
    def result(self) -> dict:
        return {
            'title': self.title,
            'description': self.description,
        }


def parse_results(html: str) -> dict:
    parser = Parser()
    parser.feed(html)
    return parser.result
