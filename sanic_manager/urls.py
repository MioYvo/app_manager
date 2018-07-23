# coding=utf-8
# __author__ = 'Mio'

from sanic_manager.handlers.app import AppView
from sanic_manager.settings import app


def prepare_routes():
    app.add_route(AppView.as_view(), "/", )
    # app.add_route(AppView.as_view(), "/<app_id>", )


