# coding=utf-8
# __author__ = 'Mio'

from Manager.utils.web import BaseRequestHandler


class HomeHandler(BaseRequestHandler):
    def get(self):
        self.render("home.html")


