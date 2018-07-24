# coding=utf-8
# __author__ = 'Mio'
import sys
from pathlib import Path
sys.path.extend([str(Path(__file__).absolute().parent.parent)])

from sanic.log import logger

from sanic_manager.settings import db, DB_DSN, app, APP_PORT
from sanic_manager.urls import prepare_routes


app.config.DB_DSN = DB_DSN
app.static('/uploads', './uploads', name='uploads')
db.init_app(app)


@app.listener('after_server_start')
async def after_server_start(_app, _loop):
    logger.info(db.bind)
    # await db.gino.drop_all()
    await db.gino.create_all()


if __name__ == '__main__':
    prepare_routes()
    app.run(host="0.0.0.0", debug=True, port=APP_PORT)
