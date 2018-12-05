import bocadillo

from crawler import crawl

api = bocadillo.API()


@api.route('/server/{port:d}')
async def call_server(req, res, port: int):
    res.media = await crawl(f'http://localhost:{port}')


if __name__ == '__main__':
    api.run()
