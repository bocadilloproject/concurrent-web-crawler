import asyncio
from typing import List

from crawler.fetch import fetch_results_from_url

STOP_SIGNAL = None


async def worker(queue, fetch, on_error):
    while not queue.empty():
        url = await queue.get()
        if url is STOP_SIGNAL:
            return
        try:
            await fetch(url)
        except Exception as e:
            on_error(url, e)
        finally:
            queue.task_done()


async def crawl(root_url: str, num_workers: int = 3) -> List[dict]:
    queue = asyncio.Queue()
    fetching, fetched = set(), set()
    results = []

    def on_error(url, e):
        print('error on', url, ':', e)

    async def fetch(url: str):
        if url in fetching:
            print('already fetching', url)
            return

        fetching.add(url)
        data = await fetch_results_from_url(url)
        results.append({
            'title': data['title'],
            'url': url,
            'description': data['description'],
        })
        fetched.add(url)

        for new_url in data['urls']:
            # Only follow links beneath the root url.
            if new_url.startswith(root_url):
                await queue.put(new_url)

    await queue.put(root_url)

    # Start workers and wait for queue to be empty.
    workers = asyncio.gather(
        *(worker(queue, fetch, on_error) for _ in range(num_workers))
    )
    await asyncio.wait_for(queue.join(), timeout=300)

    # Tell all workers to exit
    for _ in range(num_workers):
        await queue.put(STOP_SIGNAL)
    await workers

    return results
