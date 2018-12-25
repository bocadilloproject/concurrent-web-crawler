from html.parser import HTMLParser

import aiohttp


async def scrape(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            status = response.status

    print({"event": "fetched", "url": url})
    results = parse_results(html)
    results["status"] = status

    return results


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.title = None
        self.description = None

    # TODO extract page title and description (lookup the HTMLParser docs)

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
