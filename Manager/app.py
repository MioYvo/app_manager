# coding=utf-8
# __author__ = 'Mio'
import sys
import logging
from pathlib import Path

import tornado.web
from tornado.options import define, options, parse_command_line
from gino.ext.tornado import Application, Gino, GinoRequestHandler

sys.path.append(str(Path(__file__).absolute().parent.parent))

from Manager.settings import db, TEMPLATE_PATH, STATIC_PATH, DB_URL, tornado_ioloop
from Manager.urls import urls

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


async def init_db(gino_db: Gino):
    await gino_db.set_bind(DB_URL, loop=tornado_ioloop.asyncio_loop)
    await gino_db.create_all()


class ManagerApp(tornado.web.Application):
    def __init__(self):
        self.db = db

        super(ManagerApp, self).__init__(
            handlers=urls,
            # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            # xsrf_cookies=True,
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            debug=options.debug,
            blog_title="APP Manager"
        )


def main():
    parse_command_line()
    app = ManagerApp()
    app.listen(options.port)
    logging.info("init db")
    tornado_ioloop.asyncio_loop.run_until_complete(init_db(app.db))
    logging.info(f"app run on port: {options.port}")
    tornado_ioloop.start()


if __name__ == "__main__":
    main()
