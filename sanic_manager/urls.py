# coding=utf-8
# __author__ = 'Mio'

from sanic_manager.handlers.app import AppListView, AppCurrentVersionView, AppCurrentVersionDownloadView
from sanic_manager.settings import app


def prepare_routes():
    app.add_route(AppListView.as_view(), "/", )
    app.add_route(AppCurrentVersionDownloadView.as_view(), "/current/<name>/<platform>/download", )
    app.add_route(AppCurrentVersionView.as_view(), "/current/<name>/<platform>", )
    # app.add_route(FileUploadView.as_view(), "/upload", )
    # app.add_route(AppView.as_view(), "/<app_id>", )


