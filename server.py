import os
from codecs import open

import redis
import hypermark

from flask import Flask, render_template, abort
from flask_common import Common
from pyquery import PyQuery as pq

app = Flask(__name__)

common = Common(app)
r = redis.from_url(os.environ['REDIS_URL'])

from config import author


class Entry(object):
    def __init__(self, path):
        self.path = path

    @property
    def html(self):
        with open(self.path, 'rb', 'utf-8') as f:
            return hypermark.text(f.read()).html

    @property
    def title(self):
        return pq(self.html)('h1')[0].text

    @property
    def slug(self):
        return self.path.split('/')[-1][:-3]

    def mark_read(self):
        """Mark the post as read, once."""

        r.get(self.slug)
        r.incr(self.slug)

    @property
    def views(self):
        """The number of views this poast has had."""
        value = r.get(self.slug)
        if value == 'None' or value is None:
            value = '0'

        return int(value)


def gen_entries():
    def gen():
        files = ['entries/{}'.format(e) for e in os.listdir('entries')]
        for f in reversed(sorted(files, key=os.path.getctime)):
            yield Entry(f)

    g = list(gen())
    g.sort(key=lambda x: x.views, reverse=True)

    return g


@app.route('/')
@common.cache.cached(timeout=60)
def index():

    return render_template('index.html', entries=gen_entries(), author=author)


@app.route('/entry/<slug>')
def entry(slug):
    try:
        entry = Entry('entries/{}.md'.format(slug))
        entry.mark_read()

        return render_template('entry.html', entry=entry, entries=gen_entries(),
            author=author)
    except IOError:
        abort(404)


if __name__ == "__main__":
    common.serve()
