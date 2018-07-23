# coding=utf-8
# __author__ = 'Mio'
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.log import logger as logging

from schema import Schema, Optional, Use, And
# from sqlalchemy import desc

from sanic_manager.models.app import App
from sanic_manager.settings import PLAT_ANDROID, PLAT_IOS, db


class AppView(HTTPMethodView):
    async def get(self, request):
        args = self.schema_get(request.raw_args)

        query = App.query
        count_query = db.select([db.func.count(App.id)])
        if 'plat' in args:
            query = query.where(App.platform == args['plat'])
            count_query = count_query.where(App.platform == args['plat'])

        total_apps = await count_query.gino.scalar()
        total_pages = total_apps / args['per_page']

        apps = await query.offset(args['per_page'] * (args['page'] - 1)).limit(args['per_page']).gino.all()

        apps = apps if apps else []

        return json({"total_pages": total_pages, "page": args['page'], "per_page": args['per_page'],
                     "content": [app.json_format() for app in apps]})

    def schema_get(self, request_raw_args):
        try:
            data = Schema({
                Optional("plat"): lambda x: x in (PLAT_ANDROID, PLAT_IOS),
                Optional("page", default=1): And(Use(int), lambda x: x > 0),
                Optional("per_page", default=20): And(Use(int), lambda x: x > 0),
                # Optional("total_pages", default=)
            }).validate(request_raw_args)
        except Exception as e:
            logging.error(e)
            abort("400", str(e))
        else:
            return data
