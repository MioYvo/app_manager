# coding=utf-8
# __author__ = 'Mio'
from sanic.log import logger

from sanic_manager.settings import db, DB_DSN, app
from sanic_manager.urls import prepare_routes

# app = Sanic()
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
    app.run(debug=True)
