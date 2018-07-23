# coding=utf-8
# __author__ = 'Mio'
from Manager.handlers.index import HomeHandler
from Manager.handlers.search import SearchSongs
from Manager.handlers.playlist import ImportPlayList, PlayList

urls = [
    (r"/", HomeHandler),
    (r"/search", SearchSongs),
    (r"/playlist", ImportPlayList),
    (r"/search_playlist", PlayList),
]
