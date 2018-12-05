from html.parser import HTMLParser


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.title = None
        self.description = None

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get('href')
        if href and tag == 'a':
            self.urls.append(href)

    # TODO extract page title and description (lookup the HTMLParser docs)

    @property
    def result(self) -> dict:
        return {
            'title': self.title,
            'description': self.description,
            'urls': self.urls
        }


def parse_results(html: str) -> dict:
    parser = Parser()
    parser.feed(html)
    return parser.result
