from urllib.parse import urljoin, urldefrag

import aiohttp

from crawler.parser import parse_results


async def fetch_results_from_url(url: str) -> dict:
    # TODO also return title and description
    async with aiohttp.ClientSession() as session:
        html = await fetch_html(session, url)
    print({'event': 'fetched', 'url': url})
    results = parse_results(html)
    results['urls'] = [
        urljoin(url, remove_fragment(new_url))
        for new_url in results['urls']
    ]
    return results


async def fetch_html(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


def remove_fragment(url: str) -> str:
    pure_url, frag = urldefrag(url)
    return pure_url
