# coding=utf-8
# __author__ = 'Mio'
import asyncio
from os import getenv
from pathlib import Path
from tornado.ioloop import IOLoop
from gino import Gino


# --------------------     Loop     --------------------
tornado_ioloop = IOLoop.current()
# loop = asyncio.get_event_loop()


# --------------------     Database     --------------------

DB_USER = getenv("DB_HOST", "postgres")
DB_PASS = getenv("DB_PASS", "postgres")

DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = int(getenv("DB_PORT", "5432"))

DB_NAME = getenv("DB_NAME", "Manager")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = Gino()


# --------------------     Path     --------------------
SETTINGS_FILE_PATH = Path(__file__).absolute()
SYSPATH = SETTINGS_FILE_PATH.parent.parent
APP_PATH = SETTINGS_FILE_PATH.parent
TEMPLATE_PATH = APP_PATH / "templates"
STATIC_PATH = APP_PATH / "static"
