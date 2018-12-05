import sys

import bocadillo

api = bocadillo.API()


@api.route('/')
async def index(req, res):
    res.html = await api.template('index.html')


@api.route('/about', name='about')
async def about(req, res):
    res.html = await api.template('about.html')


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except (TypeError, IndexError):
        port = 5001
    api.run(port=port)
