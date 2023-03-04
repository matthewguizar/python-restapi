import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

import schemas
from schemas import PlainStoreSchema
from db import stores

blue_print = Blueprint("stores", __name__, description="Operations on stores")


@blue_print.route("/store/<string:store_id>")
class Store(MethodView):
    @blue_print.response(200, PlainStoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message="store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "store deleted"}
        except KeyError:
            abort(404, message="store not found")


@blue_print.route("/store")
class StoreList(MethodView):
    @blue_print.response(200, PlainStoreSchema(many=True))
    def get(self):
        return {"stores": list(stores.values())}

    @blue_print.arguments(PlainStoreSchema)
    @blue_print.response(200, PlainStoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"store already exists")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}  # unpacking **
        stores[store_id] = store
        return store

