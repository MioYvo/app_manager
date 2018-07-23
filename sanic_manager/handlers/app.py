# coding=utf-8
# __author__ = 'Mio'
from math import ceil
from os import remove
from pathlib import Path

from sanic.exceptions import abort
from sanic.response import json, file_stream
from sanic.views import HTTPMethodView
from sanic.log import logger as logging

from schema import Schema, Optional, Use, And
from sqlalchemy import desc

from sanic_manager.models.app import App
from sanic_manager.utils.gtz import datetime_2_isoformat

from sanic_manager.settings import PLAT_ANDROID, PLAT_IOS, db


class AppListView(HTTPMethodView):
    async def get(self, request):
        args = self.schema_get(request.raw_args)

        query = App.query
        count_query = db.select([db.func.count(App.id)])

        if 'name' in args:
            query = query.where(App.name == args['name'])
            count_query = count_query.where(App.name == args['name'])

        if 'platform' in args:
            query = query.where(App.platform == args['platform'])
            count_query = count_query.where(App.platform == args['platform'])

        total_items = await count_query.gino.scalar()
        total_pages = int(ceil(total_items / float(args['items'])))

        apps = await query.offset(args['items'] * (args['page'] - 1)). \
            limit(args['items']).order_by(desc(App.is_active), desc(App.version), desc(App.create_at)).gino.all()

        apps = apps if apps else []

        return json({"total_pages": total_pages, "page": args['page'], "items": args['items'],
                     "total_items": total_items,
                     "content": [app.json_format() for app in apps]})

    def schema_get(self, request_raw_args):
        try:
            data = Schema({
                Optional("name"): Use(str),
                Optional("platform"): And(Use(lambda x: x.strip().lower()), lambda x: x in (PLAT_ANDROID, PLAT_IOS)),
                Optional("page", default=1): And(Use(int), lambda x: x > 0),
                Optional("items", default=20): And(Use(int), lambda x: 50 >= x > 0),
                # Optional("total_pages", default=)
            }).validate(request_raw_args)
        except Exception as e:
            logging.error(e)
            abort(400, str(e))
        else:
            logging.info(data)
            return data

    def prepare_form_args(self, request_form):
        return {k: v[-1] for k, v in request_form.items()}

    async def post(self, request):
        form_args = self.schema_post_form(self.prepare_form_args(request.form))
        app = request.files.get('app')
        if not app:
            abort(400, "app is empty")

        app_name = f"{form_args['name']}-{form_args['platform']}-{form_args['version']}-{app.name}"
        app_path = Path(f"uploads/{app_name}")
        with open(app_path, "wb") as f:
            f.write(app.body)

        try:
            new_app = await App.create(file=app_name, **form_args)
        except Exception as e:
            if app_path.exists():
                remove(str(app_path))
            abort(400, str(e))
        else:
            return json(new_app.json_format(), 201)

    def schema_post_form(self, request_form):
        try:
            data = Schema({
                Optional("name", default="zhdj"): Use(str),
                "platform": And(Use(lambda x: x.strip().lower()), lambda x: x in (PLAT_ANDROID, PLAT_IOS)),
                "version": Use(int)
            }).validate(request_form)
        except Exception as e:
            logging.error(e)
            abort(400, str(e))
        else:
            return data


def get_current_app_version(name, platform):
    return App.query.with_only_columns([App.file]). \
        where(App.platform == platform).where(App.name == name). \
        where(App.is_active == True). \
        order_by(desc(App.id)). \
        gino.first()


# noinspection PyUnusedLocal
class AppCurrentVersionView(HTTPMethodView):
    async def get(self, request, name, platform):
        platform = platform.strip().lower()
        if platform not in (PLAT_ANDROID, PLAT_IOS):
            abort(400, "wrong platform")

        # where 中 一定要用 == True，用 is True会报错
        current_version = await get_current_app_version(name, platform)

        logging.info(current_version)

        if current_version:
            return json({"version": current_version.version, "platform": platform,
                         "file": current_version.file,
                         "create_at": datetime_2_isoformat(current_version.create_at)})
        else:
            return json({"version": None, "platform": platform,
                         "file": None,
                         "create_at": None})


# noinspection PyUnusedLocal
class AppCurrentVersionDownloadView(HTTPMethodView):
    async def get(self, request, name, platform):
        platform = platform.strip().lower()
        if platform not in (PLAT_ANDROID, PLAT_IOS):
            abort(400, "wrong platform")

        # where 中 一定要用 == True，用 is True会报错
        current_version = await get_current_app_version(name, platform)

        # TODO downloads count
        logging.info(current_version)
        logging.info(Path().absolute())

        if current_version:
            file_path = Path(f'uploads/{current_version.file}')
            if not file_path.exists():
                abort(500, "no file found")
            return await file_stream(file_path, mime_type="application/octet-stream",
                                     filename=file_path.name)
        else:
            return abort(400, "no app found")
