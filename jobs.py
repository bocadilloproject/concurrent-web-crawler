from scraper import scrape


class Job:
    def __init__(self, key: int, url: str, wait: int = 5):
        self.key = key
        self.url = url
        self.wait = wait
        self.state = "scheduled"
        self.results = None

    @property
    def finished(self) -> bool:
        return self.results is not None

    async def run(self):
        self.state = "in_progress"
        try:
            self.results = await scrape(self.url, wait=self.wait)
        except Exception as e:
            self.state = "failed"
            self.results = {
                "error": str(e)
            }
            raise e from None
        else:
            self.state = "success"

    def to_json(self):
        return {
            "key": self.key,
            "url": self.url,
            "state": self.state,
            "results": self.results,
        }
